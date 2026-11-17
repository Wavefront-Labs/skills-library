---
id: computing-software.cryptography-implementation.openssl.ocsp-and-crl-revocation-checking
name: ocsp-and-crl-revocation-checking
category: computing-software
field: cryptography-implementation
product: openssl
tags: [cryptography-implementation, openssl, ocsp, crl, certificate-revocation, ocsp-stapling, soft-fail, hard-fail, openssl-ocsp, must-staple, revocation-checking, x509]
level: advanced
status: docs-checked
description: "Checking certificate revocation with OpenSSL: inspecting CRLs, querying OCSP, testing stapling with s_client -status, Must-Staple, and the soft-fail versus hard-fail decision."
sources: ["https://docs.openssl.org/3.0/man1/openssl-ocsp/", "https://docs.openssl.org/3.0/man1/openssl-crl/", "https://docs.openssl.org/3.0/man1/openssl-s_client/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OCSP and CRL revocation checking with OpenSSL

The `certificates-csrs-and-tls-testing` skill in this product covers issuing and inspecting certificates; this one
covers checking whether a certificate you trust has since been revoked.

## CRL versus OCSP
- **CRL:** the issuing CA publishes a signed list of revoked certificates. Inspect one with
  `openssl crl -in revoked.crl -noout -text`. The relying party downloads the list and checks membership locally.
- **OCSP:** a query to a responder about one certificate. Query manually while debugging with
  `openssl ocsp -issuer ca.pem -cert leaf.pem -url http://ocsp.example.com -text`
  (`-text` prints the request and response in text form). The responder learns which certificate is being checked.

## OCSP stapling
With stapling the server attaches a signed OCSP response to the TLS handshake, so clients need no live OCSP call.
Test what a server staples with `openssl s_client -connect host:443 -status`: it sends a certificate status request and
prints the server's response, if any. An absent response for a certificate whose issuer supports stapling is worth
investigating.

## Soft-fail versus hard-fail
- **Soft-fail** continues the connection when the revocation check cannot complete; **hard-fail** rejects it. Find out
  which your TLS stack does by default rather than assuming. Soft-fail can be defeated by blocking the check traffic.
- Hard-fail makes availability depend on the CA's revocation infrastructure; choose that trade-off deliberately.
- **Must-Staple** is the X.509 TLS Feature extension; `tlsfeature = status_request` in an OpenSSL extension
  configuration (see the x509v3_config man page) requests it. Clients that honour it expect a stapled response, so the
  server must staple.

## Verify
- [ ] It is known, not assumed, whether the TLS stack in use is soft-fail or hard-fail.
- [ ] If stapling is expected, `openssl s_client -status` shows a valid stapled response.
- [ ] CRL and OCSP endpoints named in issued certificates are reachable from the validating environment.
- [ ] A deliberate soft-fail versus hard-fail or Must-Staple choice is on record.

## Checked

2026-11-01. Confirmed in the OpenSSL man pages: openssl-crl (`-in`, `-noout`, `-text`), openssl-ocsp (`-issuer`, `-cert`, `-url`, `-text`), openssl-s_client (`-status` sends a certificate status request and prints the response) and x509v3_config (TLS Feature, aka Must Staple, `tlsfeature = status_request`). Removed: size, propagation and privacy comparisons, the RFC 7633 citation, and claims about default behaviour and effectiveness of soft-fail in particular stacks and browsers.
Method: documentation only; no commands were run.
