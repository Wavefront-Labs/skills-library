---
id: computing-software.cryptography-implementation.libsodium.authenticated-encryption-and-signatures
name: authenticated-encryption-and-signatures
category: computing-software
field: cryptography-implementation
product: libsodium
tags: [cryptography-implementation, libsodium, nacl, pynacl, libsodium-js, secretbox, xchacha20-poly1305, aead, crypto-box, sealed-box, x25519, key-exchange, crypto-kx, ed25519, signatures, argon2id, password-hashing, crypto-pwhash, secretstream, file-encryption, nonce, sodium-memzero, sodium-mlock, authenticated-encryption]
level: practitioner
status: verified
description: "Using libsodium correctly: secretbox and XChaCha20-Poly1305 AEAD, crypto_box and sealed boxes, crypto_kx, Ed25519 signing, Argon2id pwhash, secretstream for files, memory hygiene, bindings."
sources: ["https://doc.libsodium.org/", "https://pynacl.readthedocs.io/", "https://github.com/jedisct1/libsodium.js", "https://www.rfc-editor.org/rfc/rfc9106", "https://www.rfc-editor.org/rfc/rfc8032"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# libsodium: authenticated encryption, boxes, signatures and password hashing

**Goal:** pick the right libsodium API for the job and call it in a way that cannot
silently go wrong: random nonces that are actually safe, every return code checked,
secrets wiped.

## 0. Initialise and check every return
```c
if (sodium_init() < 0) abort();   /* 0 = ok, 1 = already initialised, -1 = failure */
```
Every `*_open`, `*_decrypt` and `*_verify` returns `-1` on forgery. Treat that as a
hard failure and never use the output buffer afterwards. Keys come from `*_keygen()`
or `randombytes_buf()`, never from `rand()`.

## 1. Which API?
| Need | API | Key / nonce / overhead |
|---|---|---|
| Encrypt with a shared key | `crypto_aead_xchacha20poly1305_ietf_*` (or `crypto_secretbox_easy`) | 32 B key, 24 B nonce, 16 B tag |
| Encrypt to a known recipient, sender authenticated | `crypto_box_easy` | X25519 key pairs, 24 B nonce |
| Anonymous "drop box" to a public key | `crypto_box_seal` | 48 B overhead (ephemeral pk + tag) |
| Derive session keys between two parties | `crypto_kx_client_session_keys` / `_server_` | gives separate rx and tx keys |
| Sign / verify | `crypto_sign_detached` / `crypto_sign_verify_detached` | Ed25519, 64 B sig, 64 B secret key |
| Password storage or password-to-key | `crypto_pwhash_str` / `crypto_pwhash` | Argon2id |
| Large files or streams | `crypto_secretstream_xchacha20poly1305_*` | 24 B header, 17 B per chunk |

## 2. AEAD with a random nonce
The 24-byte (192-bit) nonce in XChaCha20 and XSalsa20 (secretbox) is big enough that
`randombytes_buf` can generate a fresh one per message without a realistic collision
risk. The 12-byte `chacha20poly1305_ietf` and `aes256gcm` variants are **not** safe
with random nonces at volume, so prefer the X variant.
```c
unsigned char key[crypto_aead_xchacha20poly1305_ietf_KEYBYTES];
unsigned char nonce[crypto_aead_xchacha20poly1305_ietf_NPUBBYTES];
crypto_aead_xchacha20poly1305_ietf_keygen(key);
randombytes_buf(nonce, sizeof nonce);
crypto_aead_xchacha20poly1305_ietf_encrypt(c, &clen, m, mlen, ad, adlen, NULL, nonce, key);
/* send nonce || c ; on receive: */
if (crypto_aead_xchacha20poly1305_ietf_decrypt(m, &mlen, NULL, c, clen, ad, adlen, nonce, key) != 0)
    reject();
```
Put context (record id, version, user id) in `ad` so a ciphertext cannot be
pasted into another record.

## 3. Boxes and key exchange
`crypto_box_easy(c, m, mlen, nonce, recipient_pk, sender_sk)` authenticates the
sender to the recipient only. Either party could forge the other's messages, so it is
not a signature. `crypto_box_seal` does not authenticate the sender at all.
`crypto_kx_*_session_keys` returns `-1` for an unacceptable peer key and gives
distinct rx/tx keys for a channel.

## 4. Signatures
`crypto_sign_detached(sig, NULL, m, mlen, sk)`, then
`crypto_sign_verify_detached(sig, m, mlen, pk) != 0` means reject. `sk` is 64 bytes
(seed plus public key); to store only 32 bytes, keep the seed (`crypto_sign_seed_keypair`).

## 5. Password hashing (Argon2id)
```c
char out[crypto_pwhash_STRBYTES];
crypto_pwhash_str(out, pw, pwlen, crypto_pwhash_OPSLIMIT_INTERACTIVE, crypto_pwhash_MEMLIMIT_INTERACTIVE);
crypto_pwhash_str_verify(out, pw, pwlen);          /* 0 = match */
crypto_pwhash_str_needs_rehash(out, ops, mem);     /* upgrade parameters on login */
```
For Argon2id the presets are INTERACTIVE = 2 passes / 64 MiB,
MODERATE = 3 / 256 MiB, SENSITIVE = 4 / 1 GiB (read from libsodium.js 1.0.22 constants). The `_str` output encodes the algorithm, salt and parameters, so store it
as-is. For key derivation, `crypto_pwhash` with a random `crypto_pwhash_SALTBYTES`
(16 B) salt that you store next to the ciphertext. Benchmark on your servers: 1 GiB
per login can exhaust memory.

## 6. Files: secretstream
`init_push` writes a 24-byte header. Push fixed-size chunks (for example 64 KiB) with
`crypto_secretstream_xchacha20poly1305_TAG_MESSAGE`, and the last one with `TAG_FINAL`.
On pull, **reject if the stream ends before a chunk tagged FINAL** arrives. Without
that check, a truncated file decrypts "successfully". Reordered or dropped chunks are
detected.

## 7. Memory hygiene
`sodium_memzero` (the compiler cannot remove it), `sodium_mlock`/`sodium_munlock`
(keeps secrets out of swap, subject to RLIMIT_MEMLOCK), and `sodium_malloc` (guard
pages, slower, for long-lived keys). Compare secrets with `sodium_memcmp`, not `memcmp`.

## 8. Bindings
- **PyNaCl:** `nacl.secret.SecretBox(key).encrypt(msg)` generates and prepends the
  nonce for you; see also `nacl.public.SealedBox`,
  `nacl.signing.SigningKey` and `nacl.pwhash.argon2id.str()`.
- **libsodium.js** (`libsodium-wrappers`): `await sodium.ready` before any call, then
  `sodium.crypto_secretbox_easy(msg, nonce, key)` with
  `sodium.randombytes_buf(sodium.crypto_secretbox_NONCEBYTES)`. Some less common
  functions only ship in `libsodium-wrappers-sumo`.

## Gotchas
- `crypto_aead_aes256gcm_*` only works where the CPU has hardware AES. Call
  `crypto_aead_aes256gcm_is_available()` first, or just use XChaCha.
- Generate separate signing and X25519 keys rather than converting Ed25519 keys.
- Define and version your own wire format (`version || nonce || ciphertext`).

## Verify
- [ ] `sodium_init()` is checked, and every open/decrypt/verify result is checked.
- [ ] Each encryption gets a new nonce from `randombytes_buf` (or a counter in a stream).
- [ ] Flipping one ciphertext bit makes decryption fail, as a test.
- [ ] Truncating a secretstream file is detected (no FINAL tag).
- [ ] Password hashes use `_str` with measured limits, and `needs_rehash` is wired in.
