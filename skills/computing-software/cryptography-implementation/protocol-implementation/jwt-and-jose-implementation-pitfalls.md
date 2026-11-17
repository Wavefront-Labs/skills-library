---
id: computing-software.cryptography-implementation.protocol-implementation.jwt-and-jose-implementation-pitfalls
name: jwt-and-jose-implementation-pitfalls
category: computing-software
field: cryptography-implementation
product: protocol-implementation
tags: [cryptography-implementation, protocol-implementation, jwt, jose, jws, jwk, alg-none, algorithm-confusion, jku, x5u, kid-injection, hs256, rs256, exp-validation, token-validation, rfc8725]
level: advanced
status: docs-checked
description: "JWT/JOSE pitfalls beyond 'use a library': algorithm confusion (alg=none, RS256/HS256), header key injection (jku/jwk/x5u/kid), and claim validation."
sources: ["https://www.rfc-editor.org/rfc/rfc7519", "https://www.rfc-editor.org/rfc/rfc7515", "https://www.rfc-editor.org/rfc/rfc8725"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# JWT/JOSE implementation pitfalls

JWTs are a signed-data format, and nearly every real-world JWT
vulnerability is a **verification-side implementation bug**, not a flaw in
the underlying signature algorithm. This is the checklist that catches
them, complementary to the general `tls-integration-and-certificate-validation`
skill's "don't let the protocol negotiate down" theme.

## `alg: none` and algorithm confusion

- **`alg: none`:** the JOSE spec defines an explicit "none" algorithm
  (unsecured JWS) for legitimate non-cryptographic use. If your verifier
  reads the `alg` header from the **untrusted token itself** and dispatches
  verification logic based on it, an attacker can simply set `alg: none`,
  omit a signature, and have a naive verifier accept it as valid. **The
  verifier must pin the expected algorithm(s) itself** (from server-side
  configuration, not from the incoming token) and reject any token whose
  header doesn't match — never let the token tell the verifier how to
  verify itself.
- **RS256/HS256 key confusion:** a classic attack when a server signs with
  RS256 (RSA, asymmetric) and publishes the corresponding RSA *public* key
  for verification. If the verifier is misconfigured to accept whatever
  `alg` the token header claims, an attacker crafts a token with
  `alg: HS256` and uses the **public key's bytes as the HMAC secret** — a
  verifier that blindly treats "the key configured for this `kid`" as an
  HMAC secret when the token says HS256 will accept this forged token,
  because HMAC verification with the (public, known) RSA key bytes as the
  shared secret succeeds. Fix is the same as above: pin the expected
  algorithm server-side per key/use case, never derive it from the token.

## Header-based key injection — don't trust `jku`, `jwk`, or `x5u`

JOSE headers can optionally carry `jku` (a URL to fetch the verification
key set), `jwk` (the verification key embedded directly in the header), or
`x5u` (a URL to fetch an X.509 cert chain). **All three let an attacker
supply their own key for the verifier to use**, if the verifier naively
follows them:
- `jwk` embedded in the header: an attacker signs a token with their own
  keypair and embeds their own public key directly in the `jwk` header. A
  verifier that extracts the verification key from the token's own header
  (instead of looking it up independently by `kid` against a trusted key
  store) will "successfully" verify a token signed by an attacker-controlled
  key.
- `jku`/`x5u`: same attack via a URL the attacker controls, if the verifier
  fetches and trusts whatever key set that URL serves instead of validating
  the URL against an allow-list of trusted issuers.
- **Rule:** never resolve the verification key from attacker-controlled
  header fields. Look up the key by `kid` against your own trusted,
  server-side key store (a JWKS endpoint you've pre-registered and
  allow-listed, not one named in the token). If you must support `jku`,
  validate it against a strict allow-list of trusted origins before
  fetching.

## Claim validation — signature valid is not the same as token valid

A cryptographically valid signature only proves the token wasn't tampered
with by someone lacking the key; it says nothing about whether the token
should still be honored:
- **`exp` (expiry) and `nbf` (not-before)** must be explicitly checked
  against current time by the verifier — some libraries do this
  automatically, some require an explicit call; confirm which for your
  library rather than assuming.
- **`aud` (audience) and `iss` (issuer)** must be checked against the
  expected values for your service — a token legitimately issued for a
  *different* service/audience by the same issuer should not be accepted
  just because the signature is valid (this is the cross-service replay
  problem, same family as the signature cross-purpose issue in
  `computing-software.cryptography-implementation.applied-cryptography.signature-scheme-pitfalls`).
- **Clock skew tolerance:** RFC 7519 allows a small leeway (usually no more
  than a few minutes) on `exp`/`nbf` checks to absorb clock drift between issuer and verifier,
  but keep it small and explicit — a large or absent tolerance either
  breaks legitimate edge cases or meaningfully extends a token's effective
  lifetime beyond what was intended.

## Verify

- [ ] The verifier pins the expected algorithm(s) from server-side config,
      never from the incoming token's `alg` header.
- [ ] `alg: none` is explicitly rejected (unless the "none" use case is a
      deliberate, documented part of the design, which is rare).
- [ ] The verification key is looked up by `kid` against a trusted
      server-side key store — `jwk`/`jku`/`x5u` header values are never
      trusted directly, or `jku` is checked against a strict allow-list.
- [ ] `exp`, `nbf`, `aud`, and `iss` are all explicitly validated, with a
      small, deliberate clock-skew tolerance.
- [ ] Token validation logic has been tested against known JWT attack
      payloads (alg=none, key-confusion), not just the happy path.
- [ ] The `kid` value is validated before use in any lookup (RFC 8725 warns of SQL/LDAP injection), and `jku`/`x5u`
      fetches match an allow-list and send no cookies (SSRF).

## Checked
2026-11-01. Confirmed against RFC 8725 (sections 2.1, 3.1, 3.2, header handling for kid, jku, x5u, typ) and RFC 7519
(exp, nbf, aud, iss and the leeway wording). Removed: the 30 to 120 second skew figure, the vendor blog sources, and
the unverified statement about library defaults (check your library's documentation).
Method: documentation only; no commands were run.
