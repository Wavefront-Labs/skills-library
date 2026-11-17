---
id: computing-software.cryptography-implementation.protocol-implementation.rekeying-long-lived-channels
name: rekeying-long-lived-channels
category: computing-software
field: cryptography-implementation
product: protocol-implementation
tags: [cryptography-implementation, protocol-implementation, secure-channel, channel-rekeying, key-update, aead-limits, confidentiality-limit, integrity-limit, forward-secrecy, ratchet]
level: advanced
status: docs-checked
description: "Rekey long-lived encrypted channels before AEAD usage limits: TLS 1.3 and QUIC per-algorithm limits, hash-ratchet key update and switch coordination."
sources: ["https://datatracker.ietf.org/doc/html/rfc8446#section-5.5", "https://datatracker.ietf.org/doc/html/rfc9001#section-6.6"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rekeying long-lived channels

AEAD keys wear out: after enough encryptions, confidentiality and forgery
bounds degrade. Long-lived connections must rotate traffic keys inside the
session.

## Limits to design against

| AEAD | Confidentiality limit | Integrity limit (failed decrypts) | Source |
|---|---|---|---|
| AES-GCM, TLS 1.3 | 2^24.5 full-size records | not stated there (TLS closes on any failed record) | RFC 8446 5.5 |
| AES-128/256-GCM, QUIC | 2^23 encrypted packets | 2^52 invalid packets | RFC 9001 6.6 |
| ChaCha20-Poly1305, QUIC | greater than the number of possible packets (2^62), disregard | 2^36 invalid packets | RFC 9001 6.6 |
| AES-128-CCM, QUIC | 2^21.5 encrypted packets | 2^21.5 invalid packets | RFC 9001 6.6 |

- RFC 8446: for ChaCha20/Poly1305 the record sequence number wraps before
  the safety limit, and implementations SHOULD key update before reaching
  the limits.
- QUIC counts confidentiality per key (packets encrypted) and integrity per
  connection (failed packets across all keys). Exceeding the confidentiality
  limit means the endpoint MUST stop using those keys, so it MUST key update
  first. Exceeding the integrity limit means the endpoint MUST close the
  connection with AEAD_LIMIT_REACHED. QUIC ignores unauthenticated packets,
  allowing repeated forgery attempts; TLS instead closes the connection
  after any record fails authentication.
- Endpoints that limit packet size MAY use higher limits (RFC 9001 Appendix B).

## Hash-ratchet rekeying

- **TLS 1.3 KeyUpdate:** sent by either peer after Finished. The sender then
  uses the next generation of keys and the receiver MUST update its receive
  keys. `request_update` set to `update_requested` obliges the peer to send
  its own KeyUpdate before its next application data. Crossing requests
  advance each side two generations. Both sides MUST send KeyUpdate under the
  old keys and MUST require it before accepting messages under the new keys,
  or truncation attacks become possible. Next secret:
  `HKDF-Expand-Label(secret, "traffic upd", "", Hash.length)`.
- **QUIC key update:** new write secret is
  `HKDF-Expand-Label(secret, "quic ku", "", Hash.length)`; the header
  protection key is not updated. The Key Phase bit is toggled. No update
  before the handshake is confirmed, and no further update until a packet
  protected with the current phase's keys has been acknowledged.
- Send and receive keys come from independent traffic secrets, so retaining
  the receive secret does not threaten forward secrecy of data already sent
  (RFC 8446 4.6.3).

## Coordinating the switch (QUIC)

- Keep old read keys until a packet under the new keys decrypts; discard
  them no more than 3x PTO after receiving such a packet.
- Wait 3x PTO after an acknowledgment confirming the previous update before
  initiating the next, so the peer can still decrypt.

## Verify

- [ ] A per-key packet or record counter triggers rekey well under the limit.
- [ ] A failed-decrypt counter closes the connection at the integrity limit.
- [ ] Old keys are discarded after the grace window.
- [ ] Interop test: force a key update mid-stream and confirm traffic continues.

## Checked

Method: docs-checked 2026-11-09 against RFC 8446 (5.5 limits, 4.6.3 KeyUpdate, 7.2 label), RFC 9001 (6.1 to 6.6 key update and AEAD limits). Removed: the draft-irtf-cfrg-aead-limits source (not matched to claims), the "380 GiB" figure, the corrected CCM limit (was 2^23), the hash-ratchet versus fresh-DH comparison (IKEv2, SSH, Signal), OpenSSH RekeyLimit advice, the KeyUpdate rate-limiting claim, and the `openssl s_client` k/K test.
