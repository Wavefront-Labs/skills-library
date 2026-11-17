---
id: computing-software.cryptography-implementation.applied-cryptography.hpke-info-and-aad-binding
name: hpke-info-and-aad-binding
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [applied-cryptography, cryptography-implementation, hpke-info, hpke, rfc-9180, aad, context-binding, domain-separation, key-schedule]
level: advanced
status: docs-checked
description: "Use HPKE info and aad correctly: what each binds, how to encode application context, sender/recipient identity binding, and avoiding cross-protocol reuse."
sources: ["https://www.rfc-editor.org/rfc/rfc9180#section-5.1", "https://www.rfc-editor.org/rfc/rfc9180#section-8", "https://www.rfc-editor.org/rfc/rfc9458"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HPKE info and aad binding

## What each input does
- **info** (setup time): mixed into the HPKE key schedule (`LabeledExpand(secret, "key", key_schedule_context)`),
  so every key derived from the context depends on it. Bind application identity, protocol version, and anything
  that must be the same for the whole context.
- **aad** (per message): authenticated with each `Seal`/`Open`; bind per-message metadata (record type, sequence,
  headers that travel in clear).
- **psk / psk_id** (PSK modes) and sender key (Auth modes): authenticate the sender, unlike info.

## Encoding info
Make it unambiguous and protocol-specific:
```
info = "example.com/file-sharing/v1" || 0x00 || uint16(len(recipient_id)) || recipient_id || uint16(len(file_id)) || file_id
```
Real example: Oblivious HTTP (RFC 9458 section 4.3) builds info as the ASCII string `"message/bhttp request"`,
a zero byte, then the request header.

## Pitfalls
- Leaving info empty in two different applications that share a recipient key lets ciphertext from one be accepted
  by the other.
- info is not secret and not authentication of the sender: base-mode HPKE is anonymous. Anyone can encrypt to the
  recipient with any info.
- If you need to check info at the recipient, it must be reconstructible there (from known context), because HPKE
  does not transmit it.
- aad must be supplied identically for Open; transmit it or derive it from context.

## Verify
- [ ] Changing one byte of info at the recipient makes Open fail.
- [ ] Different applications using one key pair use distinct info prefixes.
- [ ] RFC 9180 Appendix A vectors pass for your suite.

## Checked

2026-11-01: RFC 9180 section 5.1 (key schedule, key_schedule_context, info_hash) and RFC 9458 section 4.3 read. Confirmed: info enters the key schedule, the OHTTP info construction. Removed: the ECH info example (RFC not read this pass).
Method: documentation only; no commands were run.
