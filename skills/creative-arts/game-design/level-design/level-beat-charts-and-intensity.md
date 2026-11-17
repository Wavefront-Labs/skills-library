---
id: creative-arts.game-design.level-design.level-beat-charts-and-intensity
name: level-beat-charts-and-intensity
category: creative-arts
field: game-design
product: level-design
tags: [game-design, level-design, beat-chart, intensity-graph, level-pacing, pacing, rogers, set-piece, rest-areas, tension]
level: practitioner
status: draft
description: "Plan a level's pacing with a beat chart (Rogers) and an intensity graph: list beats, rate intensity, alternate tension and rest, and compare against playtest timings."
sources:
  - https://www.routledge.com/An-Architectural-Approach-to-Level-Design-Second-edition/Totten/p/book/9780815361367
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Level beat charts and intensity graphs

**Goal:** a level whose pacing is planned beat by beat, alternating intensity and rest,
before anything is built.

Rogers (Level Up!) recommends a **beat chart**: a table listing every level with its
setting, story beats, mechanics introduced, enemies, rewards and pacing, used to see the
whole game's flow at once. The same idea zoomed in gives a per-level beat list.

## Per-level beat list
| # | Beat | Type | Intensity 1-10 | Mechanics | Est. minutes |
|---|---|---|---|---|---|
| 1 | arrival vista | rest / orientation | 2 | - | 1 |
| 2 | first patrol encounter | combat | 5 | stealth intro | 3 |
| 3 | courtyard puzzle | puzzle | 3 | lever + timing | 4 |
| 4 | ambush in library | combat | 7 | new enemy | 3 |
| 5 | safe room | rest | 1 | save, shop | 1 |
| 6 | collapse escape | set piece | 9 | chase | 2 |

## Intensity graph
Plot intensity against time from the beat list. Check:
- **Alternation:** peaks followed by valleys (rest, exploration, story).
- **Rising baseline** across the level, climax near the end.
- **No long plateaus** at either high (fatigue) or low (boredom) intensity.
- Variety of beat types; three combat beats in a row at the same intensity reads as
  padding.

## Procedure
1. Write the beat list from the level's goals and the game-level beat chart.
2. Plot the intensity graph; adjust order and content.
3. Build the blockout following beats; time each beat in playtest.
4. Overlay actual timings and tester intensity ratings; revise.

## Gotchas
- Designer minute estimates are usually too short for first-time players; measure.
- Intensity is subjective; use playtester ratings and biometrics/observation where
  possible, not just designer numbers.
- Story beats placed at high-intensity moments get missed; put exposition in valleys.

## Verify
- [ ] Beat list with types, intensity and estimates per level.
- [ ] Intensity graph alternates and builds to a climax.
- [ ] Actual beat timings from playtest overlaid and reviewed.
