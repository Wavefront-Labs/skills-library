---
id: creative-arts.game-design.systems-and-mechanics.eight-kinds-of-fun-aesthetic-targets
name: eight-kinds-of-fun-aesthetic-targets
category: creative-arts
field: game-design
product: systems-and-mechanics
tags: [game-design, eight-kinds-of-fun, mda-framework, aesthetics, sensation, fantasy, narrative, challenge, fellowship, discovery, expression, submission, design-goals]
level: practitioner
status: draft
description: "Use MDA's eight kinds of fun (sensation, fantasy, narrative, challenge, fellowship, discovery, expression, submission) to set and rank a game's aesthetic targets."
sources:
  - https://users.cs.northwestern.edu/~hunicke/MDA.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Eight kinds of fun as aesthetic targets

**Goal:** replace "it should be fun" with a ranked, shared list of the specific
pleasures the game targets, so mechanics can be judged against them.

## The taxonomy (Hunicke, LeBlanc, Zubek 2004)
| Aesthetic | Game as... | Example |
|---|---|---|
| Sensation | sense-pleasure | rhythm games, juicy feedback |
| Fantasy | make-believe | being a pirate captain |
| Narrative | drama | a story that unfolds through play |
| Challenge | obstacle course | precision platformer, puzzle |
| Fellowship | social framework | co-op, party games |
| Discovery | uncharted territory | exploration, hidden systems |
| Expression | self-discovery | building, character customisation |
| Submission | pastime | idle games, solitaire, comfort play |
The paper stresses the list is "not complete"; extend it if your game targets something
else (e.g. competition as distinct from challenge).

## Procedure
1. **Pick 2-3 primary aesthetics and rank them.** The MDA paper's examples: Charades =
   fellowship, expression, challenge; Quake = challenge, sensation, competition, fantasy;
   The Sims = discovery, fantasy, expression, narrative; Final Fantasy = fantasy,
   narrative, expression, discovery, challenge, submission.
2. **Name the ones you are NOT targeting.** A pure fellowship party game should not sink
   time into narrative.
3. **For each primary aesthetic, write the dynamic that will produce it** (time pressure
   and opponent play produce challenge; shared goals and communication produce
   fellowship). Then the mechanics that create those dynamics. This is MDA designed
   backwards from the player's side (see
   `creative-arts.game-design.systems-and-mechanics.tracing-dynamics-with-mda`).
4. **Write playtest questions per aesthetic** ("Did you talk to the other players about
   strategy?" for fellowship) and observable behaviours.

## Gotchas
- Different audiences rank the same game differently; check your target audience's
  motivations (see `creative-arts.game-design.systems-and-mechanics.player-motivation-models`).
- **Submission** is a legitimate target (comfort, low-stakes repetition), not an insult;
  idle and cosy games design for it deliberately.
- Targeting all eight equally is targeting none. Rank.

## Verify
- [ ] Ranked list of 2-3 primary aesthetics plus explicit non-targets.
- [ ] Each primary aesthetic traces to named dynamics and mechanics.
- [ ] Playtest plan contains a question or observation per primary aesthetic.
