---
id: creative-arts.game-design.level-design.lighting-for-player-guidance
name: lighting-for-player-guidance
category: creative-arts
field: game-design
product: level-design
tags: [game-design, level-design, lighting-guidance, player-guidance, wayfinding, value-contrast, light-pools, moths-to-flame, readability, lighting-design]
level: practitioner
status: draft
description: "Use light and value contrast to guide players: lit exits and paths, pools of light as waypoints, colour temperature for safe vs danger, and greyscale tests for readability."
sources:
  - https://www.routledge.com/An-Architectural-Approach-to-Level-Design-Second-edition/Totten/p/book/9780815361367
  - https://www.gdcvault.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Lighting for player guidance

**Goal:** players move where you intend without arrows or text, because light draws the
eye to paths, exits and points of interest.

People tend to move toward light and toward the brightest, highest-contrast area in
view (Totten discusses lighting as a tool for molding player behaviour). Level design
uses this to guide navigation.

## Techniques
| Technique | Use |
|---|---|
| Lit exit | brightest point in a room is the way forward |
| Pools of light | sequential pools along a path act as waypoints |
| Silhouette backlighting | frame doorways or landmarks against light |
| Colour temperature | warm = safe/home, cool or red = danger (be consistent) |
| Contrast with dark | darkness hides optional/forbidden areas; slight light hints at secrets |
| Light shafts / god rays | point at objectives or interactables |
| Flicker/motion | draws attention; use sparingly |

## Procedure
1. **Mark the intended path** on the blockout; place the key guidance lights before
   decorative lighting.
2. **Greyscale/value test:** desaturate a screenshot from each decision point. The path
   should still be the most readable area.
3. **Squint test:** blur the image; the brightest blob should be where you want the
   player to go.
4. **Lighting artist handoff:** document which lights are gameplay-critical so mood
   passes do not remove them.
5. **Playtest** without HUD markers; watch where players turn first in each space.

## Gotchas
- Mood lighting passes often flatten contrast and break guidance late; protect critical
  lights.
- Bright decorative objects (lamps, signs) compete with the path; tone them down or put
  them on the path.
- Dark levels need accessibility options (brightness/gamma) and must still be navigable.

## Verify
- [ ] Guidance lights placed and documented per decision point.
- [ ] Desaturated screenshots show the path as the highest-contrast area.
- [ ] Playtesters choose the intended direction first in most spaces without markers.
