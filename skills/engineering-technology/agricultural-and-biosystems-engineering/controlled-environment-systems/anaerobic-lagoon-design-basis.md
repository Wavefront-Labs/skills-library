---
id: engineering-technology.agricultural-and-biosystems-engineering.controlled-environment-systems.anaerobic-lagoon-design-basis
name: anaerobic-lagoon-design-basis
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: controlled-environment-systems
tags: [agricultural-and-biosystems-engineering, controlled-environment-systems, anaerobic-lagoon, waste-treatment-lagoon, volatile-solids-loading, lagoon-liner, sludge-accumulation, nrcs-359, manure-management]
level: advanced
status: verified
description: "Understand the design basis of an anaerobic treatment lagoon: volatile solids loading, treatment and sludge volumes, minimum depth, liner, startup and risks."
sources:
  - "USDA NRCS Conservation Practice Standard 359 Waste Treatment Lagoon, 2017 (https://www.nrcs.usda.gov/sites/default/files/2022-10/Waste_Treatment_Lagoon_359_CPS_Oct_2017.pdf)"
  - "ASABE Standards, Engineering Practices and Data (https://www.asabe.org)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Anaerobic lagoon design basis

**Goal:** a lagoon that treats the manure biologically with acceptable odour, without leaking and with room for sludge.

## Concept
An anaerobic lagoon is a deep pond where bacteria break down the volatile solids (VS) of manure. It combines treatment volume, sludge storage and temporary storage (storage for effluent between irrigation or land spreading events). It works best in warm climates; in cold climates the rate falls and long storage is needed.

## Design basis
- Treatment volume is set by a volatile solids loading rate (mass of VS per unit volume per day) chosen for the climate; allowed loadings depend on the temperature zone and the regulatory standard (US NRCS Conservation Practice Standard for waste treatment lagoons, the older MWPS Livestock Waste Facilities Handbook values and similar). Use the current standard for your location. Too high loading gives odour and poor treatment.
- Add: sludge accumulation volume for the clean-out period, temporary storage volume (manure storage calculation as `manure-storage-sizing`), net rainfall and a design storm, and freeboard.
- Depth: NRCS Standard 359 sizes anaerobic lagoons by a minimum treatment volume from volatile-solids loading, not a fixed depth; deeper lagoons have less surface per volume and keep the anaerobic zone. Any minimum depth comes from the state version of the standard (no fixed national figure could be confirmed; the 8 ft operating depth seen in NRCS reflects the digester standard 366, not lagoons). The standard also requires a marker for the minimum operating level and sludge-survey provisions that vary by state.
- Inflow arrangement: deliver below the surface to avoid crust disturbance; avoid dumping solids at one corner.

## Liner and siting
Seepage control is critical: compacted clay, synthetic liner or natural soil that meets permeability limits; groundwater and bedrock separation distances; setbacks from neighbours and water; leak monitoring in sensitive areas. Fencing and warning signs because of drowning and gas hazards.

## Startup and operation
Fill with water to half or more of the design volume before loading to dilute and prevent shock; start loading in warm season when possible; avoid disinfectants and large quantities of antibiotics or cleaning chemicals; manage the sludge level by measurement.

## Alternatives
Covered lagoons and digesters capture biogas (`anaerobic-digester-and-biogas-basics`); solids separation reduces the loading.

## Verify
- [ ] Standard and its edition quoted in the design record.
- [ ] Sludge depth survey at set intervals.
- Numeric loading rates are taken from the current state standard (not listed here).
