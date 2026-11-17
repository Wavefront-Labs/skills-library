---
id: computing-software.cryptography-implementation.protocol-implementation.tls-integration-and-certificate-validation
name: tls-integration-and-certificate-validation
category: computing-software
field: cryptography-implementation
product: protocol-implementation
tags: [cryptography-implementation, protocol-implementation, tls, tls-1-3, ssl, certificate-validation, hostname-verification, sni, trust-store, ca-bundle, mutual-tls, mtls, certificate-pinning, spki, insecureskipverify, verify-false, trustmanager, rejectunauthorized, testssl, badssl, ocsp-stapling, session-resumption, 0-rtt, early-data, alpn, openssl, go-tls, python-ssl, jsse]
level: advanced
status: draft
description: "Integrate TLS without weakening it: TLS 1.2+ (prefer 1.3), hostname checks, SNI, private trust stores, mTLS, pinning trade-offs, the verify=False family of bugs, 0-RTT replay and negative testing."
sources: ["RFC 8446", "RFC 6125", "RFC 8470", "RFC 7301", "https://ssl-config.mozilla.org/", "https://github.com/testssl/testssl.sh", "https://badssl.com/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# TLS integration and certificate validation

**Goal:** get confidentiality *and* peer authentication from the platform TLS stack.
Most real-world TLS failures are not broken ciphers; they are clients that stopped
checking who they are talking to.

## 1. Don't build it, configure it
Use the platform or well-maintained stack: OpenSSL/BoringSSL, rustls, Go
`crypto/tls`, JSSE, SChannel, Apple Network.framework. Never parse certificates or
build record layers yourself. Set **TLS 1.2 minimum, prefer 1.3**. Take cipher lists
from the Mozilla SSL Configuration Generator ("intermediate" profile) instead of
writing your own.

## 2. Client validation: the three checks
1. Chain to a trusted root (trust store).
2. **Hostname matches a SAN** (DNS or IP). The CN is not used.
3. Validity dates and key usage.
Most high-level clients do all three by default. Lower-level APIs often skip step 2:

| Stack | Safe setup | Bug to grep for |
|---|---|---|
| Python | `ssl.create_default_context()`; `ctx.minimum_version = ssl.TLSVersion.TLSv1_2`; requests `verify="ca.pem"` for a private CA | `verify=False`, `CERT_NONE`, `check_hostname = False`, `_create_unverified_context` |
| Go | `&tls.Config{MinVersion: tls.VersionTLS12, RootCAs: pool}` | `InsecureSkipVerify: true` |
| Java | default `SSLContext`; on raw `SSLSocket` set `params.setEndpointIdentificationAlgorithm("HTTPS")` | `X509TrustManager` with empty `checkServerTrusted`, `HostnameVerifier` returning `true` |
| Node | `tls.connect({ host, servername: host, ca })`, `NODE_EXTRA_CA_CERTS` | `rejectUnauthorized: false`, `NODE_TLS_REJECT_UNAUTHORIZED=0` |
| OpenSSL C | `SSL_CTX_set_verify(ctx, SSL_VERIFY_PEER, NULL)`, `SSL_CTX_set_default_verify_paths`, `SSL_set1_host(ssl, host)`, `SSL_set_tlsext_host_name(ssl, host)`, `SSL_CTX_set_min_proto_version(ctx, TLS1_2_VERSION)` | missing `SSL_set1_host` (OpenSSL does not check hostnames unless told to) |
| curl | `--cacert ca.pem` | `-k` / `--insecure` |

For a private CA, **add the CA** to that client's trust store. Do not disable
verification "until we sort out certs". Add a CI grep or lint rule that fails on the
bug patterns above.

## 3. SNI and ALPN
Send SNI (the hostname) or multi-tenant servers and CDNs return the wrong
certificate. Most clients send it automatically; raw OpenSSL needs
`SSL_set_tlsext_host_name`. ALPN (RFC 7301) negotiates `h2` or `http/1.1`. A
mismatch shows up as protocol errors after a successful handshake, not as a TLS
failure.

## 4. Mutual TLS
Server: Go `ClientAuth: tls.RequireAndVerifyClientCert` with a dedicated `ClientCAs`
pool; nginx `ssl_verify_client on` + `ssl_client_certificate`. Use a **separate CA** for client certs. Authorise on a specific identity (SAN URI
such as a SPIFFE ID, or DNS name), not on "has any valid cert". Prefer short-lived,
automatically issued client certs over revocation lists.

## 5. Pinning trade-offs
Pinning defends against a mis-issuing CA, and the cost is bricked clients when keys
change. If you pin: pin the **SPKI hash**, not the whole cert; always ship at least
one **backup pin** for a key you have not yet deployed; give pins an expiry (Android
Network Security Config supports this); and have a remote-update path. Browsers
dropped HPKP. For web, rely on Certificate Transparency monitoring instead. Pinning
makes most sense for mobile apps talking to your own API, or for internal services
pinned to a private CA (trust only that CA, which is simpler than per-key pins).

## 6. Revocation, resumption, 0-RTT
- **OCSP stapling** spares clients the extra lookup, but client revocation checking
  is mostly soft-fail. Some public CAs have been moving away from OCSP toward CRLs
  and short-lived certs (Let's Encrypt announced the end of its OCSP service in
  2025), so check your CA's current position before relying on stapling.
- **Session resumption:** rotate session-ticket keys (for example daily) and share
  them across the fleet securely. A ticket key that never changes weakens forward
  secrecy.
- **0-RTT early data can be replayed** (RFC 8446 section 8). Only enable it for
  idempotent requests. Behind a proxy, honour `Early-Data: 1` and return `425 Too
  Early` for unsafe methods (RFC 8470). If in doubt, keep it off.

## 7. Testing
- `testssl.sh https://host:443` checks protocols, ciphers, chain, known
  vulnerabilities and stapling. Run it against staging in CI.
- **Negative tests** for your client: connections to `expired.badssl.com`,
  `wrong.host.badssl.com`, `self-signed.badssl.com` and `untrusted-root.badssl.com`
  must **fail**. For offline CI, mint the equivalents with a test CA (see
  `computing-software.cryptography-implementation.openssl.certificates-csrs-and-tls-testing`).

## Gotchas
- Verification disabled in a test helper that ends up in production code is the
  most common TLS bug. Keep the insecure option out of the codebase entirely.
- IP-address connections need an IP SAN.
- Proxies doing TLS interception need their CA trusted explicitly. Never "fix" this
  by turning verification off.

## Verify
- [ ] The client rejects expired, wrong-host, self-signed and untrusted-root certs in automated tests.
- [ ] TLS 1.0/1.1 handshakes fail; TLS 1.3 succeeds.
- [ ] A grep for `InsecureSkipVerify`, `verify=False`, `rejectUnauthorized: false` or a trust-all TrustManager finds nothing.
- [ ] mTLS authorisation checks a specific client identity.
- [ ] 0-RTT is disabled, or limited to idempotent requests.
- [ ] Pins (if any) include a backup and an expiry.
