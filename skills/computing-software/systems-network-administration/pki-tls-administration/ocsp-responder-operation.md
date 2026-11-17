---
id: computing-software.systems-network-administration.pki-tls-administration.ocsp-responder-operation
name: ocsp-responder-operation
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [ocsp-responder-operation, pki-ocsp, ocsp, rfc6960, responder, nocheck, pki-tls-administration]
level: practitioner
status: docs-checked
description: "Run an OCSP responder: delegated signing certs, nocheck, nonces, caching and what status values to return, per RFC 6960 and RFC 5019."
sources:
  - https://www.rfc-editor.org/rfc/rfc6960
  - https://www.rfc-editor.org/rfc/rfc5019
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OCSP responder operation
Goal: real-time status with predictable load.
- RFC 6960 defines OCSP; RFC 5019 is the lightweight profile for high-volume use (pre-produced responses, caching).
- Transport (RFC 5019 section 5): the responder MUST support HTTP. Requests of 255 bytes or less in total (after encoding, including `http://` and the server name) use GET so responses can be cached; larger requests SHOULD use POST. The GET path is the URL-encoded base64 of the DER OCSPRequest appended to the AIA URI.
- Delegated responder certificate (RFC 6960 section 4.2.2.2): issued by the same CA that issued the certificates it answers for, with `id-kp-OCSPSigning` in the extended key usage. Alternatively the CA signs responses itself.
- Revocation checking of the responder certificate: with `id-pkix-ocsp-nocheck` (non-critical, value NULL) the client trusts the responder for the certificate's lifetime. RFC 6960 warns that compromise of that key is as serious as a CA key compromise for the validity period, and suggests short lifetimes with frequent renewal. RFC 5019 recommends nocheck, no OCSP AIA and no CRL distribution points in the responder certificate, and a relatively short-lived certificate.
- Pre-produced responses (RFC 5019 section 2.2.4): the responder MUST set `thisUpdate`, `nextUpdate` and `producedAt`, and MUST always include `nextUpdate`, to aid caching. Times are GMT in `YYYYMMDDHHMMSSZ` form, seconds included. Clients reject a response with no `nextUpdate` or outside the thisUpdate to nextUpdate window.
- Caching headers (RFC 5019 section 6): `last-modified`, `ETag`, `expires` (the nextUpdate date) and `cache-control: max-age=<n>, public, no-transform, must-revalidate`; responders MUST NOT send `no-cache` or `no-store` on cacheable responses.
- Nonces: a pre-producing responder that cannot answer a nonce request SHOULD return a response without a nonce, and clients SHOULD still process it; a client that knows the server supports nonces MUST reject a reply lacking the expected nonce.
- Status values (RFC 6960 section 2.2): `good`, `revoked`, `unknown`. `good` means no certificate with that serial in its validity interval is revoked; it does not necessarily mean the certificate was ever issued. `revoked` MAY also be returned for a serial the CA never issued. `unknown` means the responder does not know the requested certificate, usually an unrecognised issuer.
- A pre-producing responder without authoritative records answers with OCSPResponseStatus `unauthorized` (RFC 5019 section 2.2.3).
- Run it over HTTP behind a cache or CDN: the profile is designed so intermediaries can cache responses.
Verify:
- [ ] A request for a good certificate returns `good` with a sane `thisUpdate` / `nextUpdate` window.
- [ ] A revoked certificate returns `revoked` with its reason within your target time.
- [ ] The responder certificate has the OCSPSigning EKU and, if you rely on it, the nocheck extension.

## Checked
Confirmed 2026-11-08 against RFC 6960 (sections 2.2, 4.2.2.2, 4.2.2.2.1) and RFC 5019 (sections 2.2, 4, 5, 6). Removed: the `openssl ocsp` commands and flags (not in the cited pages), the `nextUpdate` of 1 to 4 days, the CDN advice as a numeric target, the "Baseline Requirements say never answer good" claim (not on the cited pages; RFC 6960 only says good does not imply issuance), and the nonce gotcha about `openssl ocsp -nonce`.
Method: docs-only read of cited pages, 2026-11-08
