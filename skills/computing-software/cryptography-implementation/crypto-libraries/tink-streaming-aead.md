---
id: computing-software.cryptography-implementation.crypto-libraries.tink-streaming-aead
name: tink-streaming-aead
category: computing-software
field: cryptography-implementation
product: crypto-libraries
tags: [cryptography-implementation, crypto-libraries, tink, streaming-aead, large-file-encryption, aes-gcm-hkdf, segment-size, random-access-decryption, truncation-resistance]
level: advanced
status: docs-checked
description: "Encrypt large files and streams with Tink Streaming AEAD (AES-GCM-HKDF / AES-CTR-HMAC): segment sizes, associated data, random access, and why not one big AEAD call."
sources: ["https://developers.google.com/tink/streaming-aead", "https://developers.google.com/tink/streaming-aead/aes_gcm_hkdf_streaming", "https://eprint.iacr.org/2015/189"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tink Streaming AEAD

Streaming AEAD is for data too large to process in a single step, such as large files or live streams. Encryption
is done in segments bound to their location in the ciphertext, so segments cannot be removed or reordered, and a
segment from one ciphertext cannot be inserted into another. Modifying an existing ciphertext means re-encrypting
the whole stream. The scheme is loosely based on the online AE of Hoang, Reyhanitabar, Rogaway and Vizar (2015).
Decryption can work on a portion at a time, and partial plaintexts are obtainable without processing the whole
ciphertext.

## How AES-GCM-HKDF works (Tink spec)

- A random salt (the derived key size) and a 7-byte random nonce prefix go in the header; the header length is the
  first byte.
- HKDF (hash from the key) with the key value as input, the salt, and the **associated data as `info`** derives the
  per-file key. Wrong associated data therefore yields a different key and decryption fails.
- Each segment is encrypted with AES-GCM under the derived key; the IV is nonce prefix, a 4-byte big-endian segment
  index, and a final-segment flag byte (0x01 only on the last segment), with empty GCM associated data.
- The first segment is shorter by the header length; a message may have at most 2^32 segments.
- The spec warns that APIs must not let users confuse end-of-file with decryption errors, or an adversary can
  truncate files.

## Choosing a key type (Tink Streaming AEAD page)

- Tink recommends `AES128_GCM_HKDF_1MB` for most uses; `AES256_GCM_HKDF_1MB` is the same size class. The 1 MB
  variants use about 1 MB of memory while encrypting or decrypting.
- `AES128_GCM_HKDF_4KB` uses about 4 KB of memory: choose it when memory is scarce.
- `AES128_CTR_HMAC_SHA256_1MB` (or the 256-bit form) is described as the more conservative option.
- Each segment costs a 16-byte GCM tag.

## Rules

- Associated data is authenticated but NOT encrypted. Make it identify the object (path, object id, version), so a
  ciphertext moved to another object fails to decrypt.
- A decryption error can surface mid-stream: plaintext from earlier segments was authentic, but the file as a whole
  is not. Write to a temporary location and commit only after the stream closes without error.
- Streaming AEAD ciphertexts use their own format (see the Tink wire format page for AES-CTR-HMAC and
  AES-GCM-HKDF) and are not interchangeable with regular Tink AEAD output. Pick one format per data set.
- For the stream API in your language (encrypting stream, decrypting stream, seekable channels), read the Tink
  documentation for that language; this skill's earlier code samples were not verified and were removed.

## Verify

- [ ] Truncating the ciphertext by one segment causes an error at end of stream.
- [ ] Wrong associated data fails decryption.
- [ ] Consumers commit decrypted output only after a clean close.

## Checked

2026-10-28. Confirmed against the Tink Streaming AEAD page and the AES-GCM-HKDF Streaming specification page:
segment semantics, header and nonce layout, HKDF `info` = associated data, 2^32 segment limit, truncation warning,
recommended key types and memory figures, associated data not encrypted. Removed: Python and Java code, the
`AES256_GCM_HKDF_4KB` and `AES128_CTR_HMAC_SHA256_4KB` template names (the pages name only the 1MB CTR-HMAC form),
random-access sizing advice, and the libsodium and age incompatibility remark (not on these pages).
Method: documentation only; no commands were run.
