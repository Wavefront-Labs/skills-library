---
id: computing-software.cryptography-implementation.crypto-libraries.python-ssl-module-hardening
name: python-ssl-module-hardening
category: computing-software
field: cryptography-implementation
product: crypto-libraries
tags: [crypto-libraries, cryptography-implementation, python-ssl-module, python, ssl, sslcontext, tls, truststore, certifi, mtls, hostname-verification]
level: practitioner
status: verified
description: "Configure Python's ssl module safely: create_default_context, minimum_version, private CAs, mTLS servers, truststore for OS roots, and removed or unsafe APIs."
sources: ["https://docs.python.org/3/library/ssl.html", "https://docs.python.org/3/library/ssl.html#security-considerations", "https://truststore.readthedocs.io/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Python ssl module hardening

## Client
```python
import ssl, socket
ctx = ssl.create_default_context()                 # CERT_REQUIRED, check_hostname=True, system/certifi roots
ctx.minimum_version = ssl.TLSVersion.TLSv1_2        # already the default on 3.10+ (checked on 3.14)
# private CA (adds to defaults): ctx.load_verify_locations(cafile="corp-root.pem")
# client certificate:            ctx.load_cert_chain("client.pem", "client.key")
with socket.create_connection(("api.internal", 443)) as s:
    with ctx.wrap_socket(s, server_hostname="api.internal") as tls:
        print(tls.version(), tls.cipher())
```
Python 3.13+ also sets `VERIFY_X509_STRICT` and `VERIFY_X509_PARTIAL_CHAIN` in `create_default_context` (docs: "Changed in version 3.13"; both flags set on 3.14); some
non-compliant private CA certificates (missing AKI, bad basicConstraints) start failing. Fix the certificates rather
than clearing the flags.

## Server with mutual TLS
```python
ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
ctx.load_cert_chain("server-fullchain.pem", "server.key")
ctx.verify_mode = ssl.CERT_REQUIRED
ctx.load_verify_locations("client-ca.pem")
ctx.minimum_version = ssl.TLSVersion.TLSv1_2
```

## Trust stores
- Default: OpenSSL's configured store; on Windows `load_default_certs` also reads the system CA and ROOT stores (`ssl.enum_certificates`), which loaded 100+ roots in testing.
- `certifi` bundles Mozilla roots (used by requests).
- `truststore` (`truststore.inject_into_ssl()`) uses the OS trust store and policy on Windows, macOS and Linux,
  which picks up enterprise-installed roots; pip uses it by default from pip 24.2 (pip docs). `inject_into_ssl()` is for applications only; libraries should use `truststore.SSLContext`.

## Unsafe or removed
- `ssl._create_unverified_context()` and `verify=False` in requests/httpx disable verification.
- `ssl.wrap_socket()` was removed in 3.12 (What's New); use `SSLContext.wrap_socket`.
- `ssl.PROTOCOL_TLS` / `PROTOCOL_SSLv23` (deprecated; `DeprecationWarning` on 3.14) without `create_default_context` leave hostname checks off and `verify_mode` at `CERT_NONE` (checked); `PROTOCOL_TLS_CLIENT` turns both on.
- `check_hostname = False` with `CERT_REQUIRED` still accepts any valid certificate for any name (checked: a connection with a wrong server_hostname succeeded).

## Verify
- [ ] A wrong-hostname connection raises `SSLCertVerificationError` (checked locally with a private-CA server; `wrong.host.badssl.com` returned `SSLEOFError` from this network instead, so use a local test server).
- [ ] `tls.version()` shows TLSv1.2 or TLSv1.3 only.
