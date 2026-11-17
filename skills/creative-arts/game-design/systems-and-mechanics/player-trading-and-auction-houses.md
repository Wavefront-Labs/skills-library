---
id: creative-arts.game-design.systems-and-mechanics.player-trading-and-auction-houses
name: player-trading-and-auction-houses
category: creative-arts
field: game-design
product: systems-and-mechanics
tags: [game-design, player-trading, auction-house, game-economy, resource-economy, mmo, marketplace, transaction-tax, real-money-trading, bind-on-pickup]
level: advanced
status: draft
description: "Design player-to-player trading and auction houses: what is tradeable, listing fees and taxes as sinks, bind rules, price discovery, and defences against bots and real-money trading."
sources:
  - https://www.routledge.com/Game-Balance/Schreiber-Romero/p/book/9781498799577
  - https://www.eveonline.com/news
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Player trading and auction houses

**Goal:** a player market that creates interesting economic play (specialisation,
trading, crafting for profit) without inflation, duping, bot farming or real-money
trading taking over.

## Design decisions
| Decision | Options | Effect |
|---|---|---|
| What can be traded | everything / materials only / cosmetics only | more tradeable = stronger market, weaker personal progression |
| Bind rules | bind-on-pickup, bind-on-equip, account-bound | keeps top rewards earned, not bought |
| Venue | direct trade window, global auction house, regional markets | global = efficient prices; regional = arbitrage and travel gameplay |
| Fees | listing deposit, sales tax | primary gold sink in many MMOs |
| Price info | price history visible / hidden | visible = efficient, less room for trader skill |
| Supply | NPC vendors buy/sell floors and ceilings | stabilises prices |

## Procedure
1. **Classify items:** tradeable commodities (materials, consumables) vs bound
   progression items.
2. **Set transaction taxes** as a sink sized to offset expected gold inflow (start by
   modelling total gold created per day vs removed).
3. **Set NPC price floors** (vendor sell price) and ceilings (vendor buy price) for
   commodities to stop crashes and spikes.
4. **Plan anti-abuse:** trade limits for new accounts, delayed delivery for high-value
   trades, logging for rollback, rate limits on listings.
5. **Monitor:** price indices for a basket of goods, money supply, velocity. EVE Online
   publishes a monthly economic report with such metrics - a model of what to track.

## Gotchas
- **Duplication exploits** crash market economies fast; design for audited, atomic
  item transfers and keep the ability to roll back.
- Real-money trading (gold selling) follows any tradeable valuable; bind rules and trade
  restrictions are the main defences.
- Fully tradeable best-in-slot gear turns progression into shopping; most games bind
  top rewards.
- Market-maker players will find every arbitrage; that can be desirable emergent play.

## Verify
- [ ] Tradeability and bind rules listed per item class.
- [ ] Modelled daily gold creation vs removal (including taxes) roughly balanced.
- [ ] Anti-abuse measures specified; rollback logging in place.
- [ ] Price-index dashboard defined.
