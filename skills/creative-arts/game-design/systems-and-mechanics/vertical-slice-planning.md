---
id: creative-arts.game-design.systems-and-mechanics.vertical-slice-planning
name: vertical-slice-planning
category: creative-arts
field: game-design
product: systems-and-mechanics
tags: [game-design, vertical-slice, game-prototyping, prototype-iteration, preproduction, milestone, production-planning, greenlight, scope]
level: advanced
status: draft
description: "Plan a game vertical slice: choose the representative slice, define final-quality acceptance criteria, separate it from a horizontal slice, and avoid the throwaway-polish trap."
sources:
  - https://www.gdcvault.com/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Vertical slice planning

**Goal:** a short, final-quality section of the game that proves the core experience,
the production pipeline and the target quality bar, used to greenlight full production
or secure funding.

## Vertical vs horizontal slice
- **Vertical slice:** a small amount of content (one level, 10-20 minutes) through
  *every* layer at shipping quality: mechanics, art, audio, UI, narrative, performance.
- **Horizontal slice (or "first playable" / alpha-style):** the whole game's structure
  at low fidelity, every level blocked out, no polish. Proves scope and flow.
Many teams need both; know which one a milestone asks for.

## Choosing the slice
- Representative of the **core loop**, not a special set piece (a boss fight is
  impressive but unrepresentative).
- Exercises the **riskiest systems** (if the game lives on AI companions, the slice must
  include them).
- Contains a beginning, middle and end so it can be played cold.

## Acceptance criteria (write before production)
| Area | Criterion example |
|---|---|
| Experience | 4/5 cold testers complete it and name the pillar feeling unprompted |
| Mechanics | all core verbs in, tuned; no placeholder rules |
| Art/audio | final-quality assets for all in-slice content |
| Performance | target framerate on target hardware |
| Pipeline | asset time per unit measured (minutes per prop, days per level) |
The **pipeline measurements** are the most valuable output: multiply them out to cost
the full game.

## Gotchas
- **Hand-crafted polish that cannot scale** (a heroically lit level made by the art
  director over three weeks) proves nothing about production. Build it the way the full
  game will be built.
- Slices that become marketing demos drift toward spectacle; keep the acceptance list.
- Starting a vertical slice before the core loop is fun is premature; prototype first.

## Verify
- [ ] Slice choice justified against core loop and riskiest systems.
- [ ] Acceptance criteria signed off before production.
- [ ] Pipeline per-unit costs measured and extrapolated to the full game.
