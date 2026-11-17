---
id: repair-maintenance.aircraft-maintenance.composite-repair.wet-layup-scarf-repair-with-vacuum-bag
name: wet-layup-scarf-repair-with-vacuum-bag
category: repair-maintenance
field: aircraft-maintenance
product: composite-repair
tags: [aircraft-maintenance, composite-repair, carbon-fibre, fiberglass, cfrp, gfrp, scarf-repair, stepped-repair, wet-layup, prepreg, vacuum-bagging, hot-bonder, cure-cycle, epoxy, tap-test, delamination, honeycomb, sandwich-panel, peel-ply, breather, srm, ac-43-13, ndi]
level: practitioner
status: draft
description: "Repair a damaged laminate or sandwich panel with a tapered scarf, wet layup and vacuum-bag cure: damage mapping, scarf ratio, ply table, bagging stack, hot-bonder cure and post-repair NDI."
sources: ["FAA AC 43.13-1B ch. 3 (fiberglass and plastics)", "FAA-H-8083-31 Airframe Handbook, ch. 7 Advanced Composite Materials"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Wet-layup scarf repair with vacuum bag

**Goal:** restore strength and stiffness of a damaged composite part with a bonded
repair whose plies match the original orientation, cured to full properties and proven
by NDI. Ply count, resin system, scarf ratio and cure must come from the aircraft SRM or
the component maintenance manual — this skill is the method, not the data.

## 1. Map the damage
1. **Visual + tap test** with a coin or tap hammer in a grid; a dull "thud" means
   delamination or disbond. Mark the boundary with a grease pencil.
2. Confirm with ultrasonic (pulse-echo or bond tester) if available — tap testing misses
   deep or small delams and is unreliable on thick laminates.
3. Record: size, depth (how many plies), core damage, fluid ingress. Wet honeycomb core
   must be dried or replaced; trapped moisture blows the repair during the hot cure.
4. Classify against SRM limits: cosmetic (fill/seal), bolted/bonded patch, scarf
   repair, or replace.

## 2. Prepare the scarf
- Remove damage to sound material with a router or die grinder; round shape, no sharp corners.
- **Scarf ratio** typically 30:1 to 50:1 for carbon (length:thickness), ~12:1 to 20:1
  for some fiberglass — SRM governs. A 2 mm laminate at 50:1 means a 100 mm taper each side.
- Sand the taper with a 2–3 in pad (e.g. 80 → 120 grit aluminium oxide) so each ply
  shows as a visible ring; that ring count is your ply map.
- Note ply orientation of each ring (0/45/90/−45) from the SRM ply table or by the
  weave direction visible in the ring.
- Clean with a lint-free wipe and approved solvent (e.g. MEK/IPA per the manual),
  wipe one direction, let flash off. Do not touch the surface after this.
- Dry the part: often 1–2 h at moderate heat under vacuum before bonding.

## 3. Cut and lay plies
- Cut repair plies on a clean table from fabric matched to the original (style, weight,
  orientation). Largest-first or smallest-first layup is SRM-specific; add 1–2 extra
  "oversize" plies extending ~25 mm beyond the scarf as a cover if specified.
- Mix resin by **weight** to the manufacturer's ratio on a scale (± 1–2 %); note the pot
  life and mix batch number. Typical target fibre:resin ~ 50:50 by weight for wet layup.
- Impregnate plies between release film with a squeegee, then lay each in place, matching
  orientation to ±5°, rolling out air.

## 4. Vacuum bag stack (from the part outward)
1. Repair plies
2. Peel ply
3. Perforated release film
4. Breather/bleeder (polyester felt), extending to the vacuum port
5. Vacuum bag film sealed with tacky tape (pleat at corners)
6. Vacuum port on breather, *off* the repair; separate gauge port
Add thermocouples at the thinnest and thickest point of the repair, under the bag but not
touching the plies directly (use a scrap of release film).

**Leak check:** pull full vacuum (target ≥ 22 inHg / ~ 75 kPa), isolate the pump, and
watch the gauge — commonly accepted loss is < 2–5 inHg in 5 minutes. Fix leaks before heat.

## 5. Cure
- Hot bonder (heat blanket controller) set to the SRM cycle, e.g. ramp 1–3 °C/min, dwell
  at the specified temperature (a typical room-temp-mix epoxy: ~ 65–93 °C for 1–2 h),
  cool down ≤ 3 °C/min under vacuum. Control from the coldest thermocouple, alarm on the hottest.
- Keep the blanket at least 25 mm beyond the repair; heat sinks (spars, ribs) need
  extra insulation or the cure there will lag.
- Save the hot-bonder printout with the work order — it *is* the cure record.

## 6. Finish and inspect
- Remove the bag; peel ply leaves a bondable surface. Sand edges flush without cutting
  into the outer ply fibres.
- Tap test and ultrasonic the whole repair and a margin around it: no voids, no disbond.
- Restore lightning-strike protection (copper/aluminium mesh) and conductive primer if the
  original had it, then paint to the original finish system.

## Gotchas
- Cold, humid shop: amine blush and weak bonds. Work within the resin datasheet's
  temperature/humidity window.
- Overheating a blanket over a thin skin scorches resin and the surrounding paint.
- Never use a wet-layup in place of prepreg where the SRM specifies prepreg — strength
  allowables differ.
- Uncertain: scarf ratios and cure temperatures above are typical ranges, not universal.

## Verify
- [ ] Damage boundary confirmed by NDI, not only tap test.
- [ ] Scarf ratio and ply count/orientation match the SRM ply table.
- [ ] Resin mixed by weight; batch and pot life recorded.
- [ ] Vacuum leak check passed; cure printout attached showing every thermocouple in band.
- [ ] Post-cure NDI clean; LSP and finish restored; record references approved data.
