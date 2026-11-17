---
id: computing-software.cryptography-implementation.protocol-implementation.authenticated-record-framing
name: authenticated-record-framing
category: computing-software
field: cryptography-implementation
product: protocol-implementation
tags: [protocol-implementation, cryptography-implementation, record-framing, secure-channel, length-field, sequence-number, aead, truncation]
level: advanced
status: docs-checked
description: "Design authenticated record framing for custom secure channels: header as AAD, sequence-number nonces, record size cap, and chunk reorder and truncation detection."
sources: ["https://www.rfc-editor.org/rfc/rfc8446#section-5", "https://doc.libsodium.org/secret-key_cryptography/secretstream", "https://www.imperialviolet.org/2014/06/27/streamingencryption.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Authenticated record framing

## Model: the TLS 1.3 record layer (RFC 8446 section 5)

- **Header as AAD:** the additional data is the record header (opaque_type,
  legacy_record_version, length). An attacker cannot change header fields
  without failing authentication.
- **Nonce from a sequence number:** a 64-bit sequence number is kept
  separately for reading and writing, incremented per record, zero at
  connection start and whenever the key changes. The nonce is the sequence
  number, big-endian and left-padded with zeros to iv_length, XORed with the
  static per-direction write IV. If the number would wrap, rekey or terminate.
- **Per-direction keys:** client_write_key and server_write_key, each with its
  own IV.
- **Size cap:** ciphertext length MUST NOT exceed 2^14 + 256 bytes (2^14
  plaintext, 1 content type byte, at most 255 bytes of AEAD expansion). An
  oversized record terminates the connection (record_overflow).
- **Failure:** if decryption fails the receiver MUST terminate the connection
  (bad_record_mac). There is no separate integrity check.

## Chunked streams (ImperialViolet, libsodium)

- Chunking large data (for example 16 KB) keeps authenticator overhead small
  and makes streaming decryption safe, but the attacker may reorder chunks,
  drop chunks from the start, or drop chunks from the end.
- ImperialViolet sketch: chunk number as part of the nonce starting at zero,
  and an authenticated last-chunk indication. It notes such a scheme needs
  more thought before real use, and that truncation at a chunk boundary
  remains possible if the consumer is not told the stream ended.
- libsodium `secretstream` states that messages cannot be truncated, removed,
  reordered, duplicated or modified without detection. Tag the last message
  `crypto_secretstream_xchacha20poly1305_TAG_FINAL`; the decrypt loop runs
  until it sees that tag. `TAG_REKEY` triggers an explicit rekey.
- Treat end of stream without the final marker as an error.

## Prefer existing designs

Use TLS 1.3 or libsodium secretstream rather than a new framing.

## Verify

- [ ] Tests: flipped header bit, replayed frame, reordered frames, dropped first and last frames, truncated stream all fail.
- [ ] Length is checked against the cap before allocating.
- [ ] No plaintext released before tag verification.

## Checked

Method: docs-checked 2026-11-09 against RFC 8446 sections 5.1 to 5.3 (record format, AEAD, nonce), libsodium secretstream page, ImperialViolet "Encrypting streams". Removed: the invented frame layout (version, type, 4-byte length, seq in AAD), STREAM (Hoang et al.) and Noise recommendations (paper not read for this skill), the close_notify claim, the reflection and padding cross-references.
