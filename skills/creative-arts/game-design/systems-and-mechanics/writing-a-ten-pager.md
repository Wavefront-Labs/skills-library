---
id: creative-arts.game-design.systems-and-mechanics.writing-a-ten-pager
name: writing-a-ten-pager
category: creative-arts
field: game-design
product: systems-and-mechanics
tags: [game-design, ten-pager, game-design-document, gdd, rogers, documentation, design-overview, preproduction]
level: practitioner
status: draft
description: "Write a ten-pager (Rogers): a ten-page game overview covering concept, story, gameplay, mechanics, enemies, cutscenes, bonus materials, sitting between the one-sheet and the full GDD."
sources:
  - https://www.wiley.com/en-us
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Writing a ten-pager

**Goal:** a ten-page overview of the game that lets the whole team and stakeholders
understand its scope and content before the detailed GDD is written.

Scott Rogers (Level Up!) recommends a staged documentation path: one-sheet, ten-pager,
then the full GDD. The ten-pager stays short enough to actually be read.

## Page plan (adapted from Rogers' outline)
| Page | Content |
|---|---|
| 1 | Title page: title, platform, target audience, target rating, ship date |
| 2 | Game outline: story summary and game flow in brief |
| 3 | Character: the player character, their abilities, why they're interesting |
| 4 | Gameplay: what the player does, genre conventions used, the 3Cs |
| 5 | Game world: setting, locations, how they connect (map) |
| 6 | Game experience: how it feels, the first minutes, UI and camera |
| 7 | Gameplay mechanics: core mechanics, hazards, power-ups, collectibles |
| 8 | Enemies: types, bosses |
| 9 | Cutscenes and story beats |
| 10 | Bonus materials: unlockables, replay value, monetisation if any |
Adjust pages to your genre (a strategy game needs economy and systems pages, not
cutscenes); keep the count.

## Writing rules
- **Diagrams and mock-ups over prose:** map, loop diagram, screen mock-up, flowchart.
- **Answer "what" not "how":** implementation detail belongs in feature specs.
- **Name the pillars and essential experience** on page 2 so every page can be checked
  against them.
- **Mark unknowns** explicitly (TBD with owner) rather than inventing.
- **Version it** and keep it updated during pre-production; it becomes the onboarding
  document for new hires.

## Gotchas
- Ten-pagers that become 30 pages are GDDs with no structure; move detail out to
  linked specs.
- Writing it in isolation produces a document nobody owns; review page by page with the
  leads for each discipline.
- Do not front-load lore; readers need gameplay first.

## Verify
- [ ] Ten pages (or fewer), each with at least one visual.
- [ ] Pillars and essential experience stated up front.
- [ ] Every discipline lead has reviewed and signed off their pages.
- [ ] Unknowns listed with owners.
