---
id: computing-software.cryptography-implementation.protocol-implementation.jws-compact-and-json-serializations
name: jws-compact-and-json-serializations
category: computing-software
field: cryptography-implementation
product: protocol-implementation
tags: [protocol-implementation, cryptography-implementation, jws-json-serialization, jws, jose, rfc-7515, detached-payload, rfc-7797]
level: advanced
status: docs-checked
description: "Produce and parse JWS compact and JSON serializations (RFC 7515): signing input, protected versus unprotected headers, multiple signatures, detached payloads and b64 false."
sources: ["https://www.rfc-editor.org/rfc/rfc7515", "https://www.rfc-editor.org/rfc/rfc7797"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# JWS compact and JSON serializations

## Compact
`BASE64URL(protected) . BASE64URL(payload) . BASE64URL(signature)`
Signing input is the ASCII bytes `BASE64URL(protected) || '.' || BASE64URL(payload)`. Single signature, all
header parameters protected.

## JSON (general)
```json
{"payload":"eyJpc3MiOiJqb2UifQ",
 "signatures":[
   {"protected":"eyJhbGciOiJFUzI1NiJ9","header":{"kid":"e1"},"signature":"..."},
   {"protected":"eyJhbGciOiJSUzI1NiJ9","header":{"kid":"r1"},"signature":"..."}]}
```
- Flattened form has a single `protected`/`header`/`signature` at the top level.
- `header` (unprotected) values are not integrity protected (RFC 7515); keep `alg`, `crit` and anything
  security-relevant in the protected header.
- Multiple signatures: verifier decides policy (all must verify, or at least one from a trusted key).

## Detached and unencoded payload
- Detached: omit payload in transport (`header..signature`), verifier supplies it.
- RFC 7797 `"b64": false` with `"crit": ["b64"]`: payload is signed as raw bytes, not base64url. Libraries that
  ignore `crit` will compute the wrong input; reject unknown `crit` values.

## Verify
- [ ] RFC 7515 Appendix A examples pass; unprotected `alg` is ignored.

## Checked
2026-11-01. Confirmed against RFC 7515 (compact and JSON forms, signing input, flattened form, protected versus unprotected headers, Appendix A) and RFC 7797 (`b64` false, `crit`). Removed: the Open Banking header example and the RFC 7520 vectors, which were not fetched.
Method: documentation only; no commands were run.
