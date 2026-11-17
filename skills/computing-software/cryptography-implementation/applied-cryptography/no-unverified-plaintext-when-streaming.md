---
id: computing-software.cryptography-implementation.applied-cryptography.no-unverified-plaintext-when-streaming
name: no-unverified-plaintext-when-streaming
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [cryptography-implementation, applied-cryptography, aead, streaming-encryption, aes-gcm, chunked-aead, secretstream, tink]
level: advanced
status: docs-checked
description: "Encrypt large files or streams in authenticated segments with libsodium secretstream or Tink Streaming AEAD, and what each guarantees."
sources: ["https://doc.libsodium.org/secret-key_cryptography/secretstream", "https://developers.google.com/tink/streaming-aead"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Streaming AEAD for large data

When data is too large to process in one step (large files, live streams), encrypt it in authenticated segments so each
segment can be checked as it is decrypted, instead of one tag at the very end.

## libsodium secretstream (XChaCha20-Poly1305)
- Encrypts a sequence of messages, or one message split into any number of chunks, under a secret key.
- Messages cannot be truncated, removed, reordered, duplicated or modified without the decryption functions detecting it.
- Each message can include additional data (for example a timestamp or protocol version) in its authentication tag.
- It generates nonces transparently and handles key rotation automatically.
- Flow: `crypto_secretstream_xchacha20poly1305_keygen` makes the key; `init_push` creates the stream state and a header;
  `push` encrypts each chunk, with `TAG_FINAL` on the last chunk; the receiver calls `init_pull` with the header and key (a
  non-zero return means an invalid header, so stop) and then `pull` per chunk. The ciphertext of each chunk is longer than
  its message by `crypto_secretstream_xchacha20poly1305_ABYTES`.
- Check the tag returned by `pull`: a real application checks for the final tag rather than just running out of data.

## Tink Streaming AEAD
- Encryption is in segments bound to their location in the ciphertext; segments cannot be removed or reordered, and
  segments from one ciphertext cannot be inserted into another. Modifying existing ciphertext means re-encrypting the whole
  stream (this also prevents roll-back attacks).
- Decryption authenticates only a portion at a time, so partial plaintexts can be read without processing the whole
  ciphertext.
- Tink recommends AES128_GCM_HKDF_1MB for most uses (about 1 MB of memory); AES128_GCM_HKDF_4KB (about 4 KB of memory)
  suits low-memory systems; the AES-CTR-HMAC-SHA256 key types are the more conservative option.
- Associated data is authenticated but not encrypted. Tying a record to its owner, for example by passing user-id as
  associated data for an encrypted medical history field, stops an attacker moving it to another user.

## Checked
Date: 2026-11-09. Read: the libsodium secretstream page and the Tink Streaming AEAD page. The IACR 2015/189 page was read
but is an abstract about online AE and nonce reuse, so it was dropped as a source. Removed as not confirmed: the OpenSSL
`EVP_DecryptUpdate` behaviour, the claim that plaintext must not reach a parser before the tag verifies, the buffering
and temp-file options, the Java, Go and pyca behaviour, age and AWS Encryption SDK claims, the hand-rolled chunk nonce
design, and the decompress-then-verify and HTTP pitfalls.
Method: docs-checked 2026-11-09 against the libsodium secretstream page and the Tink Streaming AEAD page.
