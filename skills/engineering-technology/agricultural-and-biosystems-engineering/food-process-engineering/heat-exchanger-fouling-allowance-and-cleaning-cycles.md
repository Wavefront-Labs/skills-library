---
id: engineering-technology.agricultural-and-biosystems-engineering.food-process-engineering.heat-exchanger-fouling-allowance-and-cleaning-cycles
name: heat-exchanger-fouling-allowance-and-cleaning-cycles
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: food-process-engineering
tags: [agricultural-and-biosystems-engineering, food-process-engineering, heat-exchanger-fouling, fouling-resistance, cleaning-cycle, milk-fouling, fouling-allowance, run-length, food-heat-transfer]
level: advanced
status: draft
description: "Estimate fouling in food heat exchangers: fouling resistance, protein and mineral deposits, run length, area allowance and CIP interval from pressure drop and U trends."
sources:
  - "Toledo, Fundamentals of Food Process Engineering"
  - "Singh & Heldman, Introduction to Food Engineering"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Fouling allowance and cleaning cycles

**Goal:** a heat exchanger design and cleaning schedule that holds the process temperatures between cleans.

## What fouls
- Milk and dairy: protein (especially whey protein denaturation when the wall is much hotter than the product, from roughly 70 C upward) deposits as a type A layer; minerals (calcium phosphate) deposit at higher temperatures as a harder layer.
- Juices and starch: pectin, starch and sugar caramelisation; fibres.
- Oils and fats: polymerisation.

## Quantifying
Fouling resistance Rf = 1/U_fouled - 1/U_clean. Track it online from U (computed from measured temperatures and flows) and pressure drop. An increasing pressure drop and a falling outlet temperature at constant steam or hot water are the usual signs.

## Design
- Add heat transfer area or a fouling allowance, based on the tested or measured Rf for your product and operation time. Over-sizing too much leads to a higher wall temperature gradient and can worsen fouling, so do not just oversize: reduce wall-product temperature difference, use staged heating and avoid dead zones.
- Run length: choose the clean interval from the economics of lost production and cleaning chemical use, and from hygiene or regulatory limits (some processes must be cleaned within a time).

## Cleaning
Use a validated CIP program (`clean-in-place-circuit-design-and-verification`); chemistry for protein is alkaline then acid for minerals; verify cleanliness with visual inspection after opening, ATP or protein swabs.

## Verify
- [ ] Rf trend logged and a limit set for cleaning.
- [ ] Post-clean U returns to near the clean value.
- Unconfirmed: temperatures where fouling transitions; confirm in a pilot.
