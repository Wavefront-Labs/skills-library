---
id: engineering-technology.agricultural-and-biosystems-engineering.controlled-environment-systems.anaerobic-digester-and-biogas-basics
name: anaerobic-digester-and-biogas-basics
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: controlled-environment-systems
tags: [agricultural-and-biosystems-engineering, controlled-environment-systems, biogas-digester, anaerobic-digestion, biogas, methane-yield, hydraulic-retention-time, digestate, h2s-safety, manure-management]
level: advanced
status: draft
description: "Understand anaerobic digestion of manure and wastes: process stages, mesophilic and thermophilic operation, retention time, biogas yield and quality, and safety hazards."
sources:
  - "Michigan State University Extension E3080, anaerobic digestion (https://sanweb.lib.msu.edu/DMC/extension_publications/e3080/E3080.pdf)"
  - "University of Wisconsin Extension, Katers, anaerobic digestion (https://extension.soils.wisc.edu/wp-content/uploads/sites/68/2016/07/Katers.pdf)"
  - "EPA AgSTAR, anaerobic system design and technology (https://www.epa.gov/agstar)"
  - "USDA NRCS Conservation Practice Standard 366 Anaerobic Digester (https://www.nrcs.usda.gov)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Anaerobic digester biogas basics

**Goal:** judge whether and how a digester could process farm waste, with the figures to size it roughly and the hazards that must be controlled by qualified designers.

## Process
Hydrolysis, acidogenesis, acetogenesis and methanogenesis convert organic matter into biogas (mostly methane and carbon dioxide, with traces of hydrogen sulphide and water vapour) and a digestate that retains the nutrients.
- Temperature: mesophilic (about 35-40 C; Michigan State Extension gives 95-105 F) is the common choice for farm digesters; thermophilic (about 50-60 C; Michigan State Extension gives 135-145 F) gives faster digestion and higher pathogen kill but is more sensitive and uses more heat.
- Hydraulic retention time (HRT): the volume divided by the daily feed; for manure digesters, Wisconsin Extension gives about 15-30 days for plug-flow units, and NRCS standards set minimums by digester type (the design depends on the feedstock and digester type: covered lagoon, complete-mix, plug flow).
- Organic loading rate (kg VS per m3 per day) must be limited to avoid souring (volatile fatty acid build-up); monitor pH, alkalinity and VFA.

## Yield and energy
- Gas yield depends on the feedstock volatile solids and its biodegradability; dairy manure gives modest yields, food waste and crop residues far more. Use tested figures (laboratory biochemical methane potential tests) for the feedstock; do not rely on generic tables for a business case.
- Biogas contains roughly 50-70 percent methane by volume; methane's lower heating value is 802.3 kJ/mol / 22.414 L/mol = 35.8 MJ per normal cubic metre (computed). Use gas for boiler heat, combined heat and power, or upgrade to biomethane.
- Parasitic load: heating, mixing and pumping can take a significant share of the output.

## Treatment and safety
- Remove hydrogen sulphide (biological desulphurisation by air dosing, or chemical scrubbing) before engines, because it corrodes them.
- Hazards: methane is flammable (flammable in air at about 5-15 percent by volume, widely published, e.g. NOAA CAMEO and NIOSH Pocket Guide; the NIOSH entry itself was not opened), hydrogen sulphide is toxic (lethal at higher concentrations, rapid loss of smell warning), and low oxygen in tanks. Classified areas, flame arrestors, flare, gas detection, confined space rules, and emergency plan are required. Digester design and operation need a qualified engineer and compliance with local gas, pressure and environmental regulations.

## Digestate
Digestate is a fertiliser (ammonium-rich) with its own odour, nitrogen volatilisation and nutrient management considerations (`manure-nutrient-balance-for-land-application`).

## Verify
- [ ] Feedstock tests and a mass balance support the business case.
- [ ] Gas composition and safety systems tested before commissioning.
- Unconfirmed: local rules; engage a specialist.
