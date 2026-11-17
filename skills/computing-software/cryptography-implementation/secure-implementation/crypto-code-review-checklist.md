---
id: computing-software.cryptography-implementation.secure-implementation.crypto-code-review-checklist
name: crypto-code-review-checklist
category: computing-software
field: cryptography-implementation
product: secure-implementation
tags: [cryptography-implementation, secure-implementation, crypto-code-review, crypto-review-checklist, security-review, threat-model, aead, key-management, pull-request-review]
level: advanced
status: docs-checked
description: "Review a pull request that touches cryptography: a checklist from threat model through algorithms, cipher modes, randomness, and key generation, rotation and storage."
sources: ["https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html", "https://cwe.mitre.org/data/definitions/310.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Crypto code review checklist

Use on any change that encrypts data at rest, generates keys or tokens, or stores keys. Ask for
the threat model first: OWASP says design should begin with who the data is being protected
against, and the right encryption layer (application, database, filesystem, hardware) depends on it.

## 1. Purpose and threat model

- [ ] Who is the data protected against? Hardware-level encryption protects against physical theft
      but not a remote compromise of the server.
- [ ] Does the change need to store the sensitive data at all? Not storing it is the best protection.
- [ ] Could a dedicated key or secrets management system (including cloud services) be used?
- [ ] Passwords use secure password hashing, not reversible encryption.

## 2. Algorithms and modes

- [ ] Symmetric encryption is AES with at least a 128-bit key (ideally 256) in a secure mode.
- [ ] Authenticated modes used where available; GCM and CCM are the first preference.
- [ ] If only CTR or CBC is available, separate authentication such as Encrypt-then-MAC is present
      (take care with variable-length messages).
- [ ] ECB is not used outside very specific circumstances.
- [ ] No custom algorithms.
- [ ] RSA, where unavoidable, uses at least 2048-bit keys and RSAES-OAEP (RFC 8017 section 7.1);
      never RSA without an encryption padding scheme.
- [ ] Public-key encryption uses a maintained library implementing an established hybrid scheme
      such as HPKE; X25519 alone does not encrypt data.
- [ ] Long-lived confidentiality needs consider post-quantum exposure of RSA and ECC.

## 3. Randomness

- [ ] Keys, IVs, session IDs and tokens come from a CSPRNG, not a general PRNG. OWASP's table
      lists, for example, `getrandom(2)` in C, `java.security.SecureRandom`, Python `secrets`,
      Go `crypto/rand` and Node `crypto.randomBytes()` as secure, and `rand()`,
      `Math.random()`, Python `random()` and Go `math/rand` as unsafe.
- [ ] UUIDs are not relied on for randomness unless the implementation is known to be secure.

## 4. Keys

- [ ] Generated with a CSPRNG, not based on words or typed characters; independent keys where
      several are used.
- [ ] Not hard-coded or checked into version control; configuration files holding keys have
      restrictive permissions; environment variables are discouraged.
- [ ] Stored in an HSM, key vault or secrets service where available.
- [ ] Rotation process exists before it is needed: re-encrypt old data, or tag items with a key ID
      and keep old keys; the algorithm or library can also be changed.
- [ ] Rotation criteria defined: compromise, cryptoperiod, mode usage limits, algorithm weakness.
- [ ] Keys stored apart from the data; DEK/KEK separation where possible, KEK at least as strong
      as the DEK.

## 5. Defence in depth

- [ ] The system stays secure if the crypto control fails: access control is enforced, and
      encrypted URL parameters are not relied on.

Escalate to a specialist reviewer for custom protocols, new primitives or anything this
checklist cannot answer.

## Checked

Method: docs-checked 2026-11-09 against the OWASP Cryptographic Storage Cheat Sheet (full page) and CWE-310 (category page, read in part). Removed: the Schneier book and Latacora sources (not readable), nonce uniqueness, AAD binding, canonical serialization, constant-time comparison, known-answer and Wycheproof test items, Argon2id/scrypt/bcrypt/PBKDF2 and signature algorithm preferences, HKDF subkey labels, and decrypt-failure metrics, none of which the read sources state.
