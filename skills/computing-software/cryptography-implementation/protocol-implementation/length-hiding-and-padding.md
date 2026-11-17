---
id: computing-software.cryptography-implementation.protocol-implementation.length-hiding-and-padding
name: length-hiding-and-padding
category: computing-software
field: cryptography-implementation
product: protocol-implementation
tags: [cryptography-implementation, protocol-implementation, secure-channel, length-hiding-padding, traffic-analysis, compression-oracle, crime, breach, padme, tls-record-padding]
level: advanced
status: docs-checked
description: "Limit what ciphertext length reveals: Padme and block padding, TLS 1.3 record padding, never compressing secrets with attacker data (CRIME, BREACH)."
sources: ["https://datatracker.ietf.org/doc/html/rfc8446#section-5.4", "https://www.petsymposium.org/2019/files/papers/issue4/popets-2019-0056.pdf", "https://www.breachattack.com/", "https://doc.libsodium.org/padding"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Length hiding and padding

Encryption hides content, not length. Most constructions disclose message
lengths (libsodium docs), and with compression the length can reveal secret
values (CRIME, BREACH).

## Padding

- **Pad inside the encrypted payload**: libsodium says padding should be
  applied before encryption and removed after decryption.
- **libsodium `sodium_pad` / `sodium_unpad`:** extend a buffer to a multiple
  of a block size using ISO/IEC 7816-4 padding; unpad fails on incorrect
  padding. Do not use padding to hide a password length; hash the password
  instead. Applications may still leak the unpadded length by side channels.
- **Padme (PURB paper):** a padding scheme limiting length leakage to
  O(log log M) bits for maximum payload size M, with overhead at most 12%
  and decreasing for larger payloads.
- **TLS 1.3 record padding (RFC 8446 5.4):** the sender may append zero
  bytes after the content type field before encryption; senders MUST set
  padding octets to zero. The receiver scans from the end for the first
  non-zero octet (the content type), limited to the AEAD-decrypted
  plaintext, and MUST terminate with unexpected_message if there is none.
  The padded TLSInnerPlaintext MUST NOT exceed 2^14 + 1 octets. A
  zero-length Application Data record is allowed (cover traffic); zero-length
  Handshake or Alert records are not. The RFC leaves padding policy
  out of scope, and suggests padding at the application layer when the
  application protocol has its own padding.

## Compression with secrets (BREACH)

- CRIME: an attacker who can inject partial chosen plaintext into requests and
  measure encrypted traffic size can recover targeted plaintext. Disabling
  TLS-level compression mitigates the demonstrated attack.
- BREACH attacks HTTP response compression. A page is exposed when it uses
  HTTP compression, reflects user input in the body, and reflects a secret
  (such as a CSRF token) in the body. It is independent of TLS version and
  cipher suite, and the secret can be guessed one character at a time.
- Mitigations listed by the BREACH site, in order of effectiveness: disable
  HTTP compression; separate secrets from user input; randomise secrets
  per request; mask secrets (XOR with a per-request random value); protect
  vulnerable pages with CSRF; length hiding (random extra bytes in
  responses); rate-limit requests. The site also recommends monitoring traffic.

## Verify

- [ ] Responses whose class must stay hidden have equal ciphertext lengths in tests.
- [ ] Padding removal is unambiguous and runs after authentication.
- [ ] No compression of mixed secret and attacker data before encryption.
- [ ] Overhead measured and accepted.

## Checked

Method: docs-checked 2026-11-09 against RFC 8446 section 5.4, libsodium padding page, PURB paper (PoPETs 2019, text extracted), breachattack.com. Removed: the comparison table rows for fixed size, power-of-two and random padding, "used by some messengers", web page and voice-phrase fingerprint examples, OpenSSL padding callbacks, the claim that TLS 1.3 removed compression, and the timing and cover-traffic paragraph.
