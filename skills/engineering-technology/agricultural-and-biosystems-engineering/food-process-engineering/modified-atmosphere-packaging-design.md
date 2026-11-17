---
id: engineering-technology.agricultural-and-biosystems-engineering.food-process-engineering.modified-atmosphere-packaging-design
name: modified-atmosphere-packaging-design
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: food-process-engineering
tags: [agricultural-and-biosystems-engineering, food-process-engineering, modified-atmosphere-packaging, map, gas-flushing, produce-respiration, headspace-gas, oxygen-scavenger, co2-absorption]
level: advanced
status: verified
description: "Design modified atmosphere packaging: gas mixtures by food type, produce respiration versus film permeability, headspace ratio, scavengers, safety and checks."
sources:
  - "Toledo, Fundamentals of Food Process Engineering"
  - "US FDA food safety regulations (https://www.fda.gov)"
  - "Codex Alimentarius, General Principles of Food Hygiene and HACCP (https://www.codexalimentarius.org)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Modified atmosphere packaging design

**Goal:** an in-pack atmosphere that slows the main spoilage mechanism for the food, without creating a safety hazard.

## Food type and gases
- Fresh meat: high oxygen (to keep bright red myoglobin) with carbon dioxide to slow aerobic spoilage; or very low oxygen with carbon monoxide in the few markets that allow it (regulation varies).
- Cooked meat, cheese, bakery, pasta: low oxygen, nitrogen and carbon dioxide to prevent mould and oxidation; carbon dioxide is bacteriostatic and dissolves into the product, so allow for pack collapse (use a larger headspace or nitrogen buffer).
- Fresh produce: the pack is a passive system. Product respiration consumes oxygen and produces carbon dioxide; the film permeability sets the steady atmosphere. Model: dO2/dt = -(respiration rate x product mass) + (O2 permeation through film); choose film area and permeability so that the steady-state oxygen and CO2 fall within the tolerance range for the produce (below the fermentation threshold). Respiration rate rises with temperature, so the pack must work at the actual distribution temperature.
- Gas to product volume ratio often 2:1 to 3:1 for gas-flushed packs of meats and cheese, as practised (gated: unconfirmed, source is paywalled or blocked); confirm for your product.

## Components
Gas mixer and flusher, headspace oxygen analyser (use a headspace gas analyser for the check), seals, barrier film, and where needed oxygen scavenger sachets or CO2 emitters. Scavenger sachets are food-contact items; follow the regulations and mark them as not edible.

## Safety
Low oxygen packs of fish, cooked and chilled foods may allow growth of non-proteolytic Clostridium botulinum at refrigeration; the packs need adequate control (acidification, salt, time-temperature limits, barrier plus shelf life limit). Determine the controls with a qualified food safety professional or a process authority, and follow the local food regulations.

## Verify
- [ ] Residual oxygen and CO2 measured at pack and at end of shelf life.
- [ ] Pack leak test (`seal-integrity-and-leak-testing`).
- Unconfirmed: gas ratios and regulatory permissions; confirm per product and market.
