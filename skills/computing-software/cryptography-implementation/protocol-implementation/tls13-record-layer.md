---
id: computing-software.cryptography-implementation.protocol-implementation.tls13-record-layer
name: tls13-record-layer
category: computing-software
field: cryptography-implementation
product: protocol-implementation
tags: [protocol-implementation, cryptography-implementation, tls-record-layer, tls-1-3, rfc-8446, record-padding, aead, key-update]
level: advanced
status: docs-checked
description: "Understand the TLS 1.3 record layer: TLSInnerPlaintext with content type and padding, per-record nonce from sequence number, size limits, and key update triggers."
sources: ["https://www.rfc-editor.org/rfc/rfc8446", "https://www.rfc-editor.org/rfc/rfc9147"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TLS 1.3 record layer

## Encrypted record
```
TLSCiphertext: opaque_type = 23 (application_data), legacy_record_version = 0x0303, length, encrypted_record
TLSInnerPlaintext = content || ContentType (1 byte) || zeros (padding)
```
- The real content type (handshake, alert, application_data) is inside the encryption; every encrypted record
  looks like application_data on the wire.
- Padding zeros after the type let senders hide lengths; the receiver scans from the end of the decrypted
  data to the first non-zero byte, which is the content type. No non-zero byte: `unexpected_message`.

## Nonce and AAD
- `nonce = write_iv XOR (64-bit sequence number in network byte order, left-padded with zeros to iv_length)`;
  separate read and write counters start at 0 for each key and increment per record. Never sent on the wire.
- AAD = the record header (opaque_type, legacy_record_version, length: 5 bytes).
- A dropped, reordered or replayed record fails decryption with `bad_record_mac` (stream transports only;
  DTLS 1.3, RFC 9147, adds an epoch and sequence number to the record header).
- If a sequence number would wrap, rekey or terminate the connection.

## Limits
- Inner plaintext (content, type byte and padding) is at most 2^14 + 1 bytes; the `length` field must not exceed
  2^14 + 256. A larger record from the peer requires a `record_overflow` alert.
- `record_size_limit` extension (RFC 8449) lowers the limit; the reduced limit covers content type and padding.
- AES-GCM: up to 2^24.5 full-size records per connection (RFC 8446 5.5); implementations SHOULD send a
  KeyUpdate before reaching the limit. For ChaCha20-Poly1305 the sequence number would wrap first.

## Pitfalls
- Application data records may have zero-length content (cover traffic); Handshake and Alert records must not
  (`unexpected_message`).
- A handshake message may be split over records, but no other record type may sit between the pieces, and a
  handshake message must not span a key change (ClientHello, EndOfEarlyData, ServerHello, Finished and
  KeyUpdate must end on a record boundary).

## Verify
- [ ] With SSLKEYLOGFILE, Wireshark shows the inner content types of decrypted records.

## Checked
Date: 2026-10-31. Confirmed against RFC 8446 (sections 5.1 to 5.5) and RFC 9147: the 0x0303 and opaque_type 23
fields, 2^14 + 256 length limit and record_overflow, nonce construction, AAD, zero-length rules, padding scan,
the handshake interleaving and key-change rules, the 2^24.5 AES-GCM figure and the ChaCha20 wrap statement,
DTLS epoch and sequence number. Corrected: plaintext limit is 2^14 + 1 for the inner plaintext; KeyUpdate is a
SHOULD, not automatic; the interleaving rule is general, not only at key changes. Removed: tlsfuzzer claim (not
checked).
Method: documentation only; no commands were run.
