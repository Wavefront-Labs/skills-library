---
id: creative-arts.game-design.narrative-design.storylets-and-quality-based-narrative
name: storylets-and-quality-based-narrative
category: creative-arts
field: game-design
product: narrative-design
tags: [game-design, narrative-design, quality-based-narrative, storylets, qbn, salience-based-narrative, failbetter, branching-narrative, modular-narrative, state-tracking]
level: advanced
status: draft
description: "Structure narrative as storylets gated by qualities (QBN): define qualities, write storylets with prerequisites and effects, and avoid branching explosion."
sources:
  - https://emshort.blog/2019/11/29/storylets-you-want-them/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Storylets and quality-based narrative

**Goal:** a narrative made of modular pieces that become available based on world and
player state, so content combines flexibly instead of growing as a branching tree.

**Quality-based narrative (QBN)**, as described by Failbetter Games (Fallen London),
gates content on numeric "qualities" (stats, story progress, relationships, items).
Emily Short's "Storylets: You Want Them" (2019) surveys storylet systems: small units
of content with prerequisites and effects, selected from a pool.

## Elements
| Element | Example |
|---|---|
| Quality | `Suspicion: 0-10`, `MetTheDuke: 1`, `Act: 2`, `Gold: 50` |
| Storylet | a scene/card with text and choices |
| Prerequisites | `Act == 2 and Suspicion < 5` |
| Effects | `Suspicion += 2`, `MetTheDuke = 1` |
| Selection | which eligible storylets are shown (all, a deck draw, highest salience) |

## Procedure
1. **Define qualities** that represent what matters to the story (progress, relationships,
   resources, flags). Prefer counters over many booleans.
2. **Write storylets** with explicit prerequisites and effects; each should make sense
   whenever its prerequisites are met (write for unknown prior context).
3. **Plan progression qualities** (`Act`, `Chapter`) to pace major arcs, and
   **resource qualities** to create choices (spend Gold or Suspicion to proceed).
4. **Selection rule:** show all eligible storylets (menu), draw from a deck (Fallen London's
   opportunity deck), or pick the most specific match (salience-based dialogue).
5. **Tooling:** keep storylets in a spreadsheet or database with columns for
   prerequisites and effects; write a script that lists storylets reachable from a
   given state and flags unreachable ones.

## Gotchas
- **Context assumptions:** a storylet that references events the player may not have
  seen breaks immersion; check prerequisites encode them.
- Too many eligible storylets at once overwhelms; cap the visible set.
- Quality grinds (repeat storylet to raise a stat) feel tedious; vary repeatable content.

## Verify
- [ ] Quality list with ranges and meanings.
- [ ] Each storylet has explicit prerequisites and effects.
- [ ] Reachability script finds no unreachable storylets.
- [ ] Playtest shows coherent sequences across different paths.
