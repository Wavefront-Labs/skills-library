---
id: creative-arts.game-design.systems-and-mechanics.dynamic-difficulty-adjustment
name: dynamic-difficulty-adjustment
category: creative-arts
field: game-design
product: systems-and-mechanics
tags: [game-design, dynamic-difficulty, dda, difficulty-design, flow-channel, rubber-banding, ai-director, adaptive-difficulty, player-modelling]
level: advanced
status: draft
description: "Design dynamic difficulty adjustment: which signals to read, which levers to move, how fast, how visibly, and how to avoid players gaming or resenting the system."
sources:
  - https://www.jenovachen.com/flowingames/Flow_in_games_final.pdf
  - https://steamcdn-a.akamaihd.net/apps/valve/2009/ai_systems_of_l4d_mike_booth.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Dynamic difficulty adjustment

**Goal:** the game adapts challenge to the individual player in real time, keeping them
in the flow channel without them feeling patronised or exploited.

## Signals (inputs)
- Deaths/failures per section, retries on the same challenge.
- Health/resources at the end of encounters.
- Time to complete vs expected.
- Accuracy, damage taken per minute.
- Measured "intensity" (Left 4 Dead's AI Director tracks per-survivor emotional
  intensity from damage taken, incapacitation and nearby kills, then builds up, peaks
  and relaxes - see Booth's 2009 presentation).

## Levers (outputs)
| Lever | Visibility | Notes |
|---|---|---|
| Item/health drop rates | low | the gentlest lever |
| Enemy count/spawn timing | low-medium | used by AI directors |
| Enemy accuracy/aggression | low | subtle; easy to overdo |
| Enemy health/damage | medium | players notice "spongy" enemies |
| Puzzle hints offered | high | ask rather than force |
| Checkpoint frequency | low | very effective, little resentment |

## Procedure
1. Define the **target band** (e.g. 1-3 failures per section, end-of-fight health 20-60%).
2. Pick **2-3 signals** and **2-3 levers**; more makes behaviour hard to reason about.
3. Use **hysteresis and slow rates**: adjust after several data points, in small steps,
   with caps. Fast oscillating adjustment is noticeable.
4. **Asymmetric adjustment:** ease off faster than you ramp up; players tolerate help
   more than sudden extra punishment.
5. Decide **disclosure**: hidden DDA can feel cheap if discovered; optional, visible
   assist features are more respectful (see
   `creative-arts.game-design.systems-and-mechanics.difficulty-settings-and-assist-modes`).
6. **Exploit check:** can players deliberately fail to make the game easy before a
   reward? Bound the system or keep rewards independent of the adjusted state.

## Gotchas
- Competitive multiplayer DDA (rubber banding) is perceived as unfair by leaders.
- DDA can hide design problems; check unadjusted difficulty in playtests too.
- Players who want challenge may feel cheated by help they did not request; offer an
  off switch on higher difficulty modes.

## Verify
- [ ] Target band, signals, levers, rates and caps documented.
- [ ] Simulation or test shows convergence without oscillation.
- [ ] Deliberate-fail exploit tested.
- [ ] Playtesters do not report the game "cheating" in either direction.
