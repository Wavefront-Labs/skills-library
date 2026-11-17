---
id: repair-maintenance.aircraft-maintenance.turbine-engine-maintenance.borescope-inspection-and-trend-monitoring
name: borescope-inspection-and-trend-monitoring
category: repair-maintenance
field: aircraft-maintenance
product: turbine-engine-maintenance
tags: [aircraft-maintenance, turbine-engine-maintenance, borescope, videoscope, hot-section-inspection, hsi, pt6, pt6a, cfm56, turbofan, turboprop, combustor, nozzle-guide-vane, compressor-blades, fod, engine-trend-monitoring, ecm, itt, egt-margin, ng, torque, compressor-wash, emm]
level: practitioner
status: draft
description: "Plan and run a turbine-engine borescope inspection (compressor, combustor, turbine) against EMM limits, and read engine trend data (ITT/EGT, Ng, fuel flow deltas) to catch deterioration early."
sources: ["Pratt & Whitney Canada PT6A Engine Maintenance Manual (borescope chapter) - structure only, no values reproduced", "FAA-H-8083-32 Powerplant Handbook, ch. 10 Engine Maintenance and Operation", "FAA AC 33.4-3 (continued airworthiness)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Borescope inspection and engine trend monitoring

**Goal:** find compressor, combustor and turbine damage before it becomes an in-flight
shutdown, using two complementary tools: periodic borescope inspection against the
Engine Maintenance Manual (EMM) limits, and continuous trend monitoring of flight data.
All accept/reject limits are engine-type specific and come from the EMM; this skill is
the procedure and judgement.

## 1. Borescope inspection
**Kit:** articulating videoscope (4–6 mm tip, 1.5–3 m), with measurement capability
(stereo or 3D phase measurement) if you'll measure defects; guide tubes; engine turning
tool or hand-cranking adapter; the EMM borescope port map.

1. **Safety:** engine cool (combustor sections can stay hot for hours), ignition and
   starter circuit-breakers pulled and tagged, "DO NOT START" placard in the cockpit.
2. Remove the specified port plugs (igniter holes on a PT6 give the combustor and CT
   vane view; dedicated borescope ports on turbofans for each HPC/HPT stage). Count and
   bag plugs — lost hardware in a gas path is FOD.
3. Set a **reference blade**: mark the blade at the port (with the scope's screenshot, or
   a permitted marking such as a strip of tape on a fan blade) so you can count a full
   revolution without missing or double-counting blades.
4. Turn the rotor slowly by hand/tool, one blade at a time, recording images of each
   leading edge, trailing edge, tip and platform.
5. Look for and classify:
   - **Compressor:** nicks, dents, tears, tip curl, erosion (blunted leading edges),
     dirt build-up (wash candidate).
   - **Combustor/liner:** cracks from cooling holes, burn-through, distortion,
     carbon build-up, fuel nozzle streaking (blocked/poor spray pattern).
   - **Turbine vanes/blades:** burning, coating loss (TBC spallation), cracks, missing
     material, tip rub, airfoil distortion.
6. Measure defects against the EMM (length, depth, distance from root/platform);
   each zone of the blade has different limits. When in doubt, image and send to the
   engine manufacturer's field support — they routinely disposition images.
7. Disposition: serviceable, serviceable with reduced re-inspection interval, blend
   on-wing (if approved, with borescope blending tools), or remove engine.
8. Reinstall port plugs with new seals/lockwire per the manual; leak-check on ground run.

## 2. Engine trend monitoring (ECTM)
Raw readings are meaningless alone; compare **deltas from a baseline model** at a
stabilised condition (same altitude band, OAT corrected, steady cruise ≥ 5 minutes).
1. Record (or download from the EMU/FADEC) per flight: ITT or EGT, Ng/N2, Np/N1, torque,
   fuel flow, oil pressure/temperature, vibration, plus altitude, IAS and OAT.
2. Upload to the manufacturer or third-party trend program; it plots deltas vs. baseline.
3. Read the patterns (rules of thumb, confirm with the program's fault matrix):
   - ITT/EGT up, fuel flow up, Ng up at same power → compressor fouling/erosion →
     compressor wash and re-trend.
   - ITT up with Ng down/flat, fuel flow up → hot-section deterioration → borescope.
   - Step change in any parameter → instrumentation or sudden damage: check sensors, then inspect.
   - Rising vibration trend → bearing, imbalance, FOD.
4. Track **EGT/ITT margin** (red-line minus take-off value): the main "remaining life" metric.

## Gotchas
- Instrument faults (thermocouple harness, Ng tach generator) mimic engine faults — rule
  them out before pulling an engine.
- A single noisy data point is not a trend; act on 3–5 consistent points or a clear step.
- Compressor washes improve margin temporarily; mark them on the trend plot.
- Uncertain: the trend patterns above are generic teaching rules; your engine's
  fault-isolation matrix may differ.

## Verify
- [ ] Every blade in the inspected stages imaged with a reference blade for count.
- [ ] Each finding measured and dispositioned against the EMM with chapter reference.
- [ ] Port plugs reinstalled, lockwired, leak-checked; no hardware unaccounted for.
- [ ] Trend data taken at stabilised conditions; deltas reviewed, washes/events annotated.
- [ ] Re-inspection interval adjusted and recorded where the EMM requires.
