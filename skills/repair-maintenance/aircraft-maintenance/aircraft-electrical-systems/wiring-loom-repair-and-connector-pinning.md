---
id: repair-maintenance.aircraft-maintenance.aircraft-electrical-systems.wiring-loom-repair-and-connector-pinning
name: wiring-loom-repair-and-connector-pinning
category: repair-maintenance
field: aircraft-maintenance
product: aircraft-electrical-systems
tags: [aircraft-maintenance, aircraft-electrical-systems, aircraft-wiring, ewis, wire-splice, crimp-splice, d-sub, mil-dtl-38999, ms3106, connector-pinning, contact-insertion-tool, crimp-tool, daniels, m22520, tefzel, m22759, wire-gauge, awg, bus-fault, milliohm, insulation-resistance, megger, ac-43-13, as50881, chafing]
level: practitioner
status: draft
description: "Repair chafed aircraft wiring with environmental crimp splices, re-pin connectors with calibrated M22520 tools, and prove it with continuity, insulation-resistance and pull tests."
sources: ["FAA AC 43.13-1B ch. 11 Aircraft Electrical Systems", "SAE AS50881 Wiring Aerospace Vehicle", "FAA AC 25.1701-1 (EWIS) - background"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Wiring loom repair and connector pinning

**Goal:** return a damaged wire or connector to its original electrical and
environmental performance using approved materials and calibrated tools, without
creating a new chafe point. On transport aircraft the Standard Wiring Practices Manual
(SWPM, e.g. ATA chapter 20) for that type governs; on light aircraft AC 43.13-1B ch. 11.

## 1. Find and scope the damage
- Typical causes: chafing on structure/clamps, heat near exhausts, fluid contamination,
  broken conductors at connector backshells from vibration.
- Isolate the circuit: pull the breaker, get the wiring diagram (wire number, gauge,
  type e.g. M22759/16-20-9 = 20 AWG Tefzel white).
- Expose the loom: cut lacing/ties carefully, never knife-slit along wires.
- Measure: continuity end-to-end (≤ fractions of an ohm for short runs — compare to
  wire resistance per foot), insulation resistance to structure with a megohmmeter
  (e.g. 500 V DC, typical acceptance > 100 MΩ, confirm the SWPM value and *disconnect
  avionics* before megging).

## 2. Splice repair
Rules of thumb (SWPM/AC 43.13 decide):
- Insulation scuffed but conductor intact → may be repaired with approved sleeve;
  any exposed or broken strands → splice or replace.
- **Environmental crimp splices** (e.g. M81824/1 style, heat-shrink sealed), sized to the
  wire gauge (colour-coded).
- Stagger splices in a bundle so they don't stack (bundle diameter); keep splices out of
  bends, clamps and ≥ ~12 in from connectors where practicable.
- Max splices per wire segment is limited (often one between connectors) — check.
- Strip with a precision thermal or calibrated mechanical stripper: no nicked or cut strands.
- Crimp with the tool and die set specified for the splice; full-cycle ratchet must
  release only at full compression.
- Shrink with a heat gun using the right reflector; no scorching of adjacent wires.
- Replacement wire must match spec (type, gauge, temperature rating, shielding).
  Shielded wire: terminate the shield with a solder sleeve and keep pigtails short.

## 3. Connector pinning (circular MIL-DTL-38999 / MS3106, D-sub)
1. Identify contact part number and size (e.g. size 20, 22D). Get the insertion/extraction
   tool for that size — plastic tools for rear-release, metal for some front-release.
2. **Extract** from the rear: slide the tool along the wire into the grommet until it
   releases the retention clip; pull wire and tool together. Never force.
3. Crimp a new contact with an **M22520** crimper (e.g. M22520/1-01 with the correct
   positioner turret), selector set to the wire gauge per the positioner data plate.
   Inspection hole: conductor visible, insulation gap 0.5–1 mm short of the barrel.
4. **Insert** from the rear until it clicks; tug test lightly (5–10 lb pull is a common
   field check; contact datasheet gives retention force).
5. Seal unused cavities with the correct sealing plugs — empty grommet holes let moisture in.
6. Re-clamp the backshell and strain relief; reinstate any lacing.

## 4. Routing and protection
- Restore clamps (cushioned, correctly sized) and minimum bend radius (typically 10×
  bundle diameter, 3× for single wires — check).
- Keep ≥ 1/2 in from structure edges / grommet holes (use grommets or chafe strips) and
  separated from fuel, hydraulic and oxygen lines; wires above, never below, fluid lines.
- Re-identify wire with sleeves or printed markers at the original intervals.

## Gotchas
- Tool calibration matters: an out-of-cal crimper makes a joint that passes continuity
  and fails in vibration. Check the go/no-go gauge before each job.
- Solder splices are generally *not* acceptable in place of crimp splices on aircraft wiring.
- Mixing contact plating (gold vs tin) causes fretting corrosion.
- Uncertain: specific numbers (megger voltage, pull force, bend radii) differ per SWPM.

## Verify
- [ ] Wire spec and contact part numbers match the wiring diagram and connector.
- [ ] Crimp tool and positioner verified with the gauge; crimp inspection hole correct.
- [ ] Continuity end-to-end and insulation resistance to structure within limits.
- [ ] Contacts pass retention tug; unused cavities plugged; backshell secured.
- [ ] Routing, clamps and separation restored; function test of the circuit passed.
