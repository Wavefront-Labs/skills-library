---
id: computing-software.game-programming.multiplayer-networking.congestion-avoidance-and-send-rates
name: congestion-avoidance-and-send-rates
category: computing-software
field: game-programming
product: multiplayer-networking
tags: [multiplayer-networking, congestion-avoidance, send-rate, udp, game-programming]
level: practitioner
status: gated
description: "Avoid flooding connections over UDP: RTT and loss-based send-rate control, bandwidth estimation, adaptive snapshot rates and congestion backoff."
sources: ["https://datatracker.ietf.org/doc/html/rfc8085"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Congestion avoidance and send rates

**Goal:** UDP has no congestion control; a game that sends at a fixed high rate will cause its own
packet loss and latency on weak links. RFC 8085 (UDP usage guidelines, section 3.1) says an application that does not use a congestion-controlled transport SHOULD control the rate at which it sends UDP datagrams.

## Simple binary mode (Gaffer On Games)
```text
good mode: 30 packets/s     bad mode: 10 packets/s
if RTT > threshold (e.g. 250 ms): drop to bad mode
return to good only after RTT stays good for T seconds; double T when you drop from good to bad in under 10 s (cap 60 s),
halve T for each 10 s spent in good mode (floor 1 s)  [parameters from Gaffer's article]
```
Crude but robust, and prevents oscillation via the hysteresis timer.

## Bandwidth-aware approach
- Estimate available rate from acked bytes per RTT; increase rate slowly (additive) while loss and
  RTT are stable, cut multiplicatively on loss bursts or RTT rising well above the minimum RTT
  (delay-based signal, like LEDBAT/BBR ideas).
- Valve GameNetworkingSockets exposes per-connection `k_ESteamNetworkingConfig_SendRateMin` / `SendRateMax` (bytes per second, default 256K). Its header says that for now both should be set to the same value to configure a fixed send rate, with bandwidth estimation a future goal, so treat them as a clamp, not an adaptive controller.

## What to adapt
- Snapshot frequency (60 -> 30 -> 20 Hz) and entity priority budget per packet (bandwidth budgeting).
- Never adapt by delaying reliable control messages; adapt the bulk state data.
- Voice chat bitrate.

## Signals to watch
- RTT trend vs baseline RTT (queues filling).
- Loss rate over a sliding window (1-2 s).
- Ack gaps.

## Pitfalls
- Reacting to single lost packets; use windows.
- Wi-Fi random loss is not congestion; backing off hard on random loss hurts more than it helps.

## Verify
- Use a link emulator (clumsy on Windows, `tc netem` + `tbf` rate limit on Linux; neither was run in this review (gated: unconfirmed, source is paywalled or blocked)) at 256 kbit/s:
  the game drops rates and stays playable, RTT doesn't climb unbounded.
