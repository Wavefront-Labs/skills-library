---
id: computing-software.networking-hardware-and-wireless.wireguard.wireguard-handshake-timers-and-key-rotation
name: wireguard-handshake-timers-and-key-rotation
category: computing-software
field: networking-hardware-and-wireless
product: wireguard
tags: [handshake, rekey-timeout, reject-after-time, noise-ik, perfect-forward-secrecy, keepalive-timers, udp]
level: advanced
status: docs-checked
description: "Understand WireGuard handshake retries, rekey intervals, session expiry and the rate limits that explain stale peers."
sources: ["https://www.wireguard.com/protocol/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# WireGuard handshake timers and key rotation

WireGuard is connectionless: bring the interface up and it handles keys itself. Packets are UDP using Noise_IK(psk2) with ChaCha20-Poly1305, Curve25519, BLAKE2s, SipHash24 and HKDF. Handshakes repeat every few minutes for perfect forward secrecy, driven by time and not packet contents so packet loss is tolerated.

Timers described on the protocol page:
- Initiation is retried after REKEY_TIMEOUT plus 0-333 ms jitter until a response arrives; initiations are strictly rate limited to one per REKEY_TIMEOUT.
- Packet received but nothing sent for KEEPALIVE ms: send an empty packet. Packet sent but nothing received for KEEPALIVE + REKEY_TIMEOUT: start a new handshake.
- The original initiator rekeys when the session key reaches REKEY_AFTER_TIME or the packet count reaches REKEY_AFTER_MESSAGES; the original responder does not rekey on age alone.
- Packets are dropped past REJECT_AFTER_MESSAGES or REJECT_AFTER_TIME. Session keys and ephemeral keys are zeroed after REJECT_AFTER_TIME x 3 with no new keys.
- After REKEY_ATTEMPT_TIME of failed initiation attempts the retries stop and queued packets are cleared.

Key confirmation: after the responder replies, only the initiator may send data; the responder waits for the first encrypted packet from the initiator, so an initiator with nothing queued sends an empty packet.

Handshake packets use DSCP 0x88 (AF41) so they are the least likely to be dropped.

Verify: while traffic flows, `wg show wg0 latest-handshakes` keeps showing a recent value for the peer.

## Checked

2026-11-03. Confirmed: Primitives, Noise_IKpsk2 handshake over UDP, every-few-minutes handshakes, all listed timers, key confirmation and DSCP 0x88 (AF41) against the protocol page. Removed: the unsupported diagnosis that a stale handshake means UDP reachability rather than authentication failure.

Method: documentation only; no commands were run.
