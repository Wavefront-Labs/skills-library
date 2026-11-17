---
id: creative-arts.game-design.systems-and-mechanics.premium-pricing-and-dlc-design
name: premium-pricing-and-dlc-design
category: creative-arts
field: game-design
product: systems-and-mechanics
tags: [game-design, systems-and-mechanics, dlc-design, expansion-design, premium-pricing, monetisation, season-pass]
level: practitioner
status: docs-checked
description: "Price a premium game and plan DLC and expansions: comparable pricing, discount cadence, what belongs in DLC vs base game, season passes and save compatibility."
sources:
  - https://partner.steamgames.com/doc/marketing/discounts
  - https://partner.steamgames.com/doc/store/application/dlc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Premium pricing and DLC / expansion design

**Goal:** a base game that feels complete at its price, and paid additions players see as extra value.

## Pricing the base game
1. Benchmark 5-10 comparable titles (genre, length, production values) at launch price.
2. Price on perceived value, not hours.
3. Plan the discount calendar early. Steamworks documents these rules: a 30-day cooldown
   after release, after a price increase and between custom discounts (Steam seasonal sales
   are exempt from the discount cooldown but not from the release or price-increase one);
   discounts run 1-14 days and 10-95%; an optional launch discount runs 7-14 days, up to 40%.
   Steam advises easing into discounting and increasing depth over time, since early deep
   discounts undermine the value for full-price buyers. Recheck the current page.

## What goes in DLC
| Type | Good fit | Bad fit |
|---|---|---|
| Expansion | new region, story or systems that extend the endgame | content cut from the main story |
| Cosmetic | skins, soundtrack, art book | power in competitive modes |
| Convenience | rarely; reads as pay-to-skip | XP boosts in a premium game |
| Episode / mode | standalone chapters, new character | patching an unfinished ending |

Anything the base story needs stays in the base game. Announce DLC as post-launch work
to avoid "cut content" backlash.

## Season pass and bundles
- List the contents, or at least the count and timing; vague passes generate refunds.

## Technical design
- On Steam each DLC has its own app ID. Content can ship to all owners and the game checks
  ownership with `ISteamApps::BIsDlcInstalled`, so ownership gates content, not shared code.
  Saves must load with and without DLC (graceful handling when DLC is missing on another
  device).

## Checked

2026-11-09. Confirmed against the Steamworks Discounts and DLC pages: 30-day cooldowns,
seasonal-sale exemption, discount and launch-discount limits, advice to ease into discounting,
per-DLC app ID and `BIsDlcInstalled` ownership check. Removed the regional-table claim, the
season-pass saving range, the review-behaviour claim and the map-pack claim (not on the pages
read); dropped the Schell book link (a store page, not read for these claims). The DLC-type
table is judgement.
Method: documentation only; no commands were run.

## Verify
- [ ] Comparable-title price table.
- [ ] DLC plan with each item's type and justification.
- [ ] Save compatibility tested with DLC added and removed.
- [ ] Discount calendar checked against platform rules.
