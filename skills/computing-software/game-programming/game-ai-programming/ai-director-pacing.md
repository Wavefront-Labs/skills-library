---
id: computing-software.game-programming.game-ai-programming.ai-director-pacing
name: ai-director-pacing
category: computing-software
field: game-programming
product: game-ai-programming
tags: [game-ai-programming, ai-director, dynamic-pacing, intensity-tracking, procedural-spawning, left-4-dead, game-programming]
level: advanced
status: verified
description: "Build an AI director that paces play: per-player intensity tracking, build-up/peak/relax cycles, spawning out of sight along the flow path, and budgets for specials and pickups."
sources: ["https://steamcdn-a.akamaihd.net/apps/valve/2009/ai_systems_of_l4d_mike_booth.pdf", "https://www.gameaipro.com/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AI director pacing

**Goal:** a system above individual AI that controls *when* and *where* threats appear so every run
has dramatic rhythm, adapting to how the players are doing (Valve's Left 4 Dead director, Mike Booth,
"The AI Systems of Left 4 Dead", 2009).

## Track intensity per player
Emotional intensity value per survivor, increased in proportion to damage taken, on incapacitation, when pushed off a
ledge, and when a nearby infected dies (inversely proportional to distance), and decaying towards zero over time but
not while infected are actively engaging that survivor. Use the **maximum** across the team for decisions.
```
intensity += damageTaken * k1 + (nearbyKill ? k2 / distance : 0)
intensity  = max(0, intensity - decayPerSecond * dt)   // decay only when not in combat
```

## Pacing state machine (L4D)
- **Build up:** create the full threat population until intensity crosses the peak threshold.
- **Sustain peak:** continue the full population for 3-5 s after the peak.
- **Peak fade:** switch to the minimal population and wait until intensity decays out of the peak range, so the
  current fight plays out without eating the relax period.
- **Relax:** minimal threats for 30-45 s, or until the survivors have travelled far enough toward the next safe
  room; then build up again.

## Where to spawn
- Precompute the **flow distance** along the navmesh from start to goal; players' progress is their
  flow value.
- Spawn in the **Active Area Set** (the navmesh areas surrounding the team), in areas **not visible** to any
  player (potential visibility is precomputed between nav areas). In L4D, 75% of mobs spawn at or behind the team's
  flow distance (wanderers and specials are usually engaged ahead), slow Boomers spawn ahead, and Smokers pick
  areas above the team.
- Wanderers are stored as a count per area, created when the area enters the active set and deleted when it
  leaves, so the world feels full without simulating the whole level.

## Budgets
In L4D, special infected are created at individually randomised intervals and mobs at randomised intervals (90-180 s
on Normal) with mob size growing from a minimum just after a spawn to a maximum after some time. Design suggestion
(not from the talk): cap alive specials per type and tune item placement by team state. Difficulty scales budgets and
intensity thresholds (see `dynamic-difficulty-adjustment`).

## Design cautions
Players must not feel cheated: no spawns in view, fair warnings (audio cues for specials), and a
minimum relax period. Log the intensity curve per session; plot it to tune (the target shape is a
sawtooth with peaks, not a flat line).

## Verify
- [ ] Session telemetry plot shows build/peak/relax cycles.
- [ ] No spawn ever occurs inside any player's view frustum and line of sight (automated assert).
- [ ] A struggling team (low health) receives more relax time and more health items than a strong one.

## Checked (2026-10-22)
- Read the Valve slide deck text (Mike Booth, AI Systems of Left 4 Dead, 2009): intensity inputs and decay rules, max over the four survivors, Build Up / Sustain Peak (3-5 s) / Peak Fade / Relax (30-45 s or until far enough toward the next safe room), Active Area Set, potential visibility, wanderer counts per area, mob interval 90-180 s on Normal, 75% of mobs from behind, Boomers ahead. Corrected spawn direction advice; removed the 'scripted crescendo override' and 'radius' claims (not in the slides) and the unsourced 'deck' budget.
- Simulated the four-state machine (build 0..0.3 per tick until 1.0, sustain 4 s, fade, relax 35 s): 13 cycles in 600 s of simulated time with a clear peak and relax shape; the telemetry check in Verify is design guidance.
