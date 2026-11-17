---
id: computing-software.game-programming.multiplayer-networking.audio-and-vfx-during-rollback
name: audio-and-vfx-during-rollback
category: computing-software
field: game-programming
product: multiplayer-networking
tags: [multiplayer-networking, rollback-effects, rollback-netcode, game-feel, game-programming]
level: practitioner
status: draft
description: "Handle sounds, particles and camera shake under rollback netcode: deferring, de-duplicating and cancelling effects when re-simulation changes the outcome."
sources: ["https://www.ggpo.net/", "https://www.gdcvault.com/play/1025471/8-Frames-in-16ms-Rollback"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Audio and VFX during rollback

**Goal:** rollback re-simulates frames several times; effects must not replay, stutter or survive
when the corrected timeline says they never happened.

## Problem
Frame 100: predicted punch hits, hit spark and sound play. Frame 103: remote input arrives showing
a block, rollback to 100 and re-sim; now the punch is blocked. Naive code plays the block effect too
(and maybe the hit sound again on each re-sim).

## Techniques
1. **Effects are outputs, not state:** gameplay simulation emits effect *requests* with a stable
   identity: `(frame, entity, effectType, sequence)`. A presentation layer outside the sim decides
   what to play.
2. **De-duplicate on re-sim:** keep a table of started effects keyed by identity; a re-simulated
   frame emitting the same identity does nothing.
3. **Cancel on mispredict:** after a rollback, effects started in the rolled-back range whose
   identity was not re-emitted get stopped (fade out quickly). Mortal Kombat/Injustice
   (GDC 2018 *8 Frames in 16ms*) stop such sounds and particles.
4. **Seek, don't restart:** effects re-emitted at an earlier frame keep playing from their current
   time; long sounds may be seeked to `(now - startFrame)`.
5. **Delay-sensitive choice:** very short sounds (hits) play immediately; dramatic, long ones can
   wait for confirmed frames (all inputs known) at the cost of latency.

## Never inside sim
- Particle systems, audio voices and camera shake with their own randomness or timers must not feed
  back into simulation state.
- Rendering-side RNG must not consume the sim RNG.

## Verify
- Force a misprediction every few frames in a test mode (random input delay): no double sounds, no
  orphaned particles; SyncTest still passes (effects don't touch state).
