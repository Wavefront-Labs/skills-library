---
id: creative-arts.design-for-form-and-experience.experiential-design.setting-illuminance-targets-and-colour-quality
name: setting-illuminance-targets-and-colour-quality
category: creative-arts
field: design-for-form-and-experience
product: experiential-design
tags: [illuminance, lighting-design, color-temperature, cri, lux-levels, foot-candles, lighting-calculation, cct]
level: practitioner
status: draft
description: "Set lighting targets: illuminance in lux or footcandles by task, colour temperature, CRI and R9, uniformity, glare, and a lumen-method check for the layout."
sources:
  - "IES Lighting Handbook, 10th ed. (Illuminating Engineering Society, 2011) and IES RP-30 Museum and Art Gallery Lighting"
  - "CIE 157:2004 Control of Damage to Museum Objects by Optical Radiation"
  - "IES TM-30-20 Method for Evaluating Light Source Color Rendition"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Illuminance targets and colour quality

## Illuminance (maintained, on the task plane)
- 1 footcandle (fc) = 10.76 lux. Typical: corridors 50-100 lux (5-10 fc); offices 300-500 lux; retail general 300-750 lux with feature displays at 3-5x ambient; restaurants 100-200 lux; exhibits: **light-sensitive** objects (textiles, watercolours, prints) about **50 lux**, **moderately sensitive** (oil and tempera paintings, wood) about **150-200 lux**, insensitive (metal, stone, glass) up to 300 lux and more.
- **Museum exposure:** limit cumulative lux-hours per year (for example 150,000 lux-hours per year for medium sensitivity per CIE 157) and filter UV (under 75 microwatts per lumen).
- **Ratios:** accent to ambient 3:1 for emphasis up to 10:1 for drama; avoid more than 10:1 for adaptation and safety; keep uniformity (min:avg) of 0.6-0.7 on task areas.

## Colour temperature (CCT)
2700 K warm (hospitality, residential), 3000 K warm-white (retail, galleries), 3500-4000 K neutral (offices, retail), 5000-6500 K cool (task, daylight simulation). Stay consistent across a space (within about 100-200 K, or within MacAdam step 3 for fixtures that are seen together). Tunable white for circadian designs.

## Colour rendering
- **CRI Ra 80+** for general; **90+ for museums, retail apparel, food, cosmetics**; check **R9 (saturated red) above 50** and R13 skin tones. IES TM-30 (Rf above 85 fidelity, Rg 100 plus or minus 5 gamut) gives richer evaluation.
- Use LED sources with spectral power data; compare mock-ups under final lighting.

## Quick lumen method
Number of fixtures = (target lux x area) / (lumens per fixture x CU x LLF). Typical CU 0.5-0.7, LLF 0.8-0.85. Verify with DIALux evo or AGi32 for photometric plots, then adjust.

## Controls and glare
Dimming (0-10 V, DALI, DMX) down to 1 percent; scenes; daylight harvesting; unified glare rating (UGR under 19 for offices); shield sources and avoid veiling reflections on glass and screens. Respect energy code lighting power density (ASHRAE 90.1 and local).

## Verify
- [ ] Targets chosen by task and object sensitivity with ratios.
- [ ] CCT, CRI and R9 specified; mock-up approved.
- [ ] Calculation or software plot supports quantity and layout.
