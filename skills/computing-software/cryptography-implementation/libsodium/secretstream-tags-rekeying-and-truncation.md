---
id: computing-software.cryptography-implementation.libsodium.secretstream-tags-rekeying-and-truncation
name: secretstream-tags-rekeying-and-truncation
category: computing-software
field: cryptography-implementation
product: libsodium
tags: [cryptography-implementation, secretstream-tags, secretstream, crypto-secretstream-xchacha20poly1305, libsodium, truncation-detection, rekey, chunked-encryption]
level: practitioner
status: docs-checked
description: "Use crypto_secretstream tags (MESSAGE, PUSH, REKEY, FINAL), detect truncation by checking for FINAL, rekey explicitly and handle headers and chunk sizes."
sources: ["https://doc.libsodium.org/secret-key_cryptography/secretstream", "https://github.com/jedisct1/libsodium/blob/master/src/libsodium/include/sodium/crypto_secretstream_xchacha20poly1305.h"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# secretstream tags, rekeying and truncation

## Tags
| Constant | Value | Meaning |
|---|---|---|
| `crypto_secretstream_xchacha20poly1305_TAG_MESSAGE` | 0 | Ordinary chunk (the most common tag) |
| `..._TAG_PUSH` | 1 | End of a set of messages, not the end of the stream (app-defined boundary) |
| `..._TAG_REKEY` | 2 | "Forget" the key used for this and earlier messages and derive a new one (the decryptor does it automatically) |
| `..._TAG_FINAL` | 3 | Last chunk; also performs an implicit rekey and marks the end of the stream |

## Push side
```c
unsigned char header[crypto_secretstream_xchacha20poly1305_HEADERBYTES];   /* 24 bytes, send before the stream */
crypto_secretstream_xchacha20poly1305_state st;
crypto_secretstream_xchacha20poly1305_init_push(&st, header, key);
/* for each chunk */
crypto_secretstream_xchacha20poly1305_push(&st, c, &clen, m, mlen, NULL, 0,
    is_last ? crypto_secretstream_xchacha20poly1305_TAG_FINAL : crypto_secretstream_xchacha20poly1305_TAG_MESSAGE);
```
Ciphertext per chunk = plaintext + `ABYTES` (17 bytes: the docs' algorithm section truncates the first block to the tag size, leaving one encrypted tag byte plus the 16-byte MAC).

## Pull side and truncation
```c
if (crypto_secretstream_xchacha20poly1305_init_pull(&st, header, key) != 0) goto bad_header;
unsigned char tag;
if (crypto_secretstream_xchacha20poly1305_pull(&st, m, &mlen, &tag, c, clen, NULL, 0) != 0) goto corrupt;
if (tag == crypto_secretstream_xchacha20poly1305_TAG_FINAL && !at_end_of_input) goto trailing_data;
/* at end of input */
if (last_tag != crypto_secretstream_xchacha20poly1305_TAG_FINAL) goto truncated;
```
The docs state that messages cannot be truncated, removed, reordered, duplicated or modified without detection, and that applications typically call `pull` in a loop until the `TAG_FINAL` message arrives. Each chunk authenticates against the state from earlier chunks, so a stream cut exactly at a chunk boundary still decrypts up to that point; **only the missing FINAL tag reveals truncation**. Always check it.

## Rekeying
- Automatic and transparent before the internal counter wraps; you do not need to count.
- `crypto_secretstream_xchacha20poly1305_rekey(&st)` updates the state without adding anything to the stream, so the decryptor must call it at exactly the same stream position; the alternative is to send `TAG_REKEY`, which the decryptor handles itself. Use either where forward secrecy is critical.

## Practical points
- Use a fixed chunk size with a smaller final chunk and store the chunk size in your file header for decoding (the docs' file example uses 4096 bytes).
- Use the per-chunk `ad` to bind file metadata to the first chunk, or bind it once via a key derived per file.
- One key per stream is fine; new random header per stream.

## Verify
- [ ] Truncating a file at a chunk boundary is reported as truncated.
- [ ] Swapping two chunks fails authentication.

## Checked

2026-10-26, libsodium documentation (libsodium-doc, master) and libsodium source at 1.0.22 era master. Confirmed: tag constants 0x00, 0x01, 0x02 (FINAL defined by expression) in the header and meanings in the docs, push and pull signatures, 24-byte header, ABYTES 17 and the truncated-first-block layout, automatic rekey, explicit rekey needing the same position on both sides, FINAL implicit rekey. Removed a fixed 64 KiB chunk recommendation and a dead anchor URL from sources.

Method: documentation only; no commands were run.
