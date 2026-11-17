---
id: creative-arts.game-design.tabletop-game-design.bill-of-materials-and-manufacturing
name: bill-of-materials-and-manufacturing
category: creative-arts
field: game-design
product: tabletop-game-design
tags: [game-design, tabletop-game-design, bill-of-materials, game-manufacturing, component-design, cogs, msrp, print-run, production, board-game-publishing]
level: advanced
status: draft
description: "Build a board game bill of materials, estimate manufacturing cost, and use the cost-to-price multiplier to make component decisions before talking to manufacturers."
sources:
  - https://stonemaiergames.com/kickstarter/
  - https://www.thegamecrafter.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Bill of materials and manufacturing

**Goal:** know what the game costs to make and what it must sell for, early enough that
component choices are design decisions rather than surprises.

## Bill of materials (BOM)
List every component with specs:
| Component | Qty | Spec |
|---|---|---|
| Cards | 110 | poker size, 300 gsm black-core, linen finish |
| Board | 1 | quad-fold, 2 mm greyboard, 50 x 50 cm |
| Punchboards | 2 | 2 mm, die-cut tokens |
| Wooden cubes | 60 | 8 mm, 5 colours |
| Custom dice | 4 | d6, printed |
| Rulebook | 1 | 16 pp, A4, full colour |
| Box | 1 | two-piece, size, insert type |

## Cost to price
- Manufacturers quote **unit cost (COGS)** by quantity; cost per unit drops sharply with
  larger print runs.
- A widely used industry rule of thumb is that MSRP is several times the
  landed manufacturing cost (often quoted as roughly 4-5x for retail distribution,
  because distributors and retailers each take a margin). Direct-to-consumer
  (crowdfunding, web store) margins differ; Jamey Stegmaier's Kickstarter lessons
  discuss the economics in depth.
- Add freight, fulfilment, duties/VAT, and platform fees for a true landed cost.

## Component decisions
1. Price the "dream" BOM and the "lean" BOM; compare MSRP outcomes.
2. Biggest cost drivers are usually custom components (miniatures, custom dice, special
   shapes) and box size (also drives shipping).
3. Standard sizes and stock components (cubes, standard card sizes) are cheaper.
4. Check card count against the manufacturer's sheet layout (cards are printed on
   sheets in fixed multiples, e.g. 54 or 55 per sheet for poker size at some factories);
   rounding up to full sheets wastes nothing extra.

## Procedure
1. Draft the BOM during prototyping; update with each design change.
2. Request quotes from 2-3 manufacturers at 2-3 print-run sizes.
3. Model cost per unit, MSRP, margin at each run size.
4. Decide component changes (and design changes if needed) from the numbers.

## Gotchas
- Shipping and tariffs can exceed manufacturing costs per unit for heavy games;
  quote freight early.
- Quotes change with paper and freight markets; date every quote.
- Plastic inserts and vacuum trays add cost; cardboard inserts or none are options.

## Verify
- [ ] BOM with full specs.
- [ ] Quotes from multiple manufacturers at multiple run sizes.
- [ ] Landed cost and target MSRP modelled per channel.
