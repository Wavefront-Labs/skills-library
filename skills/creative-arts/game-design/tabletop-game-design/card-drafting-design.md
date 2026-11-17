---
id: creative-arts.game-design.tabletop-game-design.card-drafting-design
name: card-drafting-design
category: creative-arts
field: game-design
product: tabletop-game-design
tags: [game-design, tabletop-game-design, card-drafting, pick-and-pass, open-drafting, hate-drafting, board-games]
level: practitioner
status: draft
description: "Design card drafting: pick-and-pass vs open markets, pack size per player count, signalling and hate-drafting, card-pool tuning and the draft as a hidden engine builder."
sources:
  - https://boardgamegeek.com/browse/boardgamemechanic
  - https://magic.wizards.com/en/news/making-magic
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Card drafting

**Goal:** each pick is a real trade-off between what helps me, what blocks you, and what
might come back around.

## Draft types
| Type | Example | Feel |
|---|---|---|
| Pick-and-pass (closed) | 7 Wonders, Sushi Go, Magic booster draft | simultaneous, low downtime, reading neighbours |
| Open market / river | Ticket to Ride face-up cards, Splendor | visible, interactive, slower |
| Pick order by position | Kingdomino, Race for the Galaxy roles | built-in catch-up |
| Draft then play | Magic, Fantasy Realms variants | deck/tableau building in two phases |

## Tuning levers
1. **Pack size vs players:** 7 Wonders uses 7 cards per age for 3-7 players; seeing a
   pack twice (pack size > player count) allows planning ("will this wheel?").
2. **Pass direction:** alternate each round so no one always feeds the same neighbour.
3. **Card pool composition:** count cards per strategy; each strategy needs enough
   support that two players can share it at the table's max count.
4. **Hate-drafting value:** taking a card only to deny it should be sometimes right, not
   always; if denial beats building, interaction is too high.
5. **Last card:** decide whether the last card is played, discarded or passed.

## Procedure
1. Spreadsheet card pool by strategy tag and cost.
2. Run drafts with bots picking by a simple rule (highest value) to find over-picked cards.
3. Watch pick timing in live tests; picks over ~20 s signal unclear evaluation or too
   many options per pack.
4. Iterate cards that are always first picks (too strong or too flexible).

## Gotchas
- Large packs with many similar cards cause analysis paralysis; trim to the meaningful.
- Drafting with strong signalling needs consistent pack contents; random packs weaken reading.
- Two-player pick-and-pass needs a variant (burn a card, dummy player), not the base rules.

## Verify
- [ ] Each strategy is draftable by two players at max count.
- [ ] No card is first pick in most test drafts.
- [ ] Average pick time under target.
