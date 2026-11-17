---
id: computing-software.game-programming.multiplayer-networking.reliable-ordered-messages-over-udp
name: reliable-ordered-messages-over-udp
category: computing-software
field: game-programming
product: multiplayer-networking
tags: [multiplayer-networking, reliable-ordered, acks, ack-bitfield, message-channels, rtt-estimation, udp, game-programming]
level: advanced
status: gated
description: "Build acks and reliable-ordered channels over UDP: ack + 32-bit ack bitfield, sequence buffers, resending unacked messages inside new packets, ordered delivery and RTT."
sources: ["https://gafferongames.com/post/reliability_ordering_and_congestion_avoidance_over_udp/", "https://gafferongames.com/post/reliable_ordered_messages/", "https://github.com/mas-bandwidth/reliable"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reliable ordered messages over UDP

**Goal:** most game data is unreliable (latest state wins), but some messages (chat, "player joined",
inventory changes, RPCs) must arrive exactly once and in order, without TCP's head-of-line stall on
the unreliable data.

## Packet-level acks (redundant)
Every outgoing packet carries `sequence`, `ack` (most recent received sequence) and `ackBits` (bit
*i* set = `ack − 1 − i` received). Each packet acks the last 33 (Gaffer: ack plus a 32-bit field, always 33 acks), so acks survive heavy loss without
dedicated ack packets. A Python simulation of this scheme (20% loss in each direction, one-way latency 100 ms plus or minus 100 ms jitter, 10,000 messages, resend delay max(1.25 x RTT, 0.1 s), RTT smoothing 0.1) delivered all 10,000 messages exactly once and in order, and the RTT estimate settled at 0.197 s against a true mean of 0.2 s.
- **Sequence buffer**: fixed array of 1024 entries indexed by `seq % 1024` with a stored sequence to
  detect stale slots; holds send time and which messages each packet carried.
- On receiving an ack for packet P: mark P acked, compute RTT sample `now − sendTime[P]`, smooth
  (`rtt += (sample − rtt) * 0.1`), and mark P's messages acked.

## Reliable message channel
- Messages get their own 16-bit **message ids** (separate from packet sequence).
- Send queue holds unacked messages; each tick, fill the packet's reliable section with messages not
  sent in the last `resendDelay` (~RTT * 1.25, min 0.1 s), oldest first, within a byte budget.
  A message rides in many packets until one carrying it is acked.
- Receive side: a receive buffer indexed by message id; deliver to the game only when the **next
  expected id** is present (ordered); drop duplicates and ids outside the window.
- Window limit (e.g. 256-1024 messages in flight): if the send queue is full, the connection is
  hopeless; disconnect rather than grow forever.
- Large blocks (level data, avatars) go in a separate **block/fragment** path with per-fragment acks,
  not as one giant message.

## Channels
Mix in one packet: unreliable-sequenced (snapshots, inputs: drop old), reliable-ordered (game
events), reliable-unordered (independent notifications). Each ordered channel stalls only itself.
Libraries: yojimbo/reliable (Glenn Fiedler), ENet, GameNetworkingSockets (Valve), Unity Transport
pipelines (`ReliableSequencedPipelineStage`), Unreal reliable RPCs (per-actor-channel order) (gated: unconfirmed, source is paywalled or blocked).

## Pitfalls
- Using reliable for state that changes every tick (positions): queue grows, latency explodes.
- Reliable RPC spam: Unreal disconnects clients whose reliable buffer overflows (gated: unconfirmed, source is paywalled or blocked).
- Resending immediately on every packet wastes bandwidth; respect the resend delay.

## Verify
- [ ] Under 20% simulated loss and 200 ms jitter, 10,000 reliable messages arrive once, in order.
- [ ] RTT estimate tracks the simulated latency within 10%.
- [ ] Unreliable snapshots keep flowing while a reliable message is being resent.
