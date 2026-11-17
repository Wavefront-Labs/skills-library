---
id: computing-software.cybersecurity-defensive.identity-protocols.oauth-mtls-certificate-bound-tokens
name: oauth-mtls-certificate-bound-tokens
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [oauth-mtls-certificate-bound-tokens, oauth-mtls, cnf, x5t#s256, certificate-bound, sender-constrained, mtls-tokens, identity-protocols]
level: advanced
status: docs-checked
description: "Issue tokens bound to the client certificate with cnf x5t#S256, and have resource servers compare the TLS client certificate thumbprint."
sources:
  - https://www.rfc-editor.org/rfc/rfc8705
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Certificate-bound access tokens

Goal: reject tokens presented on a connection from another certificate.

Method (RFC 8705 Section 3): when the token request is made over mutual TLS, the AS binds the issued access token to the client certificate. For JWT access tokens it carries a `cnf` claim with `x5t#S256`, the base64url-encoded (no padding) SHA-256 hash of the DER encoding of the X.509 certificate; for token introspection the same `cnf` member is returned. The RS MUST obtain the client certificate from its TLS layer on every request and verify that it matches the certificate associated with the token; if not, it MUST reject the request with HTTP 401 and error code `invalid_token`. Metadata: `tls_client_certificate_bound_access_tokens` (boolean, default false) in server metadata and as a client registration parameter.

Gotchas:
- Refresh tokens are indirectly certificate-bound: RFC 6749 binds them to the client and confidential clients authenticate when using them, which with `tls_client_auth` or `self_signed_tls_client_auth` is certificate-based. RFC 8705 Section 4 covers refresh tokens for public clients.
- If TLS terminates at a load balancer or reverse proxy, how certificate information reaches the application is out of scope of RFC 8705 (Section 6.5): secure the hop yourself.
- Because the token is bound to one certificate, a client that updates its certificate invalidates its tokens and must request a new one, typically with a refresh token.
- A client that wants bound tokens but calls the token endpoint without mutual TLS may get an error or an unbound token, at the AS's discretion.

Verify: use the token with another client certificate and expect 401.

## Checked

Date: 2026-11-02. Confirmed in RFC 8705 Sections 3, 3.2, 3.4, 4, 6.3 and 6.5. Removed as not stated there: the "strip inbound header copies" gateway advice and the "keep lifetimes short" figure.

Method: documentation only; no commands were run.
