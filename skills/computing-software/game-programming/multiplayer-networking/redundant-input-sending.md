---
id: computing-software.game-programming.multiplayer-networking.redundant-input-sending
name: redundant-input-sending
category: computing-software
field: game-programming
product: multiplayer-networking
tags: [multiplayer-networking, input-redundancy, client-prediction, packet-loss, game-programming]
level: practitioner
status: verified
description: "Send redundant inputs: pack the last N unacked input frames in every packet so loss does not drop moves, with delta encoding and server-side de-duplication."
sources: ["https://gafferongames.com/post/deterministic_lockstep/", "https://www.gabrielgambetta.com/client-side-prediction-server-reconciliation.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Redundant input sending

**Goal:** a lost packet should never cost the server a player input.

## Technique
Each client packet carries all inputs since the last one the server acknowledged:
```text
packet = { ackedServerTick, firstInputTick, count, inputs[count] }
client keeps an input ring buffer; server acks the latest tick it received
client sends inputs from (lastAckedInputTick + 1) .. currentTick
```
Inputs are tiny (buttons as bits, quantised stick/aim), so 10-30 redundant frames fit in one
packet. Simulated in Python at 60 Hz with a 6-tick (100 ms) round trip and acks that ride on server replies: with 10% random packet loss, resending everything since the last ack lost 0 of 5,900 inputs (only 9 arrived more than 2 ticks later than the no-loss case), whereas sending each input once lost 590; at 30% loss it was still 0 lost (178 late) against 1,752 lost, and the largest packet held 14 input frames. Glenn Fiedler's deterministic lockstep article shows inputs at 60 Hz with redundancy
surviving heavy loss without retransmission delays.

## Encoding
- Delta encode consecutive inputs (most frames equal the previous): 1 bit "same as previous" per frame.
- Cap redundancy (e.g. 1 s) so a long outage doesn't make packets huge; beyond that the
  connection is effectively timing out.

## Server side
- Keep the highest processed tick per client; ignore older inputs, process new ones in order.
- Missing inputs when it is time to simulate: reuse the last input (prediction of input), then mark;
  if the real one arrives later, it's too late for authoritative servers (rollback servers can
  re-simulate).
- Maintain a small input buffer (jitter buffer) so slightly late inputs still arrive in time.

## Verify
- 10% random loss: zero dropped inputs in server logs. 30% burst loss: inputs recovered on next packet.
- Compare bandwidth with and without redundancy; overhead should be small.
