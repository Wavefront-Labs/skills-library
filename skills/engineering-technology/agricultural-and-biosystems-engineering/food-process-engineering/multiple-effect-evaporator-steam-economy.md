---
id: engineering-technology.agricultural-and-biosystems-engineering.food-process-engineering.multiple-effect-evaporator-steam-economy
name: multiple-effect-evaporator-steam-economy
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: food-process-engineering
tags: [agricultural-and-biosystems-engineering, food-process-engineering, multiple-effect-evaporator, steam-economy, feed-arrangement, forward-feed, backward-feed, evaporator-effects]
level: advanced
status: draft
description: "Design a multiple-effect evaporator: effects, feed arrangement, pressure and temperature profile, steam economy, area per effect and when to stop adding effects."
sources:
  - "Singh & Heldman, Introduction to Food Engineering"
  - "Toledo, Fundamentals of Food Process Engineering"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Multiple-effect evaporator steam economy

**Goal:** the number of effects that gives the lowest total cost of steam, capital and cooling water for the evaporation load.

## Idea
Vapour from effect 1 heats effect 2 (which boils at a lower pressure and temperature), and so on. Ideal steam economy is about the number of effects N; actual values are lower (losses, boiling point elevation, feed heating), commonly in the range of 0.8 x N or lower.

## Feed arrangements
- Forward feed: feed and steam in the same direction; simple, no pumps between effects, but the most concentrated, viscous liquor is in the coldest effect (low U).
- Backward feed: feed enters the coldest effect; concentrated liquor boils in the hottest effect (good for viscous products) but needs pumps between effects and heats the liquor to high temperatures (poor for heat-sensitive foods).
- Mixed or parallel: used for specialised cases, for example crystallising solutions.

## Design calculation
1. Overall temperature drop from steam to the last-effect boiling temperature (set by the condenser vacuum) minus the sum of boiling point elevations gives the useful driving force.
2. Distribute the driving force over the effects (equal area is a common starting point).
3. Iterate mass and energy balances per effect to find vapour flows, and recompute areas until equal.
4. Compare economy and cost for N = 2 to maybe 6 or 7; stop when the added effect's saved steam does not pay for it.

## Heat sensitive foods
Dairy and juice evaporators often use falling-film with thermal vapour recompression (TVR) or mechanical recompression to reach high economy at low temperatures; mind residence time and flavour (aroma recovery).

## Verify
- [ ] Heat balance error below a couple of percent.
- [ ] Measured economy and area versus design after commissioning.
- Unconfirmed: cost optima depend on local energy price.
