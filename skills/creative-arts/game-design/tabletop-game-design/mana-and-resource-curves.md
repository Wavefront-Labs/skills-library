---
id: creative-arts.game-design.tabletop-game-design.mana-and-resource-curves
name: mana-and-resource-curves
category: creative-arts
field: game-design
product: tabletop-game-design
tags: [game-design, tabletop-game-design, mana-curve, resource-curve, card-games, deck-construction, cost-distribution]
level: practitioner
status: draft
description: "Design mana and resource curves for card games: cost distribution across the pool, resource count per deck, flood and screw mitigation and curve as a pacing tool."
sources:
  - https://magic.wizards.com/en/news/making-magic
  - https://magic.wizards.com/en/rules
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mana and resource curves

**Goal:** players can usually spend their resources each turn, games escalate on
schedule, and resource draw rarely decides the game alone.

## Resource models
| Model | Example | Flood / screw |
|---|---|---|
| Resource cards in deck | Magic lands | real risk; mitigated by mulligan, deck ratio |
| Automatic growth | Hearthstone +1 mana per turn | none; curve fixed by turn |
| Any card as resource | Ascension / Star Realms coins, Race for the Galaxy discards | flexible |
| Separate resource deck | Flesh and Blood pitch, Lorcana inkable cards | middle ground |

## Curve of the card pool
1. Decide the intended game length in turns and the key turns (when the first threat
   lands, when bombs appear).
2. Histogram cards by cost in the pool; typical limited Magic sets have the most cards at
   2-3 mana, tapering to few at 6+.
3. Make sure each faction or archetype has plays at every early cost; a hole at 2 means
   those decks skip turns.
4. Put strong late-game cards at costs that arrive after the game's mid-point.

## Resource count per deck (resource-in-deck model)
- Magic's common guidance: about 17 lands in a 40-card limited deck and 24 in 60-card
  constructed; Frank Karsten's hypergeometric analysis gives exact land counts per curve.
- Use hypergeometric odds: P(at least k resources in the first n cards). Target
  roughly 85-90% to hit the curve's key land drop on time.
- Mitigations: mulligan rules, card draw/selection, cards with dual modes (land or spell).

## Procedure
1. Build the cost histogram per faction in the set sheet.
2. Build 5 sample decks and calculate on-curve probabilities for each.
3. Playtest and log turns where a player could not spend resources or had no plays.
4. Adjust costs or resource counts until those turns are rare.

## Gotchas
- Undercosted top-end makes everyone ramp; overcosted top-end makes aggro the only strategy.
- Automatic mana growth removes screw but makes turn sequences predictable; add cost reducers or flexible cards.
- A high-variance resource system can be a feature in casual games; decide on purpose.

## Verify
- [ ] Cost histogram per faction shows plays at every early cost.
- [ ] Sample decks hit key drops at the target probability.
- [ ] Logged "nothing to do" turns are rare in tests.
