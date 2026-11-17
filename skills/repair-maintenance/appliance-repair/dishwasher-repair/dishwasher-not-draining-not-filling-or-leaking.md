---
id: repair-maintenance.appliance-repair.dishwasher-repair.dishwasher-not-draining-not-filling-or-leaking
name: dishwasher-not-draining-not-filling-or-leaking
category: repair-maintenance
field: appliance-repair
product: dishwasher-repair
tags: [appliance-repair, dishwasher-repair, dishwasher, drain-pump, wash-pump, circulation-pump, filter, sump, air-gap, high-loop, garbage-disposal-knockout, inlet-valve, water-inlet-valve, float-switch, anti-flood, aquastop, e15, e24, spray-arms, heating-element, door-gasket, leak, bosch, whirlpool, miele]
level: practitioner
status: draft
description: "Fix the big three dishwasher faults: won't drain (filter, high loop/air gap, drain pump), won't fill (supply, inlet valve, float/anti-flood), and leaks (door seal, sump, spray arm, overfill)."
sources: ["Manufacturer service manuals / error code lists (e.g. Bosch E15/E24 meanings)", "Author's synthesis; brand specifics vary"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Dishwasher: not draining, not filling, or leaking

**Goal:** resolve the majority of dishwasher calls with a fixed order of checks, cheapest
first. Unplug (or isolate at the breaker) and turn off the water before opening panels;
keep towels handy — there is always water in the sump.

## 1. Won't drain (standing water after the cycle; drain error code)
1. **Filter/sump:** twist out the filter assembly at the bottom of the tub; clean the
   fine mesh and coarse filter under the tap with a soft brush. Look into the sump for
   glass, olive pits, labels — they jam the drain pump impeller.
2. **Drain pump:** with the filter out, bail the sump, then reach in (gloves; glass) to
   the pump cover (often a small snap-in cover in the sump) and turn the impeller by
   hand — it should spin freely with a slight magnetic cogging. Remove obstructions.
3. **Drain path:**
   - A **new garbage disposal** with its knockout plug still in place — classic install
     error; the dishwasher inlet on the disposal must be knocked out.
   - Hose kinked behind the unit; clogged **air gap** (countertop cap) — remove the cap and
     clean.
   - The hose must have a **high loop** (secured up under the counter) or an air gap to
     stop sink water siphoning back.
4. **Electrical test:** in service/diagnostic mode, run the drain; no hum → measure pump
   coil (often tens of ohms to ~200 Ω) and voltage at the pump. Hum, no flow → impeller.
5. Error codes: e.g. Bosch **E24/E25** point to drain blockage or pump; many Whirlpool
   models show drain faults via blinking light patterns. Look up by model.

## 2. Won't fill (or fills slowly)
1. Supply valve under the sink open fully; hose not kinked; inlet filter screen at the
   valve (where the supply hose connects) not clogged with debris (common after mains work).
2. **Float switch:** a plastic float in the front corner of the tub; if stuck up (food,
   foam), the machine thinks it's full. Lift and drop it — it should move freely and click.
3. **Anti-flood/AquaStop:** many machines sit in a base tray with a float switch; water in
   the tray (from a leak) triggers the anti-flood (e.g. Bosch **E15**) and the machine
   refuses to fill, pumping out instead. Tip the machine back ~45° carefully to drain the
   tray, dry it, then find the leak that caused it.
4. **Inlet valve:** measure coil resistance (often ~500 Ω–1.5 kΩ; check tech sheet) and
   voltage during fill. Coil good and voltage present but no flow → valve mechanism failed.

## 3. Leaking
Find where first: put dry paper towels under the machine and run a cycle with the kick
plate off.
- **Front/door bottom:** door gasket worn or dirty; wrong detergent (hand-wash liquid
  makes foam that pours out); machine not level so water runs to the door. Level it
  (bubble level on the door frame and tub rim).
- **Under the tub:** sump seals, pump seals, the hose clamps on drain/circulation hoses,
  heating-element nuts.
- **Inlet connection:** cracked inlet valve body or loose supply fitting (use a new
  fibre/rubber washer; don't overtighten plastic threads).
- **Spray arms:** cracked arm or missing end caps spraying at the door seal.
- **Overfill:** float stuck down or inlet valve not closing (water keeps coming with power off
  = valve leaking through → replace).

## 4. Poor cleaning (often reported as "broken")
Clean spray arms (pick out holes with a toothpick), clean the filter, check the wash pump
runs, hot water at the sink first (run the kitchen tap until hot), rinse aid and correct
detergent dose; hard water → use salt in the softener if fitted.

## Gotchas
- Never run the drain pump dry for long in testing — seals overheat.
- Heating element "won't dry" complaints: many modern machines use condensation drying
  with no element; check the manual before diagnosing.
- Uncertain: resistance values and error-code meanings vary between brands and model years.

## Verify
- [ ] Filter, sump and drain pump impeller clear; drain path (knockout, air gap, high loop) correct.
- [ ] Float moves freely; anti-flood tray dry and the original leak found.
- [ ] Inlet valve tested by resistance and voltage; fills to the correct level.
- [ ] Leak source identified with a paper-towel run; machine level.
- [ ] Full cycle completes with no error code and no water under the machine.
