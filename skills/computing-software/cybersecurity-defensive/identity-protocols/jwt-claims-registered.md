---
id: computing-software.cybersecurity-defensive.identity-protocols.jwt-claims-registered
name: jwt-claims-registered
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [jwt-claims-registered, jose-jws-jwt, jwt, rfc7519, registered-claims, numericdate, exp, nbf, jti, identity-protocols]
level: practitioner
status: docs-checked
description: "Apply the registered claims iss, sub, aud, exp, nbf, iat and jti: types, NumericDate, case sensitivity and the validation order for relying parties."
sources:
  - https://www.rfc-editor.org/rfc/rfc7519
  - https://www.rfc-editor.org/rfc/rfc8725
  - https://www.rfc-editor.org/rfc/rfc9068
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Registered JWT claims and validation

Goal: validate JWT claims the same way every time.

- `iss`: a case-sensitive StringOrURI. RFC 8725 Section 3.8: validate that the keys used belong to the issuer.
- `sub`: a StringOrURI that MUST be locally unique in the issuer's context or globally unique.
- `aud`: an array of case-sensitive strings (a single string is allowed for one audience). Each principal that processes the JWT MUST identify itself in `aud`; if it is not there the JWT MUST be rejected.
- `exp`, `nbf`, `iat`: NumericDate, a JSON number of seconds since 1970-01-01T00:00:00Z UTC. `exp`: the JWT MUST NOT be accepted on or after that time. `nbf`: the current time MUST be after or equal to it. Leeway of "usually no more than a few minutes" is allowed for clock skew.
- `jti`: a unique identifier for the JWT.

Gotchas:
- All of these claims are optional in RFC 7519; RFC 9068 makes `iss`, `exp`, `aud`, `sub`, `client_id`, `iat` and `jti` required for JWT access tokens, so require what your profile requires.
- Claim Names within a JWT Claims Set MUST be unique; parsers reject duplicates or use the last one.
- A valid signature does not mean the token is meant for you; check `iss` and `aud`.

Verify: unit test tokens that are expired, not yet valid and wrong audience.

## Checked

Date: 2026-11-02. Confirmed in RFC 7519 Section 4.1 and the NumericDate definition, RFC 8725 Section 3.8 and RFC 9068 Section 2.2 (required claims). Removed as not stated there: the 30-120 s leeway figure, the milliseconds mistake, "Aud is not aud" note.

Method: documentation only; no commands were run.
