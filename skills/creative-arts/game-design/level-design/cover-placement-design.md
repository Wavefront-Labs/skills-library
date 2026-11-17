---
id: creative-arts.game-design.level-design.cover-placement-design
name: cover-placement-design
category: creative-arts
field: game-design
product: level-design
tags: [game-design, level-design, cover-design, cover-shooter, encounter-design, low-cover, high-cover, flanking, destructible-cover, combat-spaces]
level: practitioner
status: draft
description: "Place cover in combat spaces: low vs high cover, spacing between cover points, flanking lanes, angles that prevent safe camping, and destructible cover to force movement."
sources:
  - https://www.gdcvault.com/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cover placement design

**Goal:** combat spaces where cover protects but never makes a position permanently
safe, so players move, flank and make decisions.

## Building blocks
| Element | Rule of thumb |
|---|---|
| Low cover | below crouch eye line from player metrics; allows shooting over |
| High cover | blocks standing player; shoot around corners |
| Cover spacing | close enough to sprint between under fire (measure in seconds of exposure) |
| Flank lanes | routes that reach the side of a cover cluster |
| Angles | cover protects from one direction; enemies elsewhere expose you |
| Destructible cover | degrades over time, forcing relocation |
| Height | high ground counters low cover |

## Procedure
1. **Use the metrics** (low/high cover heights) from
   `creative-arts.game-design.level-design.player-metrics-and-grid`.
2. **Draw a cover map** top-down: mark cover pieces with protected direction arrows.
3. **Exposure test:** for each cover spot, list the enemy positions that can hit it.
   A spot hit from nowhere is a camping spot; one hit from everywhere is useless.
4. **Movement chain:** ensure a chain of cover leads forward toward the objective, plus
   at least one flank chain.
5. **AI usage:** enemies use the same cover (navigation markers); check AI picks sensible
   spots and does not cluster.
6. **Playtest:** heatmap of player positions; look for spots where players sit the whole
   fight.

## Gotchas
- Waist-high walls everywhere make spaces read as artificial; integrate cover into the
  setting (cars, crates, rubble, architecture).
- Cover that looks protective but isn't (thin fences, glass) must read as such.
- Too much cover stalls fights; too little makes them run-and-gun. Tune per encounter.

## Verify
- [ ] Cover map with protected directions exists.
- [ ] No cover spot is safe from every enemy position.
- [ ] Forward and flank cover chains exist.
- [ ] Position heatmaps show movement, not camping.
