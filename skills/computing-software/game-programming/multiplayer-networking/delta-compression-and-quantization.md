---
id: computing-software.game-programming.multiplayer-networking.delta-compression-and-quantization
name: delta-compression-and-quantization
category: computing-software
field: game-programming
product: multiplayer-networking
tags: [multiplayer-networking, delta-compression, quantization, bitpacking, smallest-three, baseline-snapshot, ack, bandwidth, game-programming, delta-baseline, bitpacker]
level: advanced
status: verified
description: "Shrink game snapshots: bit-packing, quantizing positions/rotations (smallest-three quaternions), delta encoding against acked baselines, and per-entity changed flags."
sources: ["https://gafferongames.com/post/snapshot_compression/", "https://gafferongames.com/post/reading_and_writing_packets/", "https://gafferongames.com/post/serialization_strategies/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Delta compression and quantization

**Goal:** fit snapshots for many entities into a small bandwidth budget (Gaffer On Games "Snapshot
Compression": 901 cubes at 60 Hz cost 17.37 Mbps naively against a 256 kbps target; the article then walks through each reduction step).

## 1. Bit-pack instead of bytes
Write fields with exactly the bits needed via a bit writer (`write_bits(value, n)`), with ranges known on
both sides: a bool is 1 bit, an enum of 6 values is 3 bits, health 0-100 is 7 bits.

## 2. Quantize floats
- **Position**: choose world bounds and precision. E.g. +-512 m at 1 mm resolution = 2^20 values per
  axis -> 20 bits instead of 32. `q = round((x - min) / precision)`.
- **Velocity**: clamp to max speed, quantize similarly; or omit and derive from positions.
- **Rotation (smallest three)**: drop the quaternion component with largest magnitude, send its index
  (2 bits) and the other three in [-1/sqrt2, 1/sqrt2] quantized to ~9-10 bits each: ~29-32 bits per
  rotation; reconstruct the dropped one with `sqrt(1 - a^2 - b^2 - c^2)` (sign fixed by negating if needed). Python round trip over 100,000 random rotations: 10 bits per component (32 bits total) gave a worst-case error of 0.22 degrees, 9 bits (29 bits total) 0.44 degrees; ranges: +-512 m at 1 mm is 1,024,000 values, which fits in 2^20 = 1,048,576 (20 bits).
- Quantize the **simulation state on the server too** (or at least before sending) so client and server
  agree; otherwise prediction/extrapolation drift.

## 3. Delta against a baseline
- Client acks the latest snapshot sequence it received.
- Server encodes each new snapshot relative to the most recent **acked** snapshot for that client
  (baseline): unchanged entities cost 1 bit ("not changed"); changed fields send deltas or full values.
- Small position deltas encoded with fewer bits (relative offset within a small range, else full).
- If no acked baseline exists (new client, too old), send full state.
- Keep a ring buffer of sent snapshots per client to delta from.

## 4. Priorities and relevancy
Delta compression pairs with interest management (only relevant entities) and priority accumulators
(important entities more often) to stay under the budget (see multiplayer-networking
bandwidth-budgeting-and-priority).

## Pitfalls
- Encoding and decoding must be bit-identical: write serialization once with a unified read/write
  function (Gaffer's serialize-stream pattern) so they cannot diverge.
- Validate ranges on read (untrusted data): never allocate or index from unchecked network values.
- Measure: log bits per entity type per snapshot.

## Verify
- [ ] Bits per snapshot measured before/after each step; total under budget at max player count.
- [ ] Round-trip fuzz test: random states encode/decode within quantization error.
- [ ] Clients survive lost acks (fallback to older baselines or full state).
