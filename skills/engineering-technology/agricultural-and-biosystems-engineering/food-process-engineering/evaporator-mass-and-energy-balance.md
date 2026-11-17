---
id: engineering-technology.agricultural-and-biosystems-engineering.food-process-engineering.evaporator-mass-and-energy-balance
name: evaporator-mass-and-energy-balance
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: food-process-engineering
tags: [agricultural-and-biosystems-engineering, food-process-engineering, evaporator-balance, evaporation, solids-balance, steam-economy, vapour-load, single-effect-evaporator]
level: advanced
status: draft
description: "Do the mass and energy balance of a single-effect evaporator: solids balance, vapour and steam rates, heat transfer area, boiling point effects and economy."
sources:
  - "Singh & Heldman, Introduction to Food Engineering"
  - "Toledo, Fundamentals of Food Process Engineering"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Evaporator mass and energy balance

**Goal:** the steam use, vapour rate and area for concentrating a liquid food from feed to target solids.

## Balances
- Total: F = L + V (feed, concentrate, vapour).
- Solids: F x xF = L x xL, so V = F x (1 - xF/xL).
- Energy: F x hF + S x lambda_s = L x hL + V x H_v (plus losses), where S is steam, lambda_s its latent heat, h are enthalpies. For dilute solutions, use water properties for the vapour at the boiling pressure and add the boiling point elevation to the vapour superheat (`boiling-point-elevation-and-duhring-plot`).
- Steam economy = V / S; for single effect about 0.8-0.95 in good conditions; multi-effect or recompression improves it (`multiple-effect-evaporator-steam-economy`).

## Area
Q = U x A x (T_steam - T_boiling), with U set by viscosity, which falls strongly as solids increase; U is typically much lower in the last stage of a viscous product. Use measured U from similar products and the evaporator type (falling film, rising film, forced circulation).

## Practical
- Feed temperature matters: preheated feed above boiling flashes and lowers steam need.
- Condensate returned to the boiler; condenser load and vacuum capacity sized from V.
- Heat-sensitive foods (milk, juices) use low temperatures under vacuum and short residence times.

## Verify
- [ ] Mass balance closes; compare calculated and measured concentrate solids.
- [ ] Steam use per kg water evaporated tracked.
- Unconfirmed: numerical economy and U for your product.
