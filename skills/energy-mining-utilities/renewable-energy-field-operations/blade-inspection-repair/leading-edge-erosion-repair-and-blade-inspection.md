---
id: energy-mining-utilities.renewable-energy-field-operations.blade-inspection-repair.leading-edge-erosion-repair-and-blade-inspection
name: leading-edge-erosion-repair-and-blade-inspection
category: energy-mining-utilities
field: renewable-energy-field-operations
product: blade-inspection-repair
tags: [renewable-energy-field-operations, blade-inspection-repair, wind-turbine-blade, blade-repair, leading-edge-erosion, lep, leading-edge-protection, erosion-shield, filler, gelcoat, polyurethane-coating, composite-repair, glass-fibre, laminate, epoxy, scarf-repair, rope-access, irata, blade-platform, drone-inspection, damage-category, lightning-protection-system, lps, receptor, down-conductor, continuity-test, cure-temperature, humidity, dew-point]
level: advanced
status: draft
description: "Inspect a wind turbine blade and repair leading-edge erosion and small laminate damage: categorise damage, prepare, fill, coat or shell, cure in the weather window, check LPS."
sources:
  - "DNV-ST-0376 (Rotor blades for wind turbines) and DNV-RP-0171 (testing of LEP) concepts, paraphrased"
  - "Coating and LEP system manufacturers' application guidance, general practice paraphrased"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Leading-edge erosion repair and blade inspection

**Goal:** find blade damage early, repair erosion before it reaches the laminate, and make
a repair that survives rain at tip speeds near 300 km/h.

## 1. Inspection
- **Drone inspection** of all three blades, both sides and edges, is now standard for
  screening; rope-access or platform close-up for anything flagged.
- Turbine stopped, blade pitched/positioned per procedure, rotor locked, LOTO in place.
- Record per finding: blade serial, side (pressure/suction, LE/TE), radius from root (m),
  size, photo with scale, and **damage category** using the owner's or OEM's scale
  (commonly 1–5: cosmetic → structural/stop turbine).
- Look for: leading-edge erosion (pitting → coating loss → laminate exposed), trailing-edge
  splits, cracks (especially near max chord and root), lightning damage (burn marks,
  missing receptors, delamination), and drainage hole blockage near the tip.

## 2. Is it yours to repair?
Coating and filler repairs on erosion are standard field work. Laminate (structural)
damage, spar cap or shear web involvement, root or bond-line cracks → engineering
disposition first. Anything category 4–5 usually means stop the turbine and escalate.

## 3. Weather window — the real constraint
Check against the product data sheets: surface and air temperature (often ≥ 10–15 °C),
relative humidity (often ≤ 70–80%), and surface ≥ 3 °C **above dew point**. Wind within
rope/platform limits. Plan cure time before rain or low temperature. Heated tents/blankets
extend the season but need temperature logging.

## 4. Erosion repair steps (typical)
1. Clean (remove dirt, insect residue, oil) with the specified solvent.
2. Grind/sand back damaged coating and loose material to sound substrate, feathering edges
   — don't sand into the glass fibres more than necessary.
3. If laminate is exposed or damaged within the allowed limits: laminate repair with
   matching fibre and resin, scarf ratio as specified (commonly 1:50 for structural),
   cured per resin schedule.
4. Apply filler/putty to restore the aerodynamic profile; sand to a smooth contour — use a
   profile gauge, a bump or step on the LE erodes faster than the original damage.
5. Apply the LEP system (flexible coating or tape/shell) at the specified film thickness,
   number of coats and recoat window. Check wet/dry film thickness.
6. Document with before/after photos, batch numbers, temperatures and humidity.

## 5. Lightning protection checks
Receptors present and intact; resistance/continuity measured from receptor to root
down-conductor with a low-resistance ohmmeter (values per OEM; commonly well below an ohm
or a few tens of milliohms). Burn marks around receptors = investigate internal damage.

## Gotchas
- Applying over a damp or cold substrate is the #1 cause of early coating failure.
- Mixing ratios for two-pack products are by weight or volume exactly as specified — small
  errors leave soft coatings.
- Dropped tools from rope access kill; tether everything.

## Verify
- [ ] Each finding categorised with location, size and photo.
- [ ] Structural damage referred for engineering disposition.
- [ ] Weather and dew-point conditions logged at application and through cure.
- [ ] Profile smooth to gauge; LEP thickness measured.
- [ ] LPS continuity measured and within OEM limit.

*Uncertain:* damage scales, scarf ratios and environmental limits are owner/OEM/product
specific — use their documents.
