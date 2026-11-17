---
id: creative-arts.game-design.playtesting-and-balance.cost-curve-balancing
name: cost-curve-balancing
category: creative-arts
field: game-design
product: playtesting-and-balance
tags: [game-design, cost-curve, balance-tuning, balance-spreadsheet, card-balance, unit-balance, transitive-balance, schreiber, game-balance-concepts]
level: advanced
status: draft
description: "Balance transitive game objects (cards, units, items) with a cost curve: express costs and benefits in one currency, fit the curve, find over- and under-costed objects."
sources:
  - https://gamebalanceconcepts.wordpress.com/
  - https://www.routledge.com/Game-Balance/Schreiber-Romero/p/book/9781498799577
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cost curve balancing

**Goal:** every object that costs resources gives benefits in proportion to its cost, so
no option is strictly better per cost and new content can be priced consistently.

Ian Schreiber's *Game Balance Concepts* course (and the Schreiber and Romero *Game
Balance* book) describes building a **cost curve**: a function mapping cost to the
expected benefit, derived from existing objects, for **transitive** mechanics (where
better things simply cost more).

## Procedure
1. **Pick a common currency** (e.g. mana, gold, or abstract "points").
2. **List all costs** of each object (resource cost, opportunity cost, drawbacks) and
   **all benefits** (stats, abilities).
3. **Assign values** to each attribute: start with the simplest objects (vanilla stats
   only) to solve for per-stat values (e.g. 1 attack = 1 point, 1 health = 0.5 points).
4. **Decide the curve shape:** linear (benefit = k x cost) or with increasing returns at
   high cost (higher-cost cards give more per cost, compensating for being harder to
   play). Many card games use increasing returns.
5. **Spreadsheet:** one row per object; columns for each attribute value; total benefit;
   expected benefit from the curve; **delta** = benefit - expected.
6. **Flag outliers:** large positive delta = over-powered (under-costed); large negative =
   under-powered.
7. **Price special abilities** by comparing objects that differ only by that ability.
8. Validate in play; numbers start the conversation, playtests finish it.

## Example spreadsheet columns
`name | cost | attack | health | ability_value | total_benefit | curve(cost) | delta`
with `curve(cost) = a*cost + b` fitted (e.g. LINEST/trendline) from vanilla objects.

## Gotchas
- Context-dependent abilities (strong in some decks) can't be valued by one number;
  give ranges and test in context.
- Synergies break per-object balance; check combinations separately.
- Intransitive relationships (counters) need a different method: payoff-matrix analysis
  (see `creative-arts.game-design.systems-and-mechanics.payoff-matrices-and-yomi`).

## Verify
- [ ] Common currency and per-attribute values documented.
- [ ] Cost curve fitted from simple objects.
- [ ] Every object's delta computed; outliers reviewed.
- [ ] Playtests confirm or correct the flagged outliers.
