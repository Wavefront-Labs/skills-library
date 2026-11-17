---
id: creative-arts.game-design.narrative-design.narrative-beat-sheets
name: narrative-beat-sheets
category: creative-arts
field: game-design
product: narrative-design
tags: [game-design, narrative-design, narrative-beat-sheet, beat-sheet, level-narrative, cross-discipline, story-beats]
level: practitioner
status: draft
description: "Write narrative beat sheets shared with level and systems design: one row per beat with location, gameplay, emotion, delivery method and dependencies, so all teams build to it."
sources:
  - https://www.routledge.com/The-Game-Narrative-Toolbox/Heussner-Finley-Hepler-Lemay/p/book/9781138778382
  - https://www.routledge.com/An-Architectural-Approach-to-Level-Design-Second-Edition/Totten/p/book/9780815361367
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Narrative beat sheets

**Goal:** a shared document where narrative, level and systems design agree what happens
where, what the player does there, and how it should feel.

## Columns
| # | Beat | Location / level | Player activity | Emotion target | Delivery | New mechanic | Dependencies | Owner |
|---|---|---|---|---|---|---|---|---|
| 07 | Mara reveals the map is fake | Lighthouse top | climb, then dialogue | betrayal, urgency | in-engine cutscene + choice | none | 06 complete, VO line set M07 | narrative |
| 08 | Escape the collapsing lighthouse | Lighthouse interior | timed traversal | panic, then relief | scripted collapse, barks | crumble floors | 07, collapse tech | level |

Rogers' level beat charts use the same idea at level scale; the narrative sheet is the
game-scale spine those charts hang from.

## Procedure
1. Narrative drafts the beat list (story only) from the outline.
2. Workshop with level and systems: for each beat fill location, activity, new mechanic.
   Change beats that have no play; a beat that is only a cutscene is a warning.
3. Mark the **emotion target** and check the sequence for variety (an interest curve:
   no three high-intensity beats in a row without relief).
4. Assign **delivery method** (cutscene, dialogue, barks, environment, documents, gameplay).
5. Record dependencies (prior beats, tech, assets) so production can schedule.
6. Make it the single source: level briefs and quest specs link to beat ids.

## Keeping it alive
- Version the sheet; when a level is cut or moved, update the sheet first.
- Review weekly in the cross-discipline sync; red-flag beats whose dependencies slipped.
- Colour code status: written, blocked out, playable, final.

## Gotchas
- Beat sheets written by narrative alone turn into a screenplay that levels cannot fit.
- Too much granularity (every line) makes the sheet unreadable; one row per beat, minutes not seconds.

## Verify
- [ ] Every beat has a location, player activity and delivery method.
- [ ] Emotion column shows rhythm, not a flat line.
- [ ] Level briefs reference beat ids.
