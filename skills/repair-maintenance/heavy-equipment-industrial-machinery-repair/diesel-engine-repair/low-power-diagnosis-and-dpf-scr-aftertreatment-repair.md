---
id: repair-maintenance.heavy-equipment-industrial-machinery-repair.diesel-engine-repair.low-power-diagnosis-and-dpf-scr-aftertreatment-repair
name: low-power-diagnosis-and-dpf-scr-aftertreatment-repair
category: repair-maintenance
field: heavy-equipment-industrial-machinery-repair
product: diesel-engine-repair
tags: [diesel-engine-repair, heavy-duty-diesel, low-power, black-smoke, white-smoke, derate, fuel-restriction, lift-pump, common-rail, rail-pressure, injector-return-flow, boost-leak, turbocharger, turbo-shaft-play, charge-air-cooler, dpf, diesel-particulate-filter, forced-regeneration, parked-regen, doc, scr, def, adblue, urea-doser, nox-sensor, egr, tier-4-final, stage-v, blow-by]
level: advanced
status: draft
description: "Diagnose low power and smoke on heavy diesels (fuel supply, rail pressure, boost leaks, turbo) and repair DPF/SCR faults: regens, DEF quality, doser and NOx sensors."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Heavy diesel low power and aftertreatment faults

**Goal:** find why a heavy-duty diesel is down on power, smoking or derated, in the
order that finds cheap causes first, and fix DPF/SCR faults without just deleting codes.

## 1. Define the complaint
- Is it a **derate** (ECM deliberately limiting torque — there will be an active code
  and often a dash lamp) or a **true loss** of power with no codes? A derate is solved by
  fixing what triggered it; a true loss is mechanical, fuel or air.
- Read codes and hour stamps first with the OEM tool (see
  `repair-maintenance.heavy-equipment-industrial-machinery-repair.oem-diagnostic-software.fault-code-triage-cutout-tests-and-ecm-flashing`).
- Note smoke colour: black = too much fuel for the air (boost leak, restricted intake,
  over-fuelling injector); white = unburnt fuel or coolant (low compression, timing,
  head gasket); blue = oil (turbo seals, rings, valve guides).

## 2. Fuel supply — the most common cause
1. Check the obvious: fuel level, water separator bowl, the right fuel grade for the
   season (waxing in cold weather).
2. Measure **supply restriction** with a vacuum gauge before the transfer pump under
   load. Rising restriction means a plugged primary filter, collapsed hose or a pickup
   problem. (Draft note: allowable restriction is engine-specific, often quoted in
   inHg or kPa — use the OEM spec.)
3. Check **low-pressure supply** after the secondary filter, and for air: a clear line
   or sight glass showing bubbles means a suction-side leak.
4. On common-rail engines, log **rail pressure desired vs actual**. Actual that cannot
   follow desired under load = supply, high-pressure pump or injector leak-back.
5. **Injector return (leak-off) flow test**: compare cylinders into graduated
   containers over a fixed time; a high-return injector bleeds rail pressure.
6. Cylinder cutout test to find a dead cylinder, then confirm with compression.

Safety: common-rail systems hold 1,600–2,500 bar. Never crack a high-pressure line
with the engine running, wait the OEM bleed-down time after shutdown, and never feel
for leaks with your hand — use cardboard. Fuel injection into skin is a surgical
emergency.

## 3. Air — intake, boost and exhaust
- Intake restriction indicator and air filter; a collapsed inner hose hides behind a
  clean filter.
- **Boost leak test**: cap the charge-air system and pressurise to about 20–30 psi
  (1.4–2 bar) with regulated shop air, spray soapy water on CAC joints, clamps and the
  cooler core. Leaking cores show as bubbles or oil wetness.
- Turbo: with engine off and cool, check shaft play — axial should be small and the
  wheel must not touch the housing when pushed radially. Oil in the intake, chipped
  blades or rub marks mean replace. Find why it failed (oil supply, debris, ingested
  dust) before fitting a new one, and prime it with oil before first start.
- High exhaust backpressure (plugged DPF, crushed pipe) also robs power.

## 4. DPF faults
- Read soot and ash load, differential pressure and regen history in the OEM tool.
- High soot with failed regens: first fix the cause (an injector or EGR fault making
  soot, short idle-heavy duty cycles). Then run a **parked/forced regeneration** in a
  clear area away from fuel, dry grass and buildings; exhaust and the outlet exceed
  500 °C.
- High **ash** load cannot be burnt off; the filter must be removed for cleaning
  (thermal + air pulse) or exchanged. Record the ash reset in the tool afterwards.
- Cracked or melted DPF faces usually follow an uncontrolled regen with excessive soot.

## 5. SCR / DEF faults
- Test DEF quality with a refractometer: target 32.5% urea (roughly 31.8–33.2%).
  Diluted, contaminated (fuel, coolant) or crystallised DEF is a common cause.
- Inspect the doser for white urea crystal build-up and the lines for heater faults in
  cold weather. Run the doser quantity test into a graduated cylinder.
- NOx sensors: compare upstream vs downstream readings; one sensor stuck or slow is a
  frequent replacement. Let new sensors complete their learn/self-test drive cycle.

## Gotchas
- Fitting a new turbo to cure black smoke when the real cause is a split CAC hose.
- Never use diesel fuel conditioner or tap water in the DEF tank; drain and flush.
- Emissions system tampering is illegal on certified machines in most jurisdictions.
- (Draft note: fuel pressures, regen temperatures and DEF test limits vary by engine
  family and model year; confirm in the OEM service manual.)

## Verify
- [ ] Power and rail pressure follow desired values on a loaded test, no derate code.
- [ ] No boost leak at test pressure; turbo play within OEM limits.
- [ ] DPF differential pressure and soot load normal after a completed regen.
- [ ] DEF concentration in range; NOx conversion efficiency code does not return.
- [ ] Root cause recorded, not just the replaced part.
