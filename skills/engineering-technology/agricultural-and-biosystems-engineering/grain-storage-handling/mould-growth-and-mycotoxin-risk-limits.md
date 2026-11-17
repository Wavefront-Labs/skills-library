---
id: engineering-technology.agricultural-and-biosystems-engineering.grain-storage-handling.mould-growth-and-mycotoxin-risk-limits
name: mould-growth-and-mycotoxin-risk-limits
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: grain-storage-handling
tags: [agricultural-and-biosystems-engineering, grain-storage-handling, mould-risk-mycotoxin, mycotoxin, aflatoxin, deoxynivalenol, fumonisin, ochratoxin, allowable-storage-time, safe-storage-moisture, stored-grain-pests]
level: advanced
status: verified
description: "Assess mould and mycotoxin risk in stored grain: moisture and temperature limits, allowable storage time, sampling for mycotoxins and regulator limits to confirm."
sources:
  - "Sinha & Muir, Grain Storage: Part of a System"
  - "Codex Alimentarius, General Principles of Food Hygiene and HACCP (https://www.codexalimentarius.org)"
  - "US FDA food safety regulations (https://www.fda.gov)"
  - "Purdue Extension AED-20 Managing Dry Grain in Storage (https://www.extension.purdue.edu/extmedia/aed/aed-20.html)"
  - "US FDA, CPG Sec. 555.400 Aflatoxins in Human Food (https://www.fda.gov/media/149666/download)"
  - "US FDA, CPG Sec. 683.100 Action Levels for Aflatoxins in Animal Food (https://www.fda.gov/media/121202/download)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Mould growth and mycotoxin risk limits

**Goal:** keep grain below the conditions that grow moulds and make toxins, and test and decide on lots correctly.

## Drivers
Storage moulds (Aspergillus and Penicillium) grow when the grain moisture is above the safe level for the temperature; field fungi (Fusarium, producers of deoxynivalenol and fumonisin) are mostly in the crop before harvest and are not much improved by storage if the grain is kept dry. Aflatoxin (Aspergillus flavus) is a drought and heat-stress problem in the field that can worsen in hot, damp storage; ochratoxin A arises in storage of cereals under damp conditions.

## Safe conditions
- Equilibrium relative humidity below about 65-70 percent restricts most storage mould growth; this corresponds to moisture contents (wet basis) in the order of 13-14 percent for wheat and about 14-15 percent for shelled corn, lower for oilseeds (gated: unconfirmed, source is paywalled or blocked). Purdue Extension lists corn at 14 percent for 6-12 months and 13 percent beyond a year, with 1 point lower for poor-quality grain. Use equilibrium moisture tables (`thin-layer-drying-equations-and-emc`) and the extension service guide for your crop and period.
- Allowable storage time tables (based on dry-matter loss experiments, for example published by university extension services) show the time at which grain loses quality at a given moisture and temperature; cooling is the main tool.
- Temperature cable monitoring and CO2 tracking identify hot spots (`temperature-cable-monitoring-and-interpretation`).

## Testing and limits
- Mycotoxin concentration is very unevenly distributed, so sampling dominates test error: take a large, representative composite sample, grind and subsample properly, and test with a validated method (lateral flow for screening; HPLC or LC-MS as confirmation).
- Regulatory limits depend on the jurisdiction and end use: for example the US FDA sets action and advisory levels (CPG 555.400: human food with more than 20 ppb total aflatoxins may be considered adulterated; animal feed levels in CPG 683.100 differ by animal class, with 20 ppb for feed for immature animals), and the EU sets maximum levels in Regulation (EU) 2023/915 (gated: unconfirmed, source is paywalled or blocked). Check the current level and the commodity-specific limit before shipping, and do not blend a contaminated lot to dilute it where the regulator forbids that.

## Verify
- [ ] Temperature and moisture log for each bin.
- [ ] Mycotoxin test results traceable to the lot and sampling plan.
- Unconfirmed: all regulatory limits; confirm with the regulator.
