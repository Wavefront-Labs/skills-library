---
id: computing-software.cryptography-implementation.protocol-implementation.message-numbering-and-replay-windows
name: message-numbering-and-replay-windows
category: computing-software
field: cryptography-implementation
product: protocol-implementation
tags: [cryptography-implementation, protocol-implementation, secure-channel, replay-window, sequence-numbers, anti-replay, sliding-window, ipsec, dtls, rfc4303]
level: advanced
status: docs-checked
description: "Stop replay, reordering and deletion in a secure channel: authenticated sequence numbers, strict vs sliding-window acceptance (IPsec/DTLS style), and nonce derivation."
sources: ["https://datatracker.ietf.org/doc/html/rfc4303", "https://datatracker.ietf.org/doc/html/rfc9147"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Message numbering and replay windows

A secure channel must ensure the receiver gets
a subsequence of the sent messages, in order, without duplicates. Encryption
plus a MAC per message is not enough; an attacker can replay, drop or reorder
whole authenticated messages. The fix is a message number authenticated with
every message.

## Reliable ordered transport (TCP, QUIC streams)

- Each direction keeps a 64-bit counter starting at 0.
- The counter is not sent (or is sent and checked); it is part of the AEAD
  nonce or AAD. TLS 1.3 derives the per-record nonce as `iv XOR seq`.
- Receiver expects exactly `next_seq`; anything else is a fatal error that
  tears down the channel. No "skip ahead".
- Stop and rekey before the counter wraps (TLS 1.3 limits are far below 2^64
  because of AEAD bounds; see rekeying skill).

## Unreliable transport (UDP, DTLS, IPsec, VPNs)

Packets can be lost or reordered, so strict ordering would drop good traffic.
Use a sliding window (RFC 4303 3.4.3, DTLS 1.3 4.5.1):

```
on receive(seq):
  if seq + W <= highest: reject (too old)
  if seq <= highest and bitmap[seq] set: reject (replay)
  verify AEAD tag  # only update state after authentication succeeds
  if seq > highest: shift bitmap by (seq - highest); highest = seq
  mark bitmap[seq]
```

- Window W: RFC 4303 requires support for at least 32 packets with 32-bit sequence numbers (64 preferred);
  RFC 9147 says to pick a window large enough for plausible reordering at your data rate. DTLS keeps a
  separate window per epoch.
- **Update the window only after the record is authenticated** (RFC 9147: the window MUST NOT be updated
  until the record is deprotected successfully); otherwise forged packets
  can advance `highest` and cause legitimate packets to be dropped (DoS).
- IPsec ESN gives a 64-bit sequence number per SA, with the high-order bits possibly not transmitted
  (RFC 4303); ESN support is a SHOULD.

## Nonce relationship

With AEADs, sequence number as nonce (or XORed into a per-direction IV) makes
nonce uniqueness automatic, as long as each direction has its own key or IV
(see directional keys). Never use random nonces and a separate counter: you
get two things to get wrong.

## Application-layer replay (APIs, webhooks)

For stateless request signing, replay protection needs a short timestamp window
plus a nonce cache covering that window, both inside the
signed data.

## Verify

- [ ] Replaying a captured message is rejected; reordered message on TCP-like channel kills the session.
- [ ] Forged packets with high sequence numbers do not move the window.
- [ ] Counter overflow triggers rekey or teardown, tested with a counter seeded near the limit.

## Checked
Date: 2026-10-31. Confirmed in RFC 4303 (3.4.3 minimum window 32 packets, 64 preferred; ESN 64-bit sequence number,
SHOULD implement) and RFC 9147 4.5.1 (sliding window borrowed from RFC 4303, window sized for reordering, per-epoch
window, no update before successful deprotection; DTLS lacks order protection). Corrected: the IPsec minimum is 32,
not 64. Removed: WireGuard window size, the 5-minute figure and the book chapter reference (the book page lists no
chapter contents).
Method: documentation only; no commands were run.
