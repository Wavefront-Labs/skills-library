---
id: computing-software.cryptography-implementation.protocol-implementation.paseto-and-jwt-alternatives
name: paseto-and-jwt-alternatives
category: computing-software
field: cryptography-implementation
product: protocol-implementation
tags: [protocol-implementation, cryptography-implementation, paseto, jwt-alternatives, tokens, jose]
level: advanced
status: docs-checked
description: "Evaluate PASETO as a JWT alternative: versioned protocols, v4.local and v4.public construction, v3 for NIST algorithms, footers and implicit assertions."
sources: ["https://github.com/paseto-standard/paseto-spec", "https://github.com/paseto-standard/paseto-spec/blob/master/docs/01-Protocol-Versions/Version4.md", "https://github.com/paseto-standard/paseto-spec/blob/master/docs/01-Protocol-Versions/Version3.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PASETO and JWT alternatives

## PASETO (spec README and version documents)

- Instead of JWT algorithm agility (including `none`, and the RS256-to-HS256
  confusion that forges tokens using the public key as an HMAC key), PASETO
  gives a `version` and a `purpose`.
- Purposes: `local` (shared-key AEAD encryption) and `public` (public-key
  signature). Only authenticated modes are allowed. The header and optional
  footer are covered by the signature or authentication tag.
- `v4.local.`: 32-byte key, 32 random bytes of nonce `n`; BLAKE2b keyed
  derivation of encryption key, counter nonce and authentication key; XChaCha20
  encryption; BLAKE2b MAC over PAE of header, nonce, ciphertext, footer and
  implicit assertion. Token is `h || base64url(n || c || t)`, plus
  `.base64url(footer)` when a footer is present.
- `v4.public.`: Ed25519 detached signature over the PAE-packed message.
- `v3.local.`: AES-256-CTR with HMAC-SHA384 and HKDF-HMAC-SHA384 key
  derivation; `v3.public.` uses 384-bit ECDSA.
- Footer: always cleartext (base64url) but authenticated. A decryptor MAY
  compare it to an expected value using a constant-time compare.
- Implicit assertion: an optional input bound into the MAC or signature but
  not carried in the token.
- Before use, assert the key is intended for that version and purpose, and for
  `local` is 32 bytes.
- Caution from the README: neither JWT nor PASETO was designed for stateless
  session management; PASETO cannot prevent replay by itself.
- Test vectors live in the paseto-standard/test-vectors repository. Key
  serialisation and wrapping is the PASERK extension.

## Choosing

JWT remains the choice where an ecosystem requires it; this skill does not
cover OAuth or OIDC interop, so decide that against your relying parties.

## Verify

- [ ] The library implements the version you use and passes the official test vectors.
- [ ] Keys are bound to a version and purpose and checked before use.

## Checked

Method: docs-checked 2026-11-09 against paseto-spec README, Version4.md and Version3.md. Removed: Biscuit and Macaroons descriptions and sources (biscuitsec.org docs page unreadable, Macaroons paper not read), opaque-token advice, library names, migration-by-prefix advice, the "kid in footer" suggestion, and the OAuth/OIDC interop and JWT hardening claims.
