---
id: repair-maintenance.aircraft-maintenance.landing-gear-hydraulics.oleo-strut-servicing-and-brake-overhaul
name: oleo-strut-servicing-and-brake-overhaul
category: repair-maintenance
field: aircraft-maintenance
product: landing-gear-hydraulics
tags: [aircraft-maintenance, landing-gear-hydraulics, landing-gear, oleo-strut, strut-servicing, nitrogen, mil-prf-5606, hydraulic-fluid, strut-extension, cleveland-brakes, brake-linings, brake-relining, brake-bleeding, wheel-bearings, tire-inspection, gear-retraction-check, jacking, hydraulic-leak, o-rings, rivet-linings, burn-in]
level: practitioner
status: draft
description: "Service an air-oil oleo strut (fluid level and nitrogen extension), reline and bleed light-aircraft disc brakes, and inspect wheel bearings - with jacking, safety and leak-isolation steps."
sources: ["FAA-H-8083-31 Airframe Handbook, ch. 13 Aircraft Landing Gear Systems", "Parker/Cleveland Wheels & Brakes Component Maintenance Manual AWBCMM0001 (method structure)", "FAA AC 43.13-1B ch. 9"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Oleo strut servicing and brake overhaul

**Goal:** restore correct strut extension and damping, and brakes that hold run-up power
without fade or drag. Exact strut extension charts, nitrogen pressures, fluid spec and
torque values come from the aircraft maintenance manual (AMM) and the brake CMM.

## 1. Oleo strut servicing (air-oil type)
**Why:** a strut that is "flat" (bottomed) transmits landing loads straight into the
structure; one that is over-extended bounces and can affect gear-door rigging.

1. Check extension first with the aircraft at normal weight on level ground; compare
   exposed piston length to the AMM chart (often vs. aircraft weight or with a
   temperature correction).
2. If low, decide: **gas only low** (common slow leak through the valve core) or **fluid low**
   (wet piston, fluid on the tyre, bottoming hard). Fluid low → full service.
3. **Full service:**
   - Jack the aircraft at the jack points per the AMM (wing and tail stand as required;
     lock jacks; no one under the aircraft).
   - Remove the valve cap; *slowly* release nitrogen through the valve core (depress with
     a tool, face away — never unscrew the valve body under pressure).
   - With pressure at zero, remove the valve, fully compress the strut and fill with the
     specified fluid (commonly MIL-PRF-5606 red; some types MIL-PRF-87257 or Skydrol in
     transport aircraft — never mix) to the filler port level.
   - Cycle (extend/compress) a few times with a hose into a fluid container to purge air,
     top up again fully compressed.
   - Reinstall the valve with a new O-ring, torque per AMM.
   - Lower the aircraft and inflate with **dry nitrogen** (not shop air — moisture and
     oxygen) until extension matches the chart.
4. Wipe clean, cycle by rocking the aircraft, recheck extension after 24 h. A strut that
   keeps dropping needs seals.

## 2. Disc brake relining (e.g. Cleveland-type)
1. Chock the opposite wheel, jack or lift the wheel just clear.
2. Remove back-plate bolts, slide the caliper off the torque plate. Measure lining
   thickness (minimum is often 0.100 in for Cleveland organic linings — check CMM) and
   the disc for thickness, warping and grooves.
3. Remove old rivets with the riveting tool punch; install new linings with the
   specified tubular/semi-tubular rivets and the clinching tool — rivet heads must be
   flush and not cracked.
4. Inspect pistons and O-rings: no corrosion, scoring or weeping. Replace O-rings with
   the correct compound for the fluid.
5. Reinstall, torque back-plate bolts per CMM and safety-wire if required.
6. **Conditioning (burn-in):** organic linings typically need several firm taxi stops
   from ~30–35 kt; metallic linings use a different procedure. Follow the manufacturer's
   sequence and let them cool between runs — skipping it gives poor holding at run-up.

## 3. Bleeding brakes
- Pressure-bleed from the bottom up: pressure pot connected to the caliper bleeder,
  catch-can at the master cylinder/reservoir. Push fluid until no bubbles appear at the top.
- Firm pedal with no sponginess; check no fluid leaks under pressure.

## 4. Wheel bearings and tyres
- Deflate before disassembling a split wheel (never unbolt an inflated split wheel —
  it can explode).
- Clean bearings with solvent, inspect for spalling/brinelling/heat colour; repack with
  the specified grease. Torque axle nut: often seat-then-back-off to a free-but-no-play
  position, then safety.
- Tyres: inflate to AMM pressure, cold; check cuts, flat spots, cord visible = replace.

## Gotchas
- Nitrogen bottles at 2,000+ psi: use a regulator, never connect a bottle directly.
- Over-servicing with fluid leaves no gas spring → harsh landings and seal blowout.
- Mixing hydraulic fluid types ruins seals; check the reservoir placard.
- Uncertain: lining minimums, torques and burn-in speeds are typical published values
  for one brake family; confirm in the CMM for your part number.

## Verify
- [ ] Strut extension within the AMM chart at known weight; no leaks after 24 h.
- [ ] Fluid type matches placard; nitrogen used, valve O-ring replaced and torqued.
- [ ] Linings riveted flush, disc within limits, back-plate bolts torqued/safetied.
- [ ] Brakes bled firm, conditioned, and hold run-up power; wheel turns freely when released.
- [ ] Bearings repacked; tyres at pressure; gear retraction check done if gear was disturbed.
