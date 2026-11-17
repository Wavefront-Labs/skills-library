---
id: repair-maintenance.automotive-repair.brake-systems.pad-rotor-replacement-and-brake-bleeding
name: pad-rotor-replacement-and-brake-bleeding
category: repair-maintenance
field: automotive-repair
product: brake-systems
tags: [automotive-repair, brake-systems, brake-pads, brake-rotors, brake-discs, calipers, caliper-slides, minimum-thickness, runout, dial-indicator, lateral-runout, bedding-in, brake-fluid, dot-4, dot-3, dot-5-1, moisture-test, brake-bleeding, pressure-bleeder, abs, abs-bleed, electronic-parking-brake, epb-service-mode, hub-cleaning, brake-judder]
level: practitioner
status: draft
description: "Replace brake pads and rotors to spec (thickness, runout, hub cleaning, slide lubrication, torque), service electronic parking brakes, bleed or flush fluid including ABS, and bed in the pads."
sources: ["Manufacturer brake service procedures (structure only)", "FMVSS 116 / SAE J1703 brake fluid specifications (DOT 3/4/5.1)", "Bosch/TRW/ATE brake service guidance (general practice)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Pad and rotor replacement and brake bleeding

**Goal:** brakes that stop straight, quietly and without judder, with fluid that won't
boil. Brakes are safety-critical: torque everything to spec, never reuse one-time
fasteners, and road test before handing back.

## 1. Inspect and measure
- Pad thickness (replace well before the wear indicator — commonly at ~ 2–3 mm friction).
  Compare inner vs outer pad: uneven wear points to seized slides or a sticking piston.
- **Rotor thickness** with a micrometer at several points; the **minimum thickness** is
  cast/stamped on the rotor ("MIN TH 22 mm"). Below min → replace.
- Thickness variation (parallelism) causes pedal pulsation; lateral runout causes it
  over time by uneven pad contact.
- Look for cracks, heavy scoring, blue heat spots, corrosion lips.

## 2. Pads and rotors (floating caliper, typical)
1. Loosen wheel nuts on the ground; lift and support on stands. Remove wheel.
2. **EPB (electronic parking brake) rear calipers:** put the system in **service/maintenance
   mode** with a scan tool (or the vehicle's own menu/procedure) before pushing pistons
   back — forcing them damages the motor/actuator.
3. Remove caliper guide bolts, hang the caliper from a wire (never by the hose). Remove
   carrier if replacing rotors (carrier bolts are often thread-locked/one-time-use).
4. Remove rotor (retaining screw; penetrating oil; tap the hat area with a soft mallet).
5. **Clean the hub face** to bare metal with a hub-cleaning disc or wire brush — rust
   scale under a new rotor is the most common cause of runout and later judder.
6. Clean new rotor's anti-rust coating if the maker says to (brake cleaner); fit and
   secure.
7. Check runout with a **dial indicator** ~10 mm from the rotor edge, with wheel nuts
   holding it (use washers/lug nuts at spec): typical limit ~ 0.05 mm (0.002 in) — check spec.
8. Clean caliper slide pins, inspect boots; lubricate with **high-temperature silicone or
   specified brake grease** (not petroleum grease on rubber boots). Clean the abutment clips
   or fit the new ones from the kit.
9. Push back the piston (open the bleeder to push old fluid out instead of back up to the
   ABS unit, where allowed — clamp hose and catch fluid). Watch the reservoir doesn't overflow.
10. Fit pads with shims, a thin smear of anti-squeal paste on the backing plate only (never
    the friction surface).
11. Refit caliper, torque guide bolts and carrier bolts to spec; wheel nuts by torque wrench
    in a star pattern (not an impact gun at full power).
12. **Pump the pedal** until firm before moving the car — first press goes to the floor.

## 3. Brake fluid
- Fluid is hygroscopic; water lowers its boiling point. Replace by **time** (commonly every
  2 years) or by a boiling-point/moisture test (> ~3 % water is a common replace threshold).
  Copper-strip tests check corrosion inhibitor depletion.
- Use the type on the reservoir cap: DOT 3, DOT 4 and DOT 5.1 (glycol) are mutually
  compatible but not equivalent; **DOT 5 (silicone)** is not compatible — never mix.
- Brake fluid strips paint; rinse spills with water immediately.

## 4. Bleeding / flushing
- **Pressure bleeder** at the reservoir (e.g. ~ 1 bar / 15 psi — check reservoir rating) is
  most reliable; two-person pedal method or vacuum bleeder as alternatives.
- Order: furthest from the master cylinder first is traditional (RR, LR, RF, LF on many LHD
  cars), but **many ABS/ESC systems specify their own order** — check the manual.
- Bleed until fluid is clear and bubble-free; close bleeders at the specified torque (small,
  easy to snap).
- **ABS modulator:** if air got into it (reservoir ran dry, unit replaced), run the
  scan-tool **ABS automated bleed** routine that cycles the valves/pump.

## 5. Bed-in (burnish) new pads
Typical: 8–10 moderate stops from ~ 60 to 10 km/h without fully stopping, then several
firmer ones from ~ 80 km/h, then drive without braking to cool. Avoid sitting with the
brake held on hot rotors (pad imprint). Follow the pad manufacturer's procedure.

## Gotchas
- Squeal from missing shims or dry abutments; judder from hub rust or lug-nut over-torque.
- Mixing pad compounds side to side causes pulling; replace in axle sets.
- Uncertain: thresholds (runout, moisture) are typical; manufacturer specs govern.

## Verify
- [ ] Rotor thickness ≥ minimum; runout within spec on a clean hub.
- [ ] Slides cleaned and correctly lubricated; pads/shims seated; bolts torqued to spec.
- [ ] EPB returned from service mode and calibrated; no warning lights.
- [ ] Fluid correct type, clear, bubble-free; ABS bleed run if needed.
- [ ] Pedal firm; pads bedded; road test stops straight with no pulsation.
