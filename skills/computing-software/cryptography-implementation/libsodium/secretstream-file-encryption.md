---
id: computing-software.cryptography-implementation.libsodium.secretstream-file-encryption
name: secretstream-file-encryption
category: computing-software
field: cryptography-implementation
product: libsodium
tags: [cryptography-implementation, libsodium, crypto-secretstream, secretstream, chunked-encryption, file-encryption, streaming-encryption, truncation-attack, tag-final, tag-rekey, chunk-size, memory-hygiene]
level: advanced
status: docs-checked
description: "Implementing file/stream encryption with libsodium's crypto_secretstream correctly: chunk-size trade-offs, the tag types, truncation-attack prevention via TAG_FINAL, and rekeying."
sources: ["https://doc.libsodium.org/secret-key_cryptography/secretstream", "https://github.com/jedisct1/libsodium/blob/master/src/libsodium/include/sodium/crypto_secretstream_xchacha20poly1305.h"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# secretstream for chunked file and stream encryption

`crypto_secretstream` exists because a single `secretbox`/AEAD call must
hold the entire plaintext in memory at once — not viable for large files or
true streams (network sockets, pipes). secretstream splits data into
authenticated chunks while preserving AEAD-level security *and* adding
guarantees plain "encrypt each chunk separately" would not have on its own.

## Why "just AEAD-encrypt each chunk" isn't enough on its own

If you naively split a file into chunks and AEAD-encrypt each one
independently (even with a unique nonce per chunk), you get confidentiality
and per-chunk integrity, but **not stream-level integrity**: an attacker who
can reorder, drop, duplicate, or truncate chunks in the ciphertext stream
isn't detected, because each chunk still authenticates correctly on its own
— nothing ties a chunk to its *position* in the sequence. secretstream's
internal state chains each chunk to the chunks before it (the nonce is updated from each chunk's MAC), and the docs state that messages cannot be truncated, removed, reordered, duplicated or modified without the decryption functions detecting it, provided the application reads until the `TAG_FINAL` message.

## Chunk size: a real trade-off, not a fixed constant

There's no single mandated chunk size — pick one that balances:
- **Memory:** your choice bounds per-chunk RAM for buffering; too large
  defeats the point of streaming (why you're not just using one `secretbox`
  call), too small adds per-chunk overhead (each chunk carries its own MAC
  tag — `crypto_secretstream_xchacha20poly1305_ABYTES`, 17 bytes, per chunk) and more function-call
  overhead.
- **Latency/granularity:** smaller chunks let you process (e.g., forward
  over a network, write to disk) data sooner, before the whole stream has
  arrived — relevant for truly live streaming, not just "a big file I have
  entirely on disk already."
- **Reference point:** the docs' file-encryption example uses a 4096-byte chunk (`CHUNK_SIZE`); benchmark for your own throughput target. Each message can be up to `crypto_secretstream_xchacha20poly1305_MESSAGEBYTES_MAX` (about 256 GB).

## The tag types, and why `TAG_FINAL` is not optional

Each chunk is pushed with a tag: `TAG_MESSAGE` (normal, more chunks follow),
`TAG_FINAL` (this is the last chunk of the stream), `TAG_PUSH` (the end of a set of messages, such as a large JSON string sent in chunks,
without ending the stream), or
`TAG_REKEY` ("forget" the key and derive a new one, covered
below). Tags are encrypted, so a stream does not reveal PUSH or REKEY boundaries.

**`TAG_FINAL` is the mechanism that prevents truncation attacks.** Without
it, an attacker who truncates the ciphertext stream (deletes the last N
chunks before the recipient reads them) produces a stream that decrypts
"successfully" as far as it goes — every chunk still authenticates — but is
silently incomplete, which for many file formats is indistinguishable from
a legitimately short file. Pushing `TAG_FINAL` on the genuine last chunk
means the decryptor's pull loop can check "did I actually reach a chunk
tagged FINAL, or did the stream just end" and **reject a stream that ends
without ever seeing TAG_FINAL** as tampered/truncated. Skipping this check
on the decrypt side (treating EOF-without-FINAL the same as a clean finish)
reopens the exact truncation vulnerability secretstream was designed to
close — this is the most common implementation mistake with this API.

## Rekeying for very long-lived streams

Rekeying happens automatically before the internal counter wraps, so streams can be arbitrarily large. `TAG_REKEY` (or calling `crypto_secretstream_xchacha20poly1305_rekey` at the same stream position on both sides) triggers an explicit rekey for applications where forward secrecy is critical; the decryptor updates the key automatically when it sees the tag. A `TAG_FINAL` also performs an implicit rekey. Most file-encryption use cases
don't need explicit rekeying.

## Header handling

secretstream's `crypto_secretstream_xchacha20poly1305_init_push` produces a
header (`crypto_secretstream_xchacha20poly1305_HEADERBYTES`, 24 bytes, not secret) that must be transmitted/stored before the stream and fed into
`_init_pull` on the decrypt side; the docs say decryption with a different header fails, and `init_pull` returns -1 for an invalid header (it seeds the
stream's internal state). Store it as a fixed-size prefix of the output file
or the first message of the stream, and treat its integrity as part of
"don't lose the ciphertext," not as a separate lower-priority concern.

## Verify

- [ ] Chunk size chosen with an explicit memory/latency trade-off reasoning,
      not an arbitrary copy-pasted constant.
- [ ] The genuine last chunk is pushed with `TAG_FINAL`.
- [ ] The decrypt/pull loop explicitly checks that `TAG_FINAL` was received
      and treats EOF-without-FINAL as a tampering/truncation error, not a
      normal end of stream.
- [ ] The stream header is stored/transmitted reliably alongside the
      ciphertext and never dropped.
- [ ] `TAG_REKEY` is used (or deliberately not used, with that choice
      documented) based on whether within-session forward secrecy is a
      requirement.

## Checked

2026-10-26, libsodium documentation (libsodium-doc, master) and libsodium source at 1.0.22 era master. Confirmed: tag meanings (MESSAGE 0, PUSH, REKEY, FINAL) and values from the header, tags encrypted, FINAL erases the key and rekeys implicitly, automatic and explicit rekeying including crypto_secretstream_xchacha20poly1305_rekey, 24-byte header with init_pull returning -1 for an invalid header, ABYTES 17, message limit about 256 GB, 4096-byte chunk in the docs example, the stream-integrity statement. Removed unconfirmed chunk-size ranges and a dead gitbook source URL.

Method: documentation only; no commands were run.
