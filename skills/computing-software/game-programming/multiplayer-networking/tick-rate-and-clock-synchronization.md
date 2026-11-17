---
id: computing-software.game-programming.multiplayer-networking.tick-rate-and-clock-synchronization
name: tick-rate-and-clock-synchronization
category: computing-software
field: game-programming
product: multiplayer-networking
tags: [multiplayer-networking, clock-synchronization, tick-rate, server-tick, rtt, ntp-style-sync, time-dilation, input-buffer, jitter-buffer, game-programming]
level: advanced
status: gated
description: "Synchronise client and server simulation time: choosing tick and send rates, RTT-based clock offset estimation, keeping clients a tick ahead and adjusting via time dilation."
sources: ["https://gafferongames.com/post/fix_your_timestep/", "https://developer.valvesoftware.com/wiki/Source_Multiplayer_Networking", "https://www.gabrielgambetta.com/client-server-game-architecture.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tick rate and clock synchronization

**Goal:** client and server agree on "which tick is it", so inputs arrive at the server just
before the tick they belong to and interpolation buffers sit at the right delay.

## Tick and send rates
- **Simulation tick** (server): fixed, e.g. 30, 60 or 128 Hz. Higher = finer hit registration, more CPU.
- **Snapshot send rate**: may be lower than tick (e.g. 20-30 Hz) to save bandwidth; clients
  interpolate.
- **Client input send rate**: usually every tick, with the last few inputs redundantly included to
  survive packet loss.
- Source engine defaults as reference: `tickrate` 66, `cl_updaterate`/`cl_cmdrate`, `cl_interp` 0.1 s
  (or `cl_interp_ratio` 2 snapshots) (gated: unconfirmed, source is paywalled or blocked).

## Estimating server time on the client
NTP-style exchange: client sends `t_c0`, server replies with `t_s` (its time when processing),
client receives at `t_c1`.
```
rtt    = t_c1 - t_c0
offset = t_s + rtt/2 - t_c1          # estimate of server_time - client_time
```
Take many samples, discard outliers (keep lowest-RTT samples or median), smooth over time. Never jump
the clock backwards abruptly; slew it. The estimate assumes symmetric path delay: with true offset 5.0 s, equal 50 ms legs give exactly 5.0, while 20 ms up and 80 ms down gives an error of (up - down)/2 = -30 ms (computed), which no amount of averaging removes.

## Where the client should run
- **Predicting client (input side):** simulate ahead of the server by `rtt/2 + input buffer`
  (e.g. 1-2 ticks of safety), so its input for tick N arrives before the server simulates tick N.
- **Remote entities:** render at `server_time - interpolation_delay` (e.g. 2 snapshot intervals).

## Adjusting continuously (time dilation)
The server reports how many ticks of input it has buffered for the client (or how late inputs are).
The client nudges its tick rate slightly:
```
if buffered < target: client_tick_dt *= 0.99   # run slightly faster to get further ahead
if buffered > target + 2: client_tick_dt *= 1.01
```
Overwatch's GDC netcode talk described this approach (gated: unconfirmed, source is paywalled or blocked); players do not notice 1-3% time changes,
but they would notice skipped or repeated ticks.

## Server-side input buffer
Server keeps a small queue of inputs per client keyed by tick. Missing input at tick time: repeat the
last input (and tell the client to speed up). Too many: drop the oldest or tell client to slow down.

## Verify
- [ ] Log per-client "input arrived N ticks early"; stays at target +-1 under 0-200 ms RTT.
- [ ] Simulated jitter of 50 ms: no missing-input repeats in steady state.
- [ ] Changing RTT from 50 to 200 ms mid-game converges within a few seconds without visible jumps.
