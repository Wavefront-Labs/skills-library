---
id: computing-software.cryptography-implementation.libsodium.generic-hashing-and-key-derivation
name: generic-hashing-and-key-derivation
category: computing-software
field: cryptography-implementation
product: libsodium
tags: [cryptography-implementation, libsodium, crypto-generichash, blake2b, crypto-kdf, crypto-shorthash, keyed-hashing, hmac, subkeys, domain-separation, siphash, content-addressing, checksum, crypto-kdf-derive]
level: practitioner
status: docs-checked
description: "libsodium's hashing/KDF functions beyond AEAD and signatures: crypto_generichash (BLAKE2b, keyed or not), crypto_kdf for subkeys, and crypto_shorthash — what each is actually for."
sources: ["https://doc.libsodium.org/hashing/generic_hashing", "https://doc.libsodium.org/key_derivation", "https://doc.libsodium.org/hashing/short-input_hashing"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# libsodium generic hashing and key derivation

This product's existing skill covers AEAD and signatures; libsodium also
ships three smaller, frequently-misused primitives that solve different
problems — picking the wrong one of the three is the common mistake this
skill addresses.

## `crypto_generichash` (BLAKE2b) — unkeyed vs keyed mode

`crypto_generichash` is BLAKE2b, usable two ways:
- **Unkeyed:** a general-purpose cryptographic hash — content addressing,
  checksums, fingerprinting data for dedup/integrity. Output size is
  configurable (`crypto_generichash_BYTES_MIN` to `_MAX`, 16 to 64 bytes; `crypto_generichash_BYTES` is 32).
  The libsodium docs present it as a faster and more secure alternative to MD5 and SHA-1, and it
  is the natural default inside a libsodium-based codebase.
- **Keyed:** passing a secret key turns it into a **keyed MAC**, functionally
  similar to HMAC but using BLAKE2b's native keying rather than the
  HMAC construction (the docs note it is safe against the length-extension attacks that affect
  MD5, SHA-1 and SHA-256, and that a keyed hash can be used as a PRF). Use keyed mode when you need a MAC and don't specifically
  need HMAC-SHA256 for interop with a system that expects that exact
  construction.
- **Common mistake:** using unkeyed `crypto_generichash` for a security
  purpose that actually needs authentication (checking data wasn't tampered
  with by an adversary who can also recompute an unkeyed hash) — an unkeyed
  hash proves integrity against *accidental* corruption, not against a
  deliberate adversary, who can simply recompute the same hash over tampered
  data. If the threat model includes a malicious party, you need the keyed
  variant (or a full AEAD construction) — see
  `computing-software.cryptography-implementation.applied-cryptography.choosing-primitives-and-modes`
  for the MAC-vs-hash decision in general.

## `crypto_kdf` — deriving numbered subkeys from one master key

`crypto_kdf_derive_from_key(subkey, subkey_len, subkey_id, context, master_key)`
derives one of potentially many subkeys from a single master key, indexed by
a 64-bit `subkey_id` and an 8-byte `context` string. This is libsodium's
purpose-built tool for exactly the domain-separation problem covered in
`computing-software.cryptography-implementation.applied-cryptography.key-derivation-and-domain-separation`
(which uses HKDF generically) — `crypto_kdf` is the libsodium-native,
slightly more constrained version (fixed-width context, numeric subkey id
instead of an arbitrary `info` string), convenient when you're already
inside the libsodium ecosystem and want subkey derivation without pulling
in a separate HKDF call.
- The `context` string is only 8 characters — too short to encode a rich
  "protocol v1 encryption key" style label. Use the numeric `subkey_id` for
  the common case (key #1, key #2, ...) and reserve `context` for a short
  fixed tag identifying the *application*, not the specific purpose; if you
  need richer context binding, use HKDF directly instead of forcing it into
  8 bytes.
- `master_key` for `crypto_kdf` must itself be uniformly random (generated
  with `crypto_kdf_keygen` or an equivalent CSPRNG draw) — like HKDF, this
  is a key *expander*, not a password hardener; don't feed it a password.

## `crypto_shorthash` (SipHash) — the one that's not for security integrity

`crypto_shorthash` is a short-input, short-output (64-bit) keyed hash
designed for **hash-table/hash-flooding DoS resistance** (this is exactly
SipHash's original motivating use case — protecting hash table bucket
selection from adversarial inputs designed to cause worst-case collision
behavior), not for general cryptographic integrity or as a MAC substitute.
The libsodium docs state the 64-bit output should not be considered collision-resistant, and that the
DoS protection only holds while the key stays secret. Reaching for `crypto_shorthash` where you actually need
`crypto_generichash`'s keyed mode is the specific mistake this function's
name invites.

## Verify

- [ ] Unkeyed `crypto_generichash` is used only where the threat model is
      accidental corruption, not deliberate tampering; keyed mode (or AEAD)
      is used wherever an adversary is in scope.
- [ ] `crypto_kdf` master keys are CSPRNG-generated, never derived from a
      password or other low-entropy source.
- [ ] Subkey derivation uses a distinct `subkey_id`/`context` combination per
      purpose — no accidental reuse across two different subkeys' roles.
- [ ] `crypto_shorthash` is used only for hash-table/DoS-resistance purposes,
      never as a MAC or integrity check on security-relevant data.

## Checked

2026-10-26, libsodium documentation (libsodium-doc, master) and libsodium source at 1.0.22 era master. Confirmed: generichash output range 16 to 64 bytes with default 32 (blake2b header), keyed mode and key sizes, length-extension statement, crypto_kdf 8-character context and 64-bit subkey id, crypto_kdf_keygen, shorthash as SipHash-2-4 with 64-bit output, not collision-resistant, key must stay secret. Removed an unconfirmed software-speed claim, a forgery-cost estimate and the BLAKE2 design-intent remark.

Method: documentation only; no commands were run.
