---
id: creative-arts.game-design.systems-and-mechanics.core-loop-and-economy-design
name: core-loop-and-economy-design
category: creative-arts
field: game-design
product: systems-and-mechanics
tags: [game-design, systems-design, mechanics, core-loop, gameplay-loop, compulsion-loop, game-economy, sources-and-sinks, faucets-and-drains, resource-economy, progression, xp-curve, inflation, balance, spreadsheet, machinations, loop-diagram, meta-loop, reward-schedule, f2p, video-games, board-games]
level: practitioner
status: draft
description: "Design a game's core loop and resource economy: map loops at three timescales, list every source and sink, model flow in a spreadsheet, and catch inflation before players do."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Core loop and economy design — rules that keep players acting

**Goal:** a written, testable model of what the player does every few seconds, every
few minutes and every session, and of how every resource enters and leaves the game,
so balance problems show up in a spreadsheet instead of in reviews.

## 1. Write the loops at three timescales
State each loop as *action → feedback → reward → new choice*:
- **Moment loop (seconds):** e.g. aim → shoot → hit feedback → ammo drops.
- **Core loop (minutes):** e.g. explore → fight → loot → upgrade → explore harder area.
- **Meta loop (sessions):** e.g. unlock character → new build options → harder mode.
Test: if a loop has no **new choice** at the end, it is a treadmill, not a loop. If
the moment loop is not satisfying with placeholder art, no meta loop will save it —
prototype the moment loop first.

## 2. Inventory sources and sinks
Make a table with one row per resource (gold, XP, wood, health, cards, time):
| Resource | Sources (faucets) | Sinks (drains) | Cap? | Convertible to |
Rules of thumb:
- Every resource needs **at least one sink that scales** with player wealth (repair
  costs, upgrade tiers, consumables). Fixed-price sinks become trivial late game.
- Every conversion between resources is an exchange rate you now have to balance.
  Fewer currencies = fewer rates. Add one only when it carries a distinct decision.
- Caps (inventory limits, max hand size) are sinks in disguise — they force spending.

## 3. Model the flow before building it
In a spreadsheet, one row per minute or per turn of expected play:
- Columns: income per source, spend per sink, net, balance, and *cost of the next
  meaningful purchase*.
- Plot **balance ÷ next-purchase cost**. Near 1 means a steady drip of decisions; well
  above 1 means inflation (nothing to buy); well below 1 means a grind wall.
- For progression curves, compare linear, polynomial (`base × level^1.5–2` is a
  common XP shape) and exponential costs; exponential costs against linear income
  produce walls fast. These exponents are conventions, not laws — tune to your pacing.
- Tools: plain spreadsheets are enough; Machinations (a node-based economy simulator)
  helps for feedback loops with randomness.

## 4. Feedback loops — know which you built
- **Positive feedback** (winning makes you stronger) ends games and snowballs.
  Useful for closing out a match; dangerous across a whole campaign.
- **Negative feedback** (leaders get slowed, rubber-banding, catch-up mechanics)
  keeps contests close but can make skill feel pointless if visible.
Name each loop in your diagram as + or −, and decide deliberately where the game
should snowball.

## Gotchas
- **Dominant strategy:** if one option is best in every case, the others are not
  choices. Check every purchase/action against "would anyone ever pick the alternative?"
- **Designers overestimate play time.** Real players skip content and optimise; model
  a min-maxer row alongside a casual row.
- **Fixed rewards inflate.** A 100-gold quest reward is huge at hour 1 and noise at
  hour 20; scale rewards or retire them.
- **Monetised economies** (free-to-play) add ethical and legal exposure (loot box
  rules differ by country). This skill does not cover monetisation design — treat it
  separately and check current regulation.
- Numbers here are starting heuristics from common practice, not verified constants;
  confirm by playtest (see creative-arts.game-design.playtesting-and-balance.running-structured-playtests).

## Verify
- [ ] Moment, core and meta loops are written down, each ending in a new choice.
- [ ] Every resource has a source, a sink that scales, and a stated reason to exist.
- [ ] A spreadsheet shows balance ÷ next-cost over a full expected playthrough.
- [ ] Each feedback loop is labelled + or −, with snowballing placed on purpose.
- [ ] No option is dominant in your option-vs-option check.
