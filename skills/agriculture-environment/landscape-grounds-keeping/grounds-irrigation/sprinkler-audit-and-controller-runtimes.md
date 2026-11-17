---
id: agriculture-environment.landscape-grounds-keeping.grounds-irrigation.sprinkler-audit-and-controller-runtimes
name: sprinkler-audit-and-controller-runtimes
category: agriculture-environment
field: landscape-grounds-keeping
product: grounds-irrigation
tags: [grounds-irrigation, landscape-irrigation, lawn-sprinkler, sprinkler-system, irrigation-audit, catch-cup-test, distribution-uniformity, dulq, precipitation-rate, run-time, irrigation-controller, smart-controller, et-controller, cycle-and-soak, rotor, spray-head, mp-rotator, head-to-head-coverage, matched-precipitation, pressure-regulation, leak-detection, winterisation, blowout, rain-sensor]
level: practitioner
status: draft
description: "Audit a turf sprinkler zone with catch cups, compute DU and precipitation rate, then set controller run times with cycle-soak; includes blowout winterisation."
sources: ["Irrigation Association, Landscape Irrigation Auditor manual (summary)", "University extension landscape irrigation audit guides (e.g. Texas A&M, UF/IFAS)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Sprinkler audit and controller run times

**Goal:** find out how much water each zone really puts down and how evenly, fix the
obvious faults, and set run times from those numbers instead of "15 minutes each".

## 1. Walk-through first (fix before you measure)
Run each zone and look for: broken or tilted heads, heads sunk below turf, nozzles
blocked or mismatched (a spray nozzle in a rotor zone), arcs watering paths/walls,
misting (pressure too high), weak throw (too low), geysers and wet spots (leaks),
heads blocked by plants. Fix these, then audit.

## 2. Catch-cup test
1. Lay **catch cups** (identical straight-sided cups or proper audit cans) in a grid:
   for spray zones ~2–3 m apart, rotor zones ~3–5 m apart; include cups near heads and
   midway between. Aim for ≥ 16–24 cups per zone.
2. Run the zone for a set time (sprays ~10–15 min; rotors ~20–30 min) in calm conditions.
3. Measure each cup's depth (or volume ÷ opening area).
4. Note the static and running pressure at a head (pitot tube + gauge) if you can.

## 3. The two numbers
- **Precipitation rate (PR, mm/h)** = average catch (mm) ÷ run time (h).
  Typical: spray heads 35–50 mm/h; rotors and rotary nozzles 8–20 mm/h.
- **Low-quarter distribution uniformity (DU_lq)** = average of lowest 25% of cups ÷ overall
  average. Rough guide: rotors ≥ 0.70 good, sprays ≥ 0.65 good; < 0.55 poor.

## 4. Turning numbers into run times
1. Get the weekly water need: `ETo × crop coefficient`. Cool-season turf ~0.8, warm-season
   ~0.6 (common landscape coefficients). E.g. summer ETo 6 mm/day × 0.8 × 7 = 34 mm/week.
2. Correct for poor uniformity: a common audit method uses a **scheduling multiplier**
   `SM ≈ 1 / (0.4 + 0.6 × DU_lq)`. DU 0.6 → SM 1.30. Weekly gross = 34 × 1.30 = 44 mm.
3. Split into days (e.g. 3 days a week → ~15 mm per watering, deep and infrequent
   encourages deeper roots).
4. **Run time (min) = depth per watering ÷ PR × 60.** 15 mm on a rotor zone at 12 mm/h
   → 75 min; on a spray zone at 40 mm/h → 22 min.
5. **Cycle-and-soak:** if the soil can't take it (clay infiltrates perhaps 5–10 mm/h,
   slopes less), split the run into cycles short enough not to run off, with ~30–60
   minutes between. Most controllers have a cycle/soak setting per zone.
6. Water early morning (e.g. finishing by ~8 am): less wind and evaporation, leaf dries
   during the day (less disease).
Re-adjust monthly (or let an ET-based "smart" controller do it — but still enter the
right PR, soil type, slope and plant type per zone, because it computes from them).

## 5. Leak finding
- Water meter reading with all zones off: if it moves, there's a leak on the mainline
  (or a stuck valve).
- A zone that won't shut off: debris under the valve diaphragm, damaged solenoid, or
  the flow control screwed down too far. Use the bleed screw to test.
- Wet soft spots and unusually green strips between heads point at lateral leaks.

## 6. Winterisation (freezing climates)
1. Shut off the irrigation supply and backflow isolation valves; set controller to off/rain mode.
2. **Compressed-air blowout:** connect at the blowout point after the backflow preventer;
   run one zone at a time at a **moderate pressure (commonly ~3.5–5.5 bar / 50–80 psi;
   lower for PVC/poly — check the system's rating)** until only mist comes out. Never
   blow through the backflow device or leave all valves closed with air running —
   compressed air heats fittings and can burst pipe. Use eye protection.
3. Drain backflow preventer test cocks as the maker directs; insulate exposed parts.

## Gotchas
- Mixing rotors and sprays in a zone guarantees over- or under-watering.
- The multiplier formula is one widely used variant; other audit programs use slightly
  different ones. **Values are typical, not checked for your site.**

## Verify
- [ ] Every zone audited after repairs: PR and DU_lq recorded.
- [ ] Run times calculated from ET, PR, DU — written into a zone table.
- [ ] No runoff during a run (cycle-soak set where needed).
- [ ] Meter is still with all zones off.
- [ ] Winterisation done before first hard freeze.
