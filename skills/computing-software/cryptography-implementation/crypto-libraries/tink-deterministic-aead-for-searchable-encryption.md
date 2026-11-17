---
id: computing-software.cryptography-implementation.crypto-libraries.tink-deterministic-aead-for-searchable-encryption
name: tink-deterministic-aead-for-searchable-encryption
category: computing-software
field: cryptography-implementation
product: crypto-libraries
tags: [tink, tink-primitives, deterministic-aead, aes-siv, tink-keyset]
level: practitioner
status: draft
description: "Use Tink DeterministicAead (AES-SIV) when equal plaintexts must give equal ciphertexts, and understand the equality leak and key template choices."
sources: ["https://developers.google.com/tink"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Tink deterministic AEAD

**Goal:** encrypt a field so you can still look it up by equality (unique constraint, join key) without storing plaintext.

## Use
```java
DeterministicAeadConfig.register();
KeysetHandle h = KeysetHandle.generateNew(KeyTemplates.get("AES256_SIV"));
DeterministicAead daead = h.getPrimitive(DeterministicAead.class);
byte[] ct = daead.encryptDeterministically(email, "users.email".getBytes(UTF_8));
byte[] pt = daead.decryptDeterministically(ct, "users.email".getBytes(UTF_8));
```
(Newer Tink releases use `RegistryConfiguration.get()` in `getPrimitive`; check your version.) Same key + same plaintext + same associated data gives the same ciphertext. Python: `tink.deterministic_aead`; Go: `daead` package.

## Rules
- Associated data binds context (table.column): different columns give different ciphertexts for the same value.
- It leaks equality and frequency. Never use it for low-cardinality values (boolean, country) or where an attacker can observe many ciphertexts and guess values. Prefer randomised AEAD plus a keyed blind index (HMAC of normalised value) when you only need exact-match lookup.
- No nonce to manage; AES-SIV is misuse-resistant, but ciphertext size is plaintext plus 16 bytes.
- Key it per purpose; rotate through the keyset (new primary key; old keys still decrypt). Re-encrypt to change values stored for lookup, because ciphertext changes with the key.
- Store keysets encrypted with a KMS key (see the Tink KMS envelope skill), never cleartext.

## Verify
Encrypting the same value twice gives identical ciphertext; a different associated data or key gives different ciphertext; tampering fails to decrypt.
