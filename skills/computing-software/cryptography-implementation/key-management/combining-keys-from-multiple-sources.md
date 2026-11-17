---
id: computing-software.cryptography-implementation.key-management.combining-keys-from-multiple-sources
name: combining-keys-from-multiple-sources
category: computing-software
field: cryptography-implementation
product: key-management
tags: [key-management, cryptography-implementation, key-combining, sp-800-133, key-generation, hybrid-keys, xor]
level: advanced
status: draft
description: "Combine key material from multiple sources per SP 800-133r2 section 6.3: XOR of independent keys, concatenate-and-KDF, and hybrid secrets so either source suffices."
sources: ["https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-133r2.pdf", "https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-56Cr2.pdf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Combining keys from multiple sources

## Approved methods (SP 800-133r2 6.3)
1. **XOR**: `K = K1 XOR K2 XOR ... XOR Kn`, each Ki the same length and generated independently. Security is at
   least that of the strongest component, if components are independent.
2. **KDF**: `K = KDF(K1 || K2 || ... , context)` with an approved KDF (SP 800-56C, SP 800-108). Works with
   unequal lengths and adds domain separation.
3. Combine a key with other secret data (e.g. a shared secret plus a PSK) via a KDF.

## Where it is used
- Split key custody: two custodians each enter a component; HSM XORs them (`key check value` per component).
- Hybrid PQ key exchange: classical and ML-KEM shared secrets concatenated into the KDF (TLS
  `X25519MLKEM768`).
- Mixing a hardware key with a software-derived key (TPM-sealed component plus passphrase-derived component).

## Rules
- Components must be independent. XORing a key with a value derived from it gives no strength.
- Never XOR keys that may be equal or attacker-chosen; use the KDF method then.
- Record key check values per component and for the result to detect entry errors.
- Wipe components after combining.

## Verify
- [ ] Ceremony log shows each component's KCV and the combined KCV.
- [ ] For hybrid schemes, confirm concatenation order matches the spec.
