---
id: engineering-technology.chemical-engineering.process-design.cooling-water-system-design
name: cooling-water-system-design
category: engineering-technology
field: chemical-engineering
product: process-design
tags: [chemical-engineering, process-design, pd-utilities-and-offsites, cooling-water-system-design, cooling-water, cooling-tower, cycles-of-concentration]
level: practitioner
status: gated
description: "Design a recirculating cooling water system: cooling tower duty, range and approach, make-up and blowdown from cycles of concentration."
sources:
  - "Towler and Sinnott, Chemical Engineering Design; Turton et al., Analysis, Synthesis and Design of Chemical Processes; Peters, Timmerhaus and West, Plant Design and Economics (textbooks, method only)"
  - "Latent heat and blowdown algebra computed (IAPWS-97 via the iapws Python package): B = E/(C - 1), M = E + B + drift"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cooling water system design

**Goal:** Design a recirculating cooling water system: cooling tower duty, range and approach, make-up and blowdown from cycles of concentration.

## Steps
1. Total duty Q from all coolers; water flow = Q / (cp x range), where range is supply-to-return temperature difference.
2. Choose cooling tower approach to the design wet-bulb temperature (a few degrees C above wet bulb is typical for sizing (gated: unconfirmed, source is paywalled or blocked); confirm with the vendor).
3. Evaporation loss is roughly 0.00085 x circulating flow x range in degrees F as a rule of thumb (gated: unconfirmed, source is paywalled or blocked) (0.00153 per degree C, so about 1 percent of flow per 6.5 C of range). The latent-heat limit if all heat left by evaporation is about 1 percent per 5.6 C (cp 4.18 kJ/kg K, latent heat 2430 kJ/kg at 30 C), so the rule must give less than that; confirm with a heat balance.
4. Blowdown B = E / (C - 1) neglecting drift, where C is the cycles of concentration; make-up M = E + B + drift.
5. Set the return temperature limit by fouling and scaling risk and the exchanger design; add chemical treatment and a pump station.

## Gotchas
- Wet-bulb design basis should be a high percentile of site data.
- Water quality limits the cycles of concentration.

## Verify
- [ ] Make-up equals evaporation plus blowdown plus drift.
- [ ] Return temperature suits exchanger design.
