---
id: computing-software.software-engineering.python.tls-with-ssl-contexts
name: tls-with-ssl-contexts
category: computing-software
field: software-engineering
product: python
tags: [python, py-networking, ssl-contexts, ssl, tls, certificate-verification, create-default-context, mtls]
level: practitioner
status: docs-checked
description: "Configure TLS in Python with ssl.create_default_context: verification, custom CAs, minimum TLS version, client certs, server contexts and the 3.13 strict verify flags."
sources: ["https://docs.python.org/3/library/ssl.html", "https://docs.python.org/3/library/ssl.html#security-considerations"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TLS with ssl contexts

```python
import ssl, socket

ctx = ssl.create_default_context()                 # verifies certs and hostname
ctx.minimum_version = ssl.TLSVersion.TLSv1_2
with socket.create_connection(("example.com", 443), timeout=5) as raw:
    with ctx.wrap_socket(raw, server_hostname="example.com") as tls:   # server_hostname needed to check the name
        print(tls.version(), tls.getpeercert()["subject"])

# Private CA: trust exactly this file, keep verification on
ctx = ssl.create_default_context(cafile="ca.pem")

# Mutual TLS client
ctx.load_cert_chain("client.pem", "client.key")

# Server side
srv = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
srv.load_cert_chain("server.pem", "server.key")
srv.verify_mode = ssl.CERT_REQUIRED               # clients must present a cert
srv.load_verify_locations("clients-ca.pem")       # required with CERT_REQUIRED
```

## What the defaults do
- `create_default_context()` uses `PROTOCOL_TLS_CLIENT` or `PROTOCOL_TLS_SERVER`, sets `verify_mode` to `CERT_REQUIRED` for `SERVER_AUTH`, and loads either the CA files you pass (`cafile`, `capath`, `cadata`) or the system default CA certificates.
- `CERT_REQUIRED` alone does not match hostnames in client mode; `check_hostname` must also be on. `PROTOCOL_TLS_CLIENT` enables both by default.
- `CERT_NONE` on a client accepts just about any certificate, including untrusted or expired ones.
- `SSLContext.load_default_certs()` loads the default CA certificates for a context you built by hand.

## Never do
- Disable verification (`check_hostname = False` with `CERT_NONE`, or an unverified context) outside local debugging; fix the trust store instead.

## Gotchas
- Since Python 3.13 the default context sets `VERIFY_X509_PARTIAL_CHAIN` and `VERIFY_X509_STRICT`. Strict mode may reject pre-RFC 5280 or malformed certificates that OpenSSL otherwise accepts; the docs say disabling it is not recommended (`ctx.verify_flags &= ~ssl.VERIFY_X509_STRICT`). Prefer reissuing the certificate.
- `CERT_REQUIRED` on a server needs CA certificates passed to `load_verify_locations()`.

## Verify
- [ ] A connection to a host with an expired or untrusted certificate fails with `SSLCertVerificationError`.

## Checked
Date: 2026-11-03. Confirmed against the ssl module documentation: `create_default_context` behaviour and parameters, `CERT_NONE`/`CERT_REQUIRED` semantics, `check_hostname`, `wrap_socket(server_hostname=)`, the 3.13 default verify flags and the strict-mode note. Removed as not in the page: certifi and macOS "Install Certificates.command", `SSL_CERT_FILE`/`SSL_CERT_DIR`, Authority Key Identifier remark, certificate pinning, urllib/httpx/asyncio integration lines, `openssl s_client` and badssl.com checks, frozen-app advice.
Method: documentation only; no commands were run.
