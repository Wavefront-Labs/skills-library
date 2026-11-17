---
id: creative-arts.game-design.systems-and-mechanics.difficulty-curve-design
name: difficulty-curve-design
category: creative-arts
field: game-design
product: systems-and-mechanics
tags: [game-design, difficulty-curve, difficulty-design, flow-channel, sawtooth, challenge, pacing, flow, csikszentmihalyi, ramp]
level: practitioner
status: draft
description: "Shape a difficulty curve that keeps players in the flow channel: sawtooth ramps of tension and release, rising baseline, measured with failure and completion data."
sources:
  - https://www.routledge.com/The-Art-of-Game-Design-A-Book-of-Lenses-Third-Edition/Schell/p/book/9781138632059
  - https://www.jenovachen.com/flowingames/Flow_in_games_final.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Difficulty curve design

**Goal:** challenge rises with player skill so the player stays between boredom and
anxiety (the flow channel), with rhythm rather than a straight line.

Schell (2nd ed.) ch10 adapts Csikszentmihalyi's flow channel: plot challenge against skill; too
much challenge = anxiety, too little = boredom. He argues a straight diagonal is dull
and recommends a **sawtooth**: rising tension, a reward/release, a dip, then a higher
peak. Jenova Chen's "Flow in Games" thesis discusses fitting the channel to different
players.

## Procedure
1. **List challenges in order** (levels, encounters, puzzles) and give each a difficulty
   estimate (1-10) from designers.
2. **Plot them.** Look for: flat stretches (boredom), cliffs (sudden spikes), and
   missing releases after peaks.
3. **Shape the sawtooth:** each section ramps up, peaks (boss, hard puzzle), then
   drops with a reward/new ability before climbing again. Baseline rises section to
   section.
4. **Replace estimates with data:** per challenge, record failure count, time to
   complete and quit rate in playtests/telemetry. Real difficulty often differs a lot
   from designer estimates; designers are experts at their own game.
5. **Fix outliers:** spikes with high quit rates get smoothed (teaching step before,
   checkpoint, tuning); flat stretches get new mechanics or tighter tuning.

## Signals table
| Signal | Likely meaning |
|---|---|
| high quit rate at one point | spike or unclear goal |
| near-zero failures for a long stretch | boredom zone |
| many failures, low quits | satisfying challenge (often fine) |
| failure count falls on retries | players are learning: good |
| failure count flat across retries | unfair/unclear challenge |

## Gotchas
- One curve cannot fit all players; combine with difficulty options and dynamic
  adjustment (see `creative-arts.game-design.systems-and-mechanics.dynamic-difficulty-adjustment`).
- New mechanics add difficulty even when numbers stay the same; account for learning load.
- Late-game difficulty often collapses because player power outpaces content (see
  `creative-arts.game-design.systems-and-mechanics.power-curves-and-horizontal-progression`).

## Verify
- [ ] Planned curve plotted with sawtooth peaks and releases.
- [ ] Actual failure/time/quit data plotted on the same axis.
- [ ] Every spike with a high quit rate has a fix.
