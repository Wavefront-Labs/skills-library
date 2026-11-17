---
id: computing-software.cryptography-implementation.applied-cryptography.key-derivation-and-domain-separation
name: key-derivation-and-domain-separation
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [cryptography-implementation, applied-cryptography, hkdf, kdf, domain-separation, context-binding, key-reuse, subkeys, rfc5869, salt, info-parameter, multi-purpose-keys, cross-protocol-attacks]
level: advanced
status: docs-checked
description: "Deriving separate subkeys from one master secret with HKDF: extract/expand, info binding for domain separation, and when not to skip extract."
sources: ["https://www.rfc-editor.org/rfc/rfc5869.txt", "https://www.rfc-editor.org/rfc/rfc8446.txt"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Key derivation and domain separation

Rule: never use one key for two cryptographic purposes. Derive an independent key per purpose
from the master secret with HKDF (RFC 5869).

## HKDF has two stages

- **Extract:** `HKDF-Extract(salt, IKM) -> PRK`. The salt is optional (it defaults to a string of
  HashLen zeros). Extract turns input keying material that is not uniformly random into a PRK.
- **Expand:** `HKDF-Expand(PRK, info, L) -> OKM`. Expands the PRK into L bytes of output.
- RFC 5869 section 3.3: if IKM is already a cryptographically strong key, Extract may be skipped
  and IKM used directly as the HMAC key in Expand. If IKM is a Diffie-Hellman value, Extract
  SHOULD NOT be skipped, because g^xy is not a uniformly random string; apply Extract
  (preferably with a salt) and use the PRK for Expand.
- Using the PRK directly as OKM when L <= HashLen is NOT RECOMMENDED, partly because it omits
  `info`.

## Domain separation via info

RFC 5869 section 3.2: `info` is optional in the definition but often of great importance. It binds
the derived key material to application and context data (protocol number, algorithm identifiers,
user identities and so on) and can prevent the same keying material being derived for different
contexts from the same IKM. Technical requirement: `info` should be independent of IKM.

```
enc_key  = HKDF-Expand(PRK, info="myapp v1 encryption-key", L=32)
mac_key  = HKDF-Expand(PRK, info="myapp v1 mac-key",        L=32)
```

(The info strings above are illustrative, not from the RFC.)

- Make `info` unique per purpose, and include a protocol or version marker so keys for different
  versions differ.
- TLS 1.3 (RFC 8446 section 7.1) builds on HKDF with `HKDF-Expand-Label`, whose HkdfLabel struct
  carries the output length, a label prefixed with "tls13 " and a context. Derive-Secret passes
  the transcript hash as context. Handshake traffic secrets use labels such as "c hs traffic"
  and "s hs traffic", giving separate client and server keys. Your protocol need not copy the
  wire format, only the separation discipline.
- If you build `info` from several fields, delimit them unambiguously (own advice, not from the
  RFC) so different field splits cannot give the same string.

## Common mistakes

- Using the master secret directly as a key, then needing a second key later.
- The same `info` for different purposes, which returns identical keys.
- Feeding a low-entropy secret such as a password to HKDF expecting brute-force resistance. HKDF
  is not designed for that; use a password-hashing KDF first.
- Skipping Extract on a Diffie-Hellman shared secret (see above).

## Verify

- [ ] Every purpose (encrypt, MAC, sign) has its own subkey.
- [ ] Every subkey's `info` is unique and carries a protocol or version marker.
- [ ] DH secrets and other non-uniform IKM go through Extract before Expand.
- [ ] No password goes straight into HKDF.

## Checked
Method: docs-checked 2026-11-09 against RFC 5869 (sections 3.2 and 3.3, downloaded text) and RFC 8446 (section 7.1 HKDF-Expand-Label and Derive-Secret, with the "c hs traffic" and "s hs traffic" labels, downloaded text). Removed the soatok blog source (not read), the claim that truncation of Expand output is safe by construction, and the Argon2id/scrypt specifics.
