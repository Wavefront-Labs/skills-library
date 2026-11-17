---
id: repair-maintenance.motorcycle-small-engine-repair.motorcycle-electrical-systems.charging-system-stator-and-regulator-testing
name: charging-system-stator-and-regulator-testing
category: repair-maintenance
field: motorcycle-small-engine-repair
product: motorcycle-electrical-systems
tags: [motorcycle-electrical-systems, motorcycle-charging, stator, regulator-rectifier, reg-rec, rectifier, mosfet-regulator, charging-voltage, ac-output-test, stator-resistance, insulation-test, battery-drain, parasitic-draw, multimeter, burnt-connector, three-phase, permanent-magnet-alternator, flat-battery, overcharging, lithium-motorcycle-battery]
level: practitioner
status: draft
description: "Diagnose a motorcycle that won't charge: battery check, charging voltage at rpm, stator AC output and resistance, insulation to ground, regulator-rectifier diode tests and the burnt connector."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Charging system: stator and regulator-rectifier testing

**Goal:** find out in 20 minutes whether a flat-battery bike has a bad battery, a bad
stator, a bad regulator-rectifier, or (very often) a burnt connector — before buying parts.

Most modern bikes use a **permanent-magnet alternator** (stator under a side cover,
magnets in the flywheel/rotor) feeding a **regulator-rectifier** (reg/rec) that turns
3-phase AC into ~14 V DC. *Exact values come from the model's service manual — the
numbers below are typical.*

## Tools
Digital multimeter (DC V, AC V, Ω, diode test), service manual wiring diagram,
battery charger, contact cleaner, dielectric grease.

## 1. Start with a known-good, charged battery
1. Charge fully. Rest ≥1 h. Lead-acid/AGM 12 V: **≥12.6–12.8 V**. Lithium: per maker
   (often ~13.2–13.4 V).
2. Load/start test: voltage shouldn't drop below ~9.6–10 V while cranking (lead-acid).
3. A battery that won't hold charge overnight with nothing connected is the battery.
4. **Parasitic draw**: ignition off, meter (A, 10 A range first) in series with the
   negative lead. Typically under ~1–3 mA on bikes with a clock/ECU memory; tens of mA
   or more = something draining (alarm, tracker, faulty relay). Pull fuses one at a time
   to find the circuit.

## 2. Charging voltage
Engine running, headlight on, meter on battery terminals:
- Idle: ~13.0–13.5 V; at **~3,000–5,000 rpm**: **~13.8–14.8 V**.
- Below ~13 V at rpm → not charging → continue.
- Above ~15 V → regulator failing (overcharging; boils or swells batteries).

## 3. Inspect the connectors (do this before buying anything)
Follow the stator wires (usually **three of the same colour**, often yellow or
white) to the reg/rec plug. **Brown/melted/blackened pins** are extremely common —
high current through a corroded or loose pin overheats. Repair with new terminals or
solder the stator leads directly (heat-shrink each), and fix the root cause
(corrosion, poor regulator ground, old shunt regulator).

## 4. Stator tests (plug unplugged from the reg/rec)
1. **Resistance between phases** (1–2, 2–3, 1–3), engine off: typically **0.1–1.0 Ω**
   and all three **equal**. Subtract meter lead resistance (touch leads together first).
   Open circuit (OL) = broken winding.
2. **Insulation to ground**: each stator wire to engine ground should read **OL/infinite**.
   Any continuity = shorted winding → replace stator.
3. **AC output** (most important — a stator can pass resistance and still fail under
   heat): engine running, meter on **AC volts** between each pair of stator wires. At idle
   often ~15–25 VAC; at ~5,000 rpm often **~50–80 VAC**, and the three readings should
   **match within a few volts**. One low phase = failing stator.
   Test hot as well as cold — insulation breaks down with heat.

## 5. Regulator-rectifier tests
- **Diode test** (unplugged): between each stator input and the reg/rec's DC + and −
  outputs the rectifier should conduct one way (~0.3–0.7 V on diode test) and read OL
  the other. Shorted both ways or open both ways = faulty. Results vary on MOSFET types;
  the manual's table is authoritative.
- **Grounding**: the reg/rec case and its ground wire must have a clean path to the
  battery negative — voltage-drop test it (should be <0.2 V).
- If the stator AC output is good, connectors are good and charging voltage is still
  low or high → replace the reg/rec. Upgrading to a **MOSFET-type** regulator runs
  cooler and is common on bikes with a known regulator weakness.

## 6. Ignition-related tie-ins
Low charging voltage can cause misfires, ECU faults and fuel pump drop-outs on EFI
bikes; fix charging before chasing "ignition problems".

## Gotchas
- Don't test by disconnecting the battery with the engine running (old car trick) —
  it can destroy the reg/rec and electronics.
- Lithium batteries need a compatible charger and reg/rec voltage; very deep discharge
  can trip their BMS.
- Aftermarket heated grips, lights and USB chargers can exceed the alternator's spare
  output at idle — check the manual's rated output.

## Verify
- [ ] Battery confirmed good (rest voltage, load test, parasitic draw).
- [ ] Charging voltage measured at idle and ~4,000 rpm; recorded.
- [ ] Connectors inspected; burnt pins repaired.
- [ ] Stator: equal phase resistance, no short to ground, balanced AC output hot.
- [ ] After repair, 13.8–14.8 V at rpm with lights on.
