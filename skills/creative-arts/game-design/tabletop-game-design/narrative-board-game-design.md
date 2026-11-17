---
id: creative-arts.game-design.tabletop-game-design.narrative-board-game-design
name: narrative-board-game-design
category: creative-arts
field: game-design
product: tabletop-game-design
tags: [game-design, tabletop-game-design, narrative-board-games, storybook-games, paragraph-books, campaign-games, branching-story]
level: practitioner
status: draft
description: "Design narrative and storybook board games: paragraph books and story decks, branching via keywords, encounter writing, campaign saves and balancing reading against play."
sources:
  - https://boardgamegeek.com/
  - https://www.routledge.com/The-Game-Narrative-Toolbox/Heussner-Finley-Hepler-Lemay/p/book/9781138778382
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Narrative and storybook board games

**Goal:** a board game whose story unfolds through play and choices (Tales of the Arabian
Nights, Sleeping Gods, Forgotten Waters, Gloomhaven, Arkham Horror LCG, Near and Far).

## Delivery methods
| Method | Notes |
|---|---|
| Paragraph / storybook | numbered entries; outcomes direct to other entries |
| Story card decks | cards revealed in order or on triggers |
| Scenario books | each scenario has setup, story intro, conclusion |
| App narration | voice, branching, hidden state (Mansions of Madness 2e, Forgotten Waters' app) |
| Keywords / status cards | record story state ("You are Cursed") |

## Structure
1. **Encounter template:**
   ```
   112. The Drowned Bell
   Story text (60-120 words).
   CHOICES: Ring the bell -> roll Spirit 4+: go to 113, else 114.
            Leave -> continue exploring.
   If you have keyword TIDE-MARKED, go to 115 instead.
   ```
2. **Keywords** carry consequences between encounters and sessions; list them in a
   glossary and on the save sheet.
3. **Branch and bottleneck:** branches converge at chapter ends to keep the book finite.
4. **Mechanics in story:** skill tests resolve choices; outcomes give resources, wounds,
   keywords, map changes.

## Balancing reading and play
- Keep entries short; long text with one player reading aloud stalls everyone else.
  Rotate the reader role.
- Every entry ends with a decision or a mechanical change.
- Mix narrative turns with board turns so non-readers act often.

## Campaign save
- Save sheet: keywords, quest progress, character state, current entry; box storage that
  preserves setup.

## Writing and QA
- Track the paragraph graph in a tool (spreadsheet of entry -> targets, or Twine/yEd
  graph) to find orphans and dead ends.
- Write to the reading level and tone of the target audience; read entries aloud in testing.

## Gotchas
- Cross-references to wrong numbers are the most common error; generate references
  from the graph data, never type them by hand.
- Choices without information are coin flips; foreshadow consequences.
- Replay value drops once paragraphs are known; random encounter decks help.

## Verify
- [ ] Paragraph graph has no orphans or dead ends.
- [ ] Every entry ends in a choice or a mechanical effect.
- [ ] Average reading time per turn measured in tests.
