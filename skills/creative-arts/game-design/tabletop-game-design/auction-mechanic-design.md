---
id: creative-arts.game-design.tabletop-game-design.auction-mechanic-design
name: auction-mechanic-design
category: creative-arts
field: game-design
product: tabletop-game-design
tags: [game-design, tabletop-game-design, auction-mechanics, bidding, open-auction, sealed-bid, dutch-auction, once-around, board-game-mechanisms, valuation]
level: practitioner
status: draft
description: "Choose and tune auction mechanics for tabletop games: open, once-around, sealed-bid, Dutch and turn-order auctions, money flow, and avoiding overlong or runaway bidding."
sources:
  - https://boardgamegeek.com/boardgamemechanic/2012/auctionbidding
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Auction mechanic design

**Goal:** auctions that create valuation decisions and player interaction, at a pace
that keeps the table engaged.

Engelstein and Shalev's *Building Blocks* catalogue many auction types; the choice
changes pace, information and how much skill valuation requires.

## Auction types
| Type | How it works | Character |
|---|---|---|
| Open (English) | bid up until all pass | dramatic, can run long |
| Once-around | each player bids once in order | fast; position matters |
| Sealed bid | simultaneous secret bids | bluffing, no info during bidding |
| Dutch | price drops until someone takes it | tension, fast |
| Fixed-price / first-come | take at price | not really an auction; tempo choice |
| Turn-order auction | bid for turn position | indirect valuation |
| Multiple-lot / simultaneous | bid across several items at once | complex |

## Design decisions
1. **Where does money go?** To the bank (sink), to other players (redistribution,
   which helps opponents), or to the seller (the active player profits from others).
2. **Money supply:** how much enters per round; too much = everything sells high; too
   little = auctions stall.
3. **Information:** can players see others' money? Hidden money adds bluffing but
   reduces calculable decisions.
4. **Tie-breaks:** state them (turn order, first bidder).
5. **Pace:** cap open auctions (one bid per player per round, minimum increments) if
   they run long.

## Tuning
- Track final prices per lot type across playtests; if a lot always sells at the same
  price, valuation is trivial; if wildly varying, players may lack information to value.
- Watch for runaway leaders who can outbid everyone; money as both currency and score
  creates negative feedback (spending reduces score).

## Gotchas
- Valuation-heavy games are hard for new players; provide reference values or price
  guides.
- Auctions with money flowing to other players can create kingmaking.

## Verify
- [ ] Auction type chosen for desired pace and information.
- [ ] Money flow and supply modelled for a full game.
- [ ] Average auction duration measured.
- [ ] Final price distribution per lot type reviewed.
