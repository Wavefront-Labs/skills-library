---
id: creative-arts.game-design.tabletop-game-design.tcg-set-design-and-rarity
name: tcg-set-design-and-rarity
category: creative-arts
field: game-design
product: tabletop-game-design
tags: [game-design, tabletop-game-design, card-game-design, set-design, card-rarity, tcg, lcg, booster-packs, as-fan, limited-format, mechanical-themes]
level: advanced
status: draft
description: "Design a trading/living card game set: set skeleton by colour and rarity, mechanical themes, as-fan maths for boosters, limited vs constructed balance and power creep control."
sources:
  - https://magic.wizards.com/en/news/making-magic
  - https://mitpress.mit.edu/9780262017138/characteristics-of-games/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# TCG set design and rarity

**Goal:** a card set with clear identity, healthy limited and constructed play, and
rarity that distributes complexity and power sensibly.

Mark Rosewater's long-running "Making Magic" column (Wizards of the Coast) documents
Magic: The Gathering's set design process, including the "set skeleton" and the
"New World Order" principle (keep complexity mostly out of common).

## Set skeleton
A spreadsheet of slots before any card is designed:
| Slot | Faction/colour | Rarity | Role (removal, creature at cost X, card draw, theme payoff) |
Fill slots with designs later. The skeleton guarantees each faction has the tools a
format needs.

## Rarity jobs
| Rarity | Typical job |
|---|---|
| Common | the bulk of limited play; simple, format-defining basics |
| Uncommon | theme signposts, moderate complexity |
| Rare | build-around and splashy effects |
| Mythic / top | showpieces; avoid making them mandatory for competitive play |
Keep the most complex cards at higher rarity so new players opening packs see simple cards.

## As-fan
**As-fan** = expected number of a given thing per booster pack. If a pack has 10
commons from a pool of 100 and 12 of those commons are a theme mechanic, the as-fan of
that mechanic at common is 10 x 12/100 = 1.2 per pack. Use as-fan to ensure themes show
up often enough in limited (draft/sealed).

## Procedure
1. Choose 2-4 mechanical themes and the set's world/flavour.
2. Build the skeleton; check per-faction cost curves with a cost histogram per faction.
3. Design cards into slots; compute as-fans for themes.
4. Playtest limited with simulated packs, constructed with top decks from previous sets.
5. Control power creep: compare new cards with older cards at the same cost.

## Gotchas
- LCG (fixed distribution, no randomised packs) removes rarity economics; balance for
  constructed only.
- Rare power in randomised products drives secondary-market prices; affects perception
  of fairness.
- Randomised paid packs may fall under loot-box rules in some places when digital.

## Verify
- [ ] Skeleton complete before designs.
- [ ] Complexity concentrated at higher rarities.
- [ ] Theme as-fans computed and adequate for limited.
- [ ] Limited and constructed playtests run.
