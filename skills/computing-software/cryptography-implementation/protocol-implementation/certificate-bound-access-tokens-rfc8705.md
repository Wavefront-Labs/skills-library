---
id: computing-software.cryptography-implementation.protocol-implementation.certificate-bound-access-tokens-rfc8705
name: certificate-bound-access-tokens-rfc8705
category: computing-software
field: cryptography-implementation
product: protocol-implementation
tags: [cryptography-implementation, protocol-implementation, mutual-tls, mtls, rfc8705, oauth2, sender-constrained-tokens, cnf-x5t-s256]
level: advanced
status: docs-checked
description: "Implement OAuth 2.0 mTLS (RFC 8705): client auth with certificates, binding access tokens via cnf x5t#S256, and resource servers checking the thumbprint on every call."
sources: ["https://www.rfc-editor.org/rfc/rfc8705", "https://www.rfc-editor.org/rfc/rfc7800", "https://www.rfc-editor.org/rfc/rfc9449"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Certificate-bound access tokens (RFC 8705)

Bearer tokens work for whoever holds them. RFC 8705 binds an access token to the client's
TLS certificate, so a stolen token is useless without the private key.

## Two independent features
1. **mTLS client authentication** at the token endpoint (replaces client secrets):
   - `tls_client_auth`: the AS checks the cert's subject DN or a SAN (`tls_client_auth_san_dns`,
     `_uri`, `_ip`, `_email`) registered for the client, chained to a trusted CA.
   - `self_signed_tls_client_auth`: the client registers its cert (JWKS); the AS matches it.
2. **Certificate-bound tokens**: the AS embeds the cert thumbprint in the token.

## Token binding format
```json
{ "iss": "https://as.example", "sub": "client-123", "aud": "https://api.example",
  "exp": 1760000000,
  "cnf": { "x5t#S256": "bwcK0esc3ACC3DB2Y5_lESsXE8o9ltc05O89jdN-dg2" } }
```
`x5t#S256` = base64url (no padding) of SHA-256 over the **DER of the whole client certificate**.
For opaque tokens, introspection returns the same `cnf` member.

## Resource server check (every request)
```python
import base64, hashlib, hmac
def thumbprint(der: bytes) -> str:
    return base64.urlsafe_b64encode(hashlib.sha256(der).digest()).rstrip(b"=").decode()
if not hmac.compare_digest(thumbprint(client_cert_der), claims["cnf"]["x5t#S256"]):
    return 401   # WWW-Authenticate error="invalid_token"
```
- The RS must obtain the client certificate from its TLS layer and reject a mismatch with HTTP 401 and
  `invalid_token` (RFC 8705 section 3). If TLS terminates at a proxy, how the certificate is passed on is out of
  scope of the RFC (section 6.5); authenticate that channel yourself.
- Missing `cnf` on an endpoint that requires bound tokens: reject, do not downgrade to bearer.

## Deployment details
- Metadata: AS advertises `tls_client_certificate_bound_access_tokens: true` and may publish
  `mtls_endpoint_aliases` (alias endpoints on a different host, so browsers and conventional clients on the normal
  endpoints are not prompted for a client certificate).
- The RS must know in advance that mutual TLS is used: the access token cannot decide whether to request a client
  certificate, because it arrives after the handshake.
- Updating a client certificate invalidates tokens bound to it; the client gets a new token (typically with a
  refresh token). Refresh tokens of clients using `tls_client_auth` or `self_signed_tls_client_auth` are indirectly
  certificate-bound through client authentication; public clients should have refresh tokens bound to the
  certificate directly (section 4).
- Binding is not supported for tokens issued directly from the authorization endpoint (implicit grant).
- DPoP (RFC 9449) is the application-layer alternative for sender-constraining tokens.

## Verify
- [ ] Replaying a valid token from a different client cert gets 401.
- [ ] Thumbprint computed over DER of the leaf cert, base64url without padding, compared in constant time.
- [ ] Token endpoint rejects clients whose cert SAN/DN does not match registration.

## Checked
2026-11-01. Confirmed against RFC 8705: sections 2.1.2 and 2.2 (client auth methods and SAN/DN metadata), 3 and 3.1
(binding, 401 invalid_token, x5t#S256 as unpadded base64url SHA-256 of the DER certificate, example thumbprint),
3.3 (metadata flag), 4, 5 (mtls_endpoint_aliases), 6.3 to 6.5, 7.1. Removed: the claim that the RS needs no chain
validation, the FAPI 2.0 acceptance claim, and token-lifetime advice (not in the RFC).
Method: documentation only; no commands were run.
