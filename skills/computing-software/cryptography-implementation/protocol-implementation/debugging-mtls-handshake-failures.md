---
id: computing-software.cryptography-implementation.protocol-implementation.debugging-mtls-handshake-failures
name: debugging-mtls-handshake-failures
category: computing-software
field: cryptography-implementation
product: protocol-implementation
tags: [protocol-implementation, cryptography-implementation, mtls-troubleshooting, mutual-tls, mtls, client-certificate, nginx, load-balancer, crl, troubleshooting]
level: practitioner
status: docs-checked
description: "Diagnose server-side mutual TLS failures using nginx client-verification settings and variables, TLS 1.3 post-handshake auth, and AWS ALB mTLS modes."
sources: ["https://nginx.org/en/docs/http/ngx_http_ssl_module.html", "https://www.rfc-editor.org/rfc/rfc8446#section-4.6.2", "https://docs.aws.amazon.com/elasticloadbalancing/latest/application/mutual-authentication.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Debugging mTLS handshake failures

## nginx: what to check
- `ssl_verify_client` is `off` by default. `on` requires and verifies a client certificate; `optional` requests one and verifies it only if present; `optional_no_ca` requests one but does not require a trusted CA signature (for cases where a service outside nginx does the verification, using `$ssl_client_cert`).
- The result is in `$ssl_client_verify`: `SUCCESS`, `FAILED:reason`, or `NONE` when no certificate was presented. Log it, plus `$ssl_client_s_dn` (subject DN in RFC 2253 form) and `$ssl_client_serial`, to separate "no certificate sent" from "certificate rejected".
- `ssl_verify_depth` defaults to 1. A client chain with intermediates may need a larger value.
- `ssl_client_certificate` supplies the trusted CA certificates used to verify clients and the list is sent to clients; `ssl_trusted_certificate` verifies without sending the list. Make sure the issuing CA (and intermediates) for the client certificate are in the verification set.
- With `ssl_crl`, CRLs for intermediates must be in the same file as the root CA's. Check the CRL's `nextUpdate` (RFC 5280: the date by which the next CRL will be issued) as a possible cause of sudden failures.

## TLS 1.3 post-handshake authentication
Under RFC 8446 section 4.6.2, a server may request client authentication after the handshake only if the client sent the `post_handshake_auth` extension; a client that receives a CertificateRequest without having sent it must send an `unexpected_message` fatal alert. Clients can also decline by sending an empty Certificate message. Servers must be prepared for delay and for other messages arriving in between.

## AWS Application Load Balancer
- Two modes: passthrough (the load balancer sends the entire client certificate chain to the target without verifying it; the target must verify) and verify (the load balancer authenticates clients against a trust store).
- Session resumption is not supported in either mode.
- Certificate information reaches backends in `X-Amzn-Mtls-*` headers: in passthrough mode `X-Amzn-Mtls-Clientcert` holds the URL-encoded PEM chain; in verify mode there are serial number, issuer, subject, validity and leaf headers.
- Supported client certificates are X.509v3 with RSA 2K-8K or ECDSA secp256r1, secp384r1 or secp521r1 keys. CA bundle files must be PEM with no blank lines, and bundles are uploaded as a whole.
- "Advertise CA subject names" lets the load balancer put the trusted CA DNs in its CertificateRequest so clients pick matching certificates.
- Connection logs record client certificate information, connection results and TLS ciphers.

## Verify
- [ ] Logs show `$ssl_client_verify` for each failure class.
- [ ] CRL expiry (`nextUpdate`) is monitored.

## Checked
Method: docs-checked 2026-11-09 against the nginx ngx_http_ssl_module page (ssl_verify_client, ssl_verify_depth, ssl_client_certificate, ssl_crl, variables), RFC 8446 section 4.6.2 and RFC 5280 section 5.1.2.5, and the AWS ALB mutual authentication page (full).
Removed as unconfirmed: the symptom-to-error-message table (specific OpenSSL error numbers and the nginx 400 text), the claim that OpenSSL rejects all certificates after CRL nextUpdate, EKU "unsupported certificate purpose" diagnosis, clock skew, the openssl s_client and verify command lines, NLB passthrough, and Envoy/Istio `x-forwarded-client-cert`.
