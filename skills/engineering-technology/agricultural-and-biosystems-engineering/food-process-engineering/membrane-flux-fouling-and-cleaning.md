---
id: engineering-technology.agricultural-and-biosystems-engineering.food-process-engineering.membrane-flux-fouling-and-cleaning
name: membrane-flux-fouling-and-cleaning
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: food-process-engineering
tags: [agricultural-and-biosystems-engineering, food-process-engineering, membrane-flux, membrane-fouling, concentration-polarisation, transmembrane-pressure, crossflow-filtration, membrane-cleaning, membrane-filtration]
level: advanced
status: draft
description: "Understand membrane flux in food filtration: pressure-driven flux, concentration polarisation and gel layer, fouling types, operating limits and cleaning."
sources:
  - "Singh & Heldman, Introduction to Food Engineering"
  - "Toledo, Fundamentals of Food Process Engineering"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Membrane flux, fouling and cleaning

**Goal:** a membrane process that holds a stable flux through the run and recovers it after cleaning.

## Flux
- Permeate flux J = (TMP - osmotic pressure difference) / (mu x total resistance), where TMP is the transmembrane pressure. For pure water flux is proportional to pressure. For feeds, as TMP rises flux levels off to a plateau limited by concentration polarisation (a solute-rich layer at the membrane) or a gel layer.
- Higher crossflow velocity thins the layer and raises the limiting flux; higher temperature lowers viscosity and raises flux (within the membrane's temperature limits).
- Flux also falls as the retentate concentrates (more viscous, higher osmotic pressure).

## Fouling
- Reversible polarisation (removed by flushing), adsorption of protein, pore blocking, and cake or biofilm formation; scaling of minerals such as calcium phosphate in dairy.
- Operate below the critical flux, run at moderate TMP, pretreat feed (clarify, pH or calcium adjustment, microfiltration to remove fat or microbes).

## Cleaning
- Clean on a cycle based on flux decline or TMP rise: water rinse, then alkaline (with chlorine for proteins where the membrane permits), acid for minerals, and sanitising step; follow the membrane maker's limits on pH, temperature and chlorine exposure.
- Verify cleanliness with the clean water flux measured at standard temperature and TMP compared with the new membrane value; a significant loss means fouling remains or the membrane is damaged.

## Verify
- [ ] Normalised water flux logged before and after each clean.
- [ ] Rejection and permeate quality checked after cleaning.
- Unconfirmed: allowed chlorine and pH for your membrane; read the datasheet.
