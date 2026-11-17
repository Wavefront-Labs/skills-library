---
id: computing-software.cryptography-implementation.key-management.generating-symmetric-keys
name: generating-symmetric-keys
category: computing-software
field: cryptography-implementation
product: key-management
tags: [cryptography-implementation, key-management, key-generation, symmetric-key-generation, sp-800-133, csprng, aes-key, hmac-key, keygen-api, passwords-are-not-keys]
level: practitioner
status: gated
description: "Generate symmetric keys per SP 800-133: full-entropy bytes from an approved RBG via the library keygen call, correct lengths, and the common ways keys end up weak."
sources: ["https://csrc.nist.gov/pubs/sp/800/133/r2/final", "https://cheatsheetseries.owasp.org/cheatsheets/Key_Management_Cheat_Sheet.html", "https://docs.python.org/3/library/secrets.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Generating symmetric keys

SP 800-133 Rev 2 section 6 ("Generation of Keys for Symmetric-Key Algorithms"): a symmetric key is the output of an approved
random bit generator (RBG), optionally combined (XOR or KDF) with other
independent key material. Anything else - passwords, timestamps, hashes of
user ids - is not a key.

## Calls that are correct

| Stack | Call |
|---|---|
| Python | `secrets.token_bytes(32)`; pyca `AESGCM.generate_key(bit_length=256)` |
| Go | `key := make([]byte, 32); rand.Read(key)` (`crypto/rand`) |
| Java | `KeyGenerator.getInstance("AES").init(256); kg.generateKey()` |
| .NET | `RandomNumberGenerator.GetBytes(32)`; `Aes.Create().GenerateKey()` |
| Node | `crypto.randomBytes(32)`; `generateKeySync('aes', {length: 256})` |
| Web Crypto | `crypto.subtle.generateKey({name:"AES-GCM",length:256}, false, [...])` |
| libsodium | `crypto_aead_xchacha20poly1305_ietf_keygen(k)` / `crypto_secretbox_keygen` |
| OpenSSL CLI | `openssl rand -out key.bin 32` |
| KMS/HSM | `GenerateDataKey`, PKCS#11 `C_GenerateKey` (key never leaves in plaintext unless asked) |

## Lengths

- AES: 256-bit default (128 is still fine classically; 256 keeps margin
  against Grover and CNSA 2.0 specifies AES-256 (gated: unconfirmed, source is paywalled or blocked)).
- HMAC-SHA-256 key: 32 bytes (>= output size; longer than the 64-byte block
  gets hashed first, no benefit).
- ChaCha20/XChaCha20: exactly 32 bytes.
- AES-SIV / XTS: double length (64 bytes for 256-bit security).

## How keys end up weak

- Generated from `random`, `Math.random`, `rand()`, `System.Random`,
  `java.util.Random` - predictable.
- Hex/base64 string of random bytes used as the key bytes directly (a 32-char
  hex string used as a 32-byte AES key has only 128 bits of entropy and a
  restricted alphabet).
- A password or passphrase used as the key; that needs a password KDF
  (Argon2id/PBKDF2) and is still only as strong as the password.
- Keys derived as `SHA256(user_id || constant)` - anyone who knows the
  constant can recompute.
- Keys generated at container build time and baked into the image, so every
  instance shares them.
- Generated on a freshly booted VM/embedded device before the kernel RNG is
  seeded (use `getrandom()` which blocks until seeded).

## Verify

- [ ] Every key generation site uses a CSPRNG-backed API listed above (grep for non-crypto RNGs).
- [ ] Key length matches the algorithm; keys are raw bytes, not encoded strings.
- [ ] No key is derived from identifiers, passwords (without a password KDF) or constants.
- [ ] Keys are generated at runtime/provisioning, not at build time.
