---
id: repair-maintenance.aircraft-maintenance.piston-engine-maintenance.differential-compression-and-magneto-timing
name: differential-compression-and-magneto-timing
category: repair-maintenance
field: aircraft-maintenance
product: piston-engine-maintenance
tags: [aircraft-maintenance, piston-engine-maintenance, lycoming, continental, differential-compression-test, leak-down, master-orifice, magneto, magneto-timing, slick, bendix, tcm, timing-light, e-gap, top-dead-center, spark-plugs, annual-inspection, 100-hour, oil-analysis, borescope, cylinder, exhaust-valve, sb-03-3]
level: practitioner
status: draft
description: "Run a differential compression test with the calibrated master orifice and time magnetos to the engine on Lycoming/Continental piston engines during an annual or 100-hour inspection."
sources: ["Continental Service Bulletin SB03-3 (differential pressure test)", "Lycoming Service Instruction SI 1191A (cylinder compression)", "FAA-H-8083-32 Powerplant Handbook, ch. 1 and 4"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Differential compression test and magneto timing

**Goal:** judge cylinder health with a repeatable leak-down test, and set ignition timing
so each magneto fires at the degrees-BTDC on the engine data plate. Both are core annual
and 100-hour tasks. Follow the engine manufacturer's current SB/SI and the magneto
manufacturer's manual for the exact values — they change between engine models.

## 1. Differential compression ("leak-down") test
**Kit:** differential compression tester with 80 psi regulated input, restrictor orifice
(0.040 in, 0.250 in long, 60° approach on most testers) and a **calibrated master orifice**
(Continental SB03-3 method). Shop air ≥ 100 psi, clean and dry.

1. Run the engine to normal operating temperature first — a cold test reads pessimistic.
2. Remove the top spark plug from each cylinder. Make sure magnetos are OFF and P-leads
   grounded; treat the propeller as live.
3. **Calibrate:** connect the master orifice to the tester, set 80 psi input, and read the
   cylinder gauge. That reading (e.g. 52 psi on a given day/tester) is the *minimum
   acceptable* value today. Write it on the work order.
4. Bring the piston to TDC on the compression stroke (thumb on the plug hole feels
   pressure, then align the TDC mark or use a TDC indicator). Connect the tester.
5. Apply air slowly; hold the prop firmly (with a helper on a prop, never alone at the
   arc) — at 80 psi a piston just off TDC will spin the prop violently.
6. Rock the prop slightly to seat the rings and find the highest reading; record it as
   `xx/80`.
7. If below the master-orifice value, **listen** for where the air goes:
   - Exhaust stack → exhaust valve
   - Induction/air intake → intake valve
   - Crankcase breather/oil filler → rings
   - Adjacent plug hole → cracked head or blown gasket
8. Before condemning: run the engine and retest; a stuck carbon flake can hold a valve
   open. Borescope any low cylinder (look for burned/channelled exhaust-valve margins,
   scoring). Lycoming and Continental say a low reading alone, with good borescope and oil
   analysis, does not necessarily mean pulling the cylinder.

## 2. Magneto-to-engine timing
**Kit:** timing light/buzz box (e.g. Eastern Technology E50), timing disc or protractor/TDC
locator, the engine data plate value (typically 20°–25° BTDC; e.g. many O-320/O-360 at 25°
— check yours).

1. Find No. 1 cylinder on compression. Rotate in normal direction to the specified BTDC
   mark (flywheel/starter ring marks or a timing disc on the prop hub). Always approach
   the mark in the direction of rotation to take up gear backlash.
2. Connect the buzz box leads to each magneto's P-lead terminal (with the P-leads
   disconnected from the switch harness) and ground to the engine.
3. Loosen the magneto clamp nuts. Rotate the magneto housing until the points *just open*
   (buzz box light/tone changes) exactly at the mark. For Slick and Bendix/TCM magnetos,
   internal E-gap timing must already be correct — set per their manual first.
4. Tighten clamps to the specified torque, then back the prop off ~10° and bring it up to
   the mark again; both magnetos should "break" within the tolerance (usually ±1° of
   the spec and of each other).
5. Reconnect P-leads; on run-up, mag drops should be within POH/engine limits (commonly
   ≤ 175 rpm on either, ≤ 50 rpm difference). Check the P-lead ground: switch to OFF at
   idle briefly — the engine must stop firing.

## Gotchas
- A "hot mag" (broken P-lead) can start the engine while you turn the prop — test
  continuity of P-leads before handling the prop.
- Retarded timing → hot CHTs; advanced → detonation risk. Never "tune by ear".
- Impulse couplings click on the start side only; turning backwards past them can damage pawls.
- Uncertain: tester orifice specs and limits here are from commonly published SB03-3
  practice; confirm the revision in force for your engine.

## Verify
- [ ] Master-orifice calibration value recorded with each cylinder reading and leak path.
- [ ] Any low cylinder borescoped and re-tested hot before a removal decision.
- [ ] Both magnetos break at the data-plate BTDC within tolerance, approached in rotation direction.
- [ ] Clamp nuts torqued, P-leads reconnected and grounding check passed on run-up.
- [ ] Logbook entry lists readings, timing value and data references.
