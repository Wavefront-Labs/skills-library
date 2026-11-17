---
id: creative-arts.game-design.systems-and-mechanics.elemental-tetrad-analysis
name: elemental-tetrad-analysis
category: creative-arts
field: game-design
product: systems-and-mechanics
tags: [game-design, elemental-tetrad, tetrad-analysis, schell, mechanics, story, aesthetics, technology, design-review]
level: practitioner
status: draft
description: "Review a game design with Schell's elemental tetrad: audit mechanics, story, aesthetics and technology for balance, gaps and contradictions, then rebalance."
sources:
  - https://www.routledge.com/The-Art-of-Game-Design-A-Book-of-Lenses-Third-Edition/Schell/p/book/9781138632059
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Elemental tetrad analysis

**Goal:** check that the four basic elements of the game support each other and the
theme, and that none is neglected or fighting the others.

## The four elements (Schell (2nd ed.) ch5)
- **Mechanics:** procedures and rules; what makes it a game. 
- **Story:** the sequence of events, pre-written or emergent.
- **Aesthetics:** how it looks, sounds, smells, feels; the most visible element.
- **Technology:** the materials and interactions that make it possible (paper, dice,
  engine, controller, network).
Schell draws them with aesthetics most visible and technology least visible; none is
more important than the others.

## Procedure
1. **Write one paragraph per element** describing the current design.
2. **For each pair (6 pairs), ask: do they reinforce or fight?**
   | Pair | Reinforce / fight | Note |
   |---|---|---|
   | mechanics-story | fight | story says urgent, no time pressure in rules |
   | aesthetics-technology | reinforce | low-poly look keeps mobile framerate |
3. **Ask Schell's Lens of the Elemental Tetrad questions:** Is the design using all four?
   Could one be improved to enhance the others? Are they in harmony toward the theme?
4. **Find the weakest element** and decide whether to strengthen it or deliberately
   minimise it (an abstract puzzle game may minimise story on purpose).
5. **Check technology as a design input**, not just an implementation detail: new tech
   (touch, VR, AR, haptics, a novel component like a dexterity tower) can suggest
   mechanics nobody has tried.

## Gotchas
- Teams over-index on the element their discipline owns (artists on aesthetics,
  engineers on technology). Run the review cross-discipline.
- A "story" element exists even in abstract games: the sequence of events players
  recount afterwards. Ask what story players tell.
- Technology constraints (paper, budget, target hardware) are part of the design; ignoring
  them produces designs that cannot ship.

## Verify
- [ ] Paragraph per element written.
- [ ] All six pairs rated; each "fight" has an action.
- [ ] Weakest element named with a strengthen-or-minimise decision.
