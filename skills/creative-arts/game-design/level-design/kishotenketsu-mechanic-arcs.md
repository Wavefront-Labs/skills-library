---
id: creative-arts.game-design.level-design.kishotenketsu-mechanic-arcs
name: kishotenketsu-mechanic-arcs
category: creative-arts
field: game-design
product: level-design
tags: [game-design, level-design, kishotenketsu, mechanic-escalation, level-pacing, introduce-develop-twist-conclude, nintendo, super-mario-3d-world, one-mechanic-per-level]
level: practitioner
status: draft
description: "Structure a level around one mechanic using kishotenketsu (introduce, develop, twist, conclude), as described for Nintendo's Super Mario 3D World level design."
sources:
  - https://en.wikipedia.org/wiki/Kish%C5%8Dtenketsu
  - https://www.gdcvault.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Kishotenketsu mechanic arcs

**Goal:** a short level that fully explores one mechanic with a satisfying arc, without
needing story or conflict to carry it.

Kishōtenketsu is a four-part structure from Chinese and Japanese poetry and narrative:
**ki** (introduction), **shō** (development), **ten** (twist), **ketsu** (conclusion).
Koichi Hayashida, a director of Super Mario 3D World, described the team building
levels around a gimmick in this way (as reported in interviews and widely analysed).

## Applying it to a mechanic
| Phase | Level design job | Example (moving platform that flips when you jump) |
|---|---|---|
| Ki - introduce | show the mechanic safely, no fail state or a trivial one | one flipping platform over solid ground |
| Shō - develop | build on it; harder layouts, combine with known elements | platforms over gaps, sequences, timing |
| Ten - twist | change how the mechanic is understood or used | now the flip is needed to dodge projectiles, or flips reveal hidden paths |
| Ketsu - conclude | a final, satisfying test or celebration | flag at the end of a skilful run; demonstrate mastery |

## Procedure
1. Pick **one mechanic** (or one interaction) per level/section.
2. Sketch four sections following the table; each should take a fraction of the level
   time (introduction short, development longest).
3. Ensure the **twist** genuinely changes perception, not just difficulty.
4. **Retire the mechanic** after the level (or reuse rarely later), so each level feels
   fresh. This is a content-hungry approach: plan enough mechanics.
5. Playtest: can players describe the twist afterwards? If not, it was not readable.

## Gotchas
- Introductions that are too long bore experienced players; keep ki brief.
- Twists that require knowledge not taught in ki/shō feel unfair.
- Not every game wants one-mechanic levels; systemic games build on combinations
  instead (see `creative-arts.game-design.systems-and-mechanics.systemic-design-interactions`).

## Verify
- [ ] One mechanic per level, documented.
- [ ] Four phases identifiable in the layout.
- [ ] Twist changes how the mechanic is used.
- [ ] Testers can explain the twist after playing.
