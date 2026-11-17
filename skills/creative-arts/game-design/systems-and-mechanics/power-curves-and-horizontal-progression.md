---
id: creative-arts.game-design.systems-and-mechanics.power-curves-and-horizontal-progression
name: power-curves-and-horizontal-progression
category: creative-arts
field: game-design
product: systems-and-mechanics
tags: [game-design, power-curve, horizontal-progression, vertical-progression, progression-systems, stat-scaling, level-scaling, power-creep, sidegrades]
level: advanced
status: draft
description: "Model player power over time against challenge, choose vertical (bigger numbers) vs horizontal (more options) progression, and control power creep and level scaling."
sources:
  - https://www.routledge.com/Game-Balance/Schreiber-Romero/p/book/9781498799577
  - https://gamebalanceconcepts.wordpress.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Power curves and horizontal progression

**Goal:** player power and game challenge grow in a planned relationship, and
progression adds options rather than only inflating numbers.

## Power curve vs challenge curve
Plot two lines over play time: **player power** (damage per second, effective HP, gold
per hour) and **challenge** (enemy HP x damage, required output). The gap is the felt
difficulty:
- Power ahead of challenge: player feels strong; too far ahead = boredom.
- Challenge ahead of power: tension; too far = grind wall or frustration.
Schreiber's Game Balance Concepts course frames progression as the relationship between
these curves; aim for a deliberate sawtooth (challenge spikes, then power catches up).

## Vertical vs horizontal
| | Vertical | Horizontal |
|---|---|---|
| What grows | stats, numbers, tiers | options, tools, sidegrades |
| Pros | clear sense of growth | keeps old content relevant; more builds |
| Cons | old content trivial; numbers inflate; power creep | weaker "I got stronger" feeling |
| Examples | RPG levels, gear score | new weapons with different roles, new characters |
Most games mix: vertical early (feel growth), horizontal later (keep content alive).

## Procedure
1. Choose the **curve shape** for power and challenge (linear, polynomial, exponential;
   multiplicative stacking makes exponential happen by accident).
2. Build a spreadsheet: rows = time/level, columns = player stats from all sources,
   enemy stats, ratio.
3. Mark **multiplicative stacking**: +10% from five sources is 1.61x, not 1.5x.
4. Decide on **level scaling**: none (old areas become trivial, which is satisfying),
   full (always challenging, but growth feels fake), or bounded bands.
5. For live games, cap **power creep**: new content should be sidegrades or use rotation
   (formats in card games) rather than strictly better items.

## Gotchas
- Full level scaling where enemies scale faster than the player makes leveling feel
  punishing (a well-known complaint in some open-world RPGs).
- Big number inflation breaks UI and integer limits late game; plan display formats.
- Horizontal progression needs varied challenges; if one tool solves everything, the
  other options are pointless.

## Verify
- [ ] Power and challenge curves plotted together.
- [ ] Multiplicative sources modelled correctly.
- [ ] Level scaling policy written.
- [ ] Late-game options still use early tools or content where intended.
