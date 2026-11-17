---
id: computing-software.game-programming.multiplayer-networking.rollback-netcode-and-ggpo
name: rollback-netcode-and-ggpo
category: computing-software
field: game-programming
product: multiplayer-networking
tags: [multiplayer-networking, rollback-netcode, ggpo, peer-to-peer, deterministic-simulation, input-delay, resimulation, desync, state-hashing, fighting-game-netcode, lockstep, frame-advantage, checksum, game-programming]
level: sme
status: draft
description: "Implement GGPO-style rollback netcode: deterministic simulation, local input-delay vs rollback distance tradeoffs, and catching desyncs before players do."
sources: ["https://github.com/pond3r/ggpo", "https://words.infil.net/w02-netcode.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Rollback netcode (GGPO-style)

**Goal:** the peer-to-peer netcode model used by modern fighting games and
other low-tolerance, deterministic simulations — distinct from the
server-authoritative client-prediction model in
`computing-software.game-programming.multiplayer-networking.client-prediction-and-server-reconciliation`,
which corrects a client against a trusted server. Rollback has no server
authority at all for gameplay simulation: both peers simulate the full game
and resolve disagreements by rewinding and replaying.

## The core loop
Every peer runs the full simulation locally using its own input immediately
(zero added latency for your own actions) and the *last known* input from the
remote peer (a guess — usually "repeat their last received input" as the
prediction). When the remote peer's actual input for that frame arrives over
the network and it matches the guess, nothing happens. When it **doesn't**
match: roll the simulation state back to the last frame where both inputs are
now known, re-simulate forward frame-by-frame with the corrected input to the
present, in a handful of milliseconds — fast enough that visually the
correction either isn't noticeable or shows as a brief, small position
correction rather than the stop-and-wait of lockstep. This is why it requires
the simulation to be **fully deterministic**: the same input sequence must
produce bit-identical results every time it's replayed, or rollback
resimulation diverges from what already happened once and desyncs.

## What determinism actually requires
- **No floating-point operations whose result can differ across the two
  peers' hardware/compiler** in gameplay-affecting code — this is the
  single hardest constraint. Differences in FPU instruction sets, compiler
  optimization flags, or even some SIMD intrinsics can produce bit-different
  float results from logically identical code on different CPUs. Many
  rollback implementations use fixed-point math for gameplay logic specifically
  to sidestep this, or constrain build settings tightly enough to guarantee
  float determinism across the supported platform set (tested, not assumed).
- **No reliance on frame-rate-dependent timing** that isn't part of the
  replayed input stream — anything reading a wall-clock timestamp directly
  into gameplay logic instead of a simulation-tick-derived value breaks replay.
- **No unseeded or externally-seeded randomness** — RNG must be seeded
  identically on both peers and advanced only by simulation ticks, never by
  anything that could differ between the two machines (frame timing, OS
  scheduling).
- Any non-deterministic step (asset loading order affecting an iteration over
  an unordered container, hash-map iteration order, pointer-based sort
  tie-breaking) is a desync waiting to happen — use ordered/stable containers
  and comparisons for anything touched during the simulated tick.

## Input delay vs rollback distance — the tunable tradeoff
Two independent knobs: **input delay** (buffer your own input N frames before
acting on it — gives the network more time for the remote input to arrive
before a guess is even needed, reducing how often rollback triggers, at the
cost of added perceived input latency even in a perfect network) and
**maximum rollback frames** (how far back resimulation can reach — bounded by
both a feasible compute budget per correction and diminishing fairness, since
rolling back and overwriting many frames of visual history that already
played is itself a worse user experience past a certain window). Shipped
fighting games commonly use 2-3 frames of input delay plus a rollback window
in the 5-8 frame range as a starting point — the right numbers depend on tick
rate and target connection quality, tune and playtest rather than copying a
number verbatim.

## Desync detection — catch it, don't ship blind
Periodically hash the full simulation state (not just visible position — any
state that affects future simulation) on each peer and exchange/compare the
hashes; a mismatch means the peers have silently diverged (a determinism bug
somewhere) and the match is no longer meaningfully synchronized even though
nothing crashed. Log the state (or a diff against the last agreeing hash) on
mismatch during development — desyncs found this way, with a frame number and
state dump, are debuggable; a desync discovered only by a player reporting
"the match went weird" is nearly impossible to trace back to its cause.

## Verify
- [ ] The same recorded input sequence replayed on two different machines (or
      two builds) produces bit-identical state hashes every frame — the single
      test that catches most determinism bugs before players do.
- [ ] Rollback resimulation after a misprediction is visually a small
      correction, not a visible teleport, within the shipped max-rollback window.
- [ ] Periodic state-hash exchange between peers is implemented and a forced
      desync (manually diverging one peer's RNG seed in a test build) is
      detected and logged with enough context to debug.
- [ ] Gameplay logic uses fixed-point math or a verified-deterministic float
      path; no direct wall-clock reads inside the simulated tick.
