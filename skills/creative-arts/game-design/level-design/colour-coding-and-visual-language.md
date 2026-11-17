---
id: creative-arts.game-design.level-design.colour-coding-and-visual-language
name: colour-coding-and-visual-language
category: creative-arts
field: game-design
product: level-design
tags: [game-design, level-design, color-coding, visual-language, affordances, climbable-surfaces, yellow-paint, player-guidance, consistency, accessibility]
level: practitioner
status: draft
description: "Define a level visual language (climbable, breakable, interactable, hazard) with consistent colour, shape and material cues, document it, and test it with new players."
sources:
  - https://www.routledge.com/An-Architectural-Approach-to-Level-Design-Second-edition/Totten/p/book/9780815361367
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Colour coding and visual language

**Goal:** players recognise what they can climb, break, use or must avoid at a glance,
because the game uses one consistent set of visual cues.

## Build the language
| Function | Cue options |
|---|---|
| Climbable / grabbable ledge | painted edges (the much-discussed "yellow paint"), worn texture, specific trim |
| Breakable | cracks, distinct material, different colour |
| Interactable | highlight on approach, consistent shape/icon |
| Hazard | red/orange, warning stripes, sound |
| Door you can open vs scenery door | handle/light vs no handle |
| Collectible | glow, bob, sparkle |

## Rules
1. **One meaning per cue.** If yellow means climbable, nothing decorative is yellow.
2. **Shape + colour + material**, never colour alone (colour-blind players; Hodent's
   point that redundant cues improve perception).
3. **Teach early, then remove crutches gradually** if desired (strong cues in tutorial,
   subtler integrated cues later), but stay consistent.
4. **Document in a style sheet** shared with environment art.
5. **Audit** every level for false positives (decorative objects that look interactable)
   and false negatives (interactables that look like scenery).

## The yellow-paint debate
Strong, diegetically awkward cues (painted ledges) improve readability but can feel
immersion-breaking. Options: integrate cues into the world's materials, offer a
toggle in accessibility settings, or rely on strong cues only on critical paths. The
key is consistency, whichever level of subtlety is chosen.

## Gotchas
- Art passes add detail that drowns cues; re-test after each art pass.
- Players stop trusting the language after one inconsistency ("I couldn't climb that
  yellow pipe").
- Different lighting conditions change perceived colour; test in dark areas.

## Verify
- [ ] Visual language style sheet written.
- [ ] No colour-only cues.
- [ ] False-positive/false-negative audit done per level.
- [ ] New players correctly identify interactables in a screenshot test.
