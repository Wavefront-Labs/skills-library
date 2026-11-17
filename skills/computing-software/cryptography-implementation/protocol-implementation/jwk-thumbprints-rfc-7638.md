---
id: computing-software.cryptography-implementation.protocol-implementation.jwk-thumbprints-rfc-7638
name: jwk-thumbprints-rfc-7638
category: computing-software
field: cryptography-implementation
product: protocol-implementation
tags: [protocol-implementation, cryptography-implementation, jwk-thumbprint, jwk, rfc-7638, rfc-9278, kid, jose, dpop, acme]
level: practitioner
status: docs-checked
description: "Compute RFC 7638 JWK thumbprints correctly (required members, lexicographic order, no whitespace) for kid values, DPoP jkt, ACME key authorizations and URIs."
sources: ["https://www.rfc-editor.org/rfc/rfc7638", "https://www.rfc-editor.org/rfc/rfc9278", "https://www.rfc-editor.org/rfc/rfc8555", "https://www.rfc-editor.org/rfc/rfc8037", "https://www.rfc-editor.org/rfc/rfc9449"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# JWK thumbprints (RFC 7638)

## Algorithm
1. Take only the **required** members for the key type:
   - EC: `crv`, `kty`, `x`, `y`
   - RSA: `e`, `kty`, `n`
   - OKP (Ed25519/X25519): `crv`, `kty`, `x`
   - oct: `k`, `kty`
2. Serialise as JSON with members in lexicographic order, no whitespace, UTF-8.
3. Hash with SHA-256; base64url-encode without padding.

```python
import json, hashlib, base64
def jwk_thumbprint(jwk: dict) -> str:
    req = {"EC": ["crv", "kty", "x", "y"], "RSA": ["e", "kty", "n"], "OKP": ["crv", "kty", "x"], "oct": ["k", "kty"]}[jwk["kty"]]
    canon = json.dumps({k: jwk[k] for k in req}, separators=(",", ":"), sort_keys=True)
    return base64.urlsafe_b64encode(hashlib.sha256(canon.encode()).digest()).rstrip(b"=").decode()
```
RFC 7638 section 3.1 gives an RSA example whose thumbprint is `NzbLsXh8uDCcd-6MNwXF4W_7noWXFZAfHkxZsRGC9Xs`; use it
as a test.

## Uses
- `kid` values that are stable and derivable from the key itself.
- DPoP: access tokens carry `cnf.jkt` = thumbprint of the client's DPoP key.
- ACME: key authorization = `token || "." || thumbprint(account key)` for HTTP-01 and DNS-01.
- RFC 9278 URI form: `urn:ietf:params:oauth:jwk-thumbprint:sha-256:<thumbprint>`.

## Gotchas
- Including optional members (`kid`, `use`, `alg`) changes the hash.
- Use the member values exactly as they appear in the JWK; the hash input is the UTF-8 JSON of those members.
- Do not rely on a JSON serialiser to sort members for you (RFC 7638 warns it cannot be counted on); build the string in lexicographic order yourself.

## Verify
- [ ] RFC 7638 example produces the published thumbprint.

## Checked
2026-11-01. Confirmed against RFC 7638 (required members, lexicographic order, no whitespace, UTF-8, SHA-256, example thumbprint), RFC 8037 (OKP crv, kty, x), RFC 9278 (URN form and the same example value), RFC 9449 (`cnf.jkt` is the SHA-256 thumbprint of the DPoP key) and RFC 8555 (ACME key authorization uses the account key thumbprint). Removed: unconfirmed padding and leading-zero claim and the non-ASCII serialiser claim.
Method: documentation only; no commands were run.
