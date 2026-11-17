---
id: repair-maintenance.heavy-equipment-industrial-machinery-repair.mobile-equipment-electrical.24v-charging-and-j1939-can-network-diagnosis
name: 24v-charging-and-j1939-can-network-diagnosis
category: repair-maintenance
field: heavy-equipment-industrial-machinery-repair
product: mobile-equipment-electrical
tags: [mobile-equipment-electrical, 24v, 24-volt, series-batteries, battery-disconnect, alternator, charging-system, voltage-drop-test, starter-circuit, ground-strap, load-test, j1939, can-bus, controller-area-network, can-h, can-l, terminating-resistor, 120-ohm, 60-ohm, backbone, stub, deutsch-connector, harness-repair, ecm, multimeter, oscilloscope, heavy-equipment-electrical]
level: practitioner
status: draft
description: "Diagnose 24V charging and starting on heavy equipment with voltage-drop tests, then fault-find J1939 CAN networks: 60-ohm termination, CAN-H/CAN-L voltages, and harness repair."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# 24 V charging/starting and J1939 network diagnosis

**Goal:** separate battery, cable, alternator and network faults on a heavy machine with
a multimeter and a few known values, then repair the harness so it stays fixed.

## 1. Know the system
- Most heavy equipment is **24 V**: two 12 V batteries in series (some machines four,
  as two series pairs in parallel). Charging voltage is roughly 27.5–28.5 V.
- Some machines have a 12 V tap off one battery for accessories — this unbalances the
  pair; the tapped battery dies early. Use a proper 24–12 V converter instead.
- Safety: battery banks deliver thousands of amps. Remove rings and watches, turn the
  battery disconnect off before working on cables, disconnect negative first, and keep
  sparks and grinding away from batteries (hydrogen). Some ECMs need a timed shutdown
  before the disconnect is turned off; follow the OEM sequence.

## 2. Batteries and charging
1. Each battery at rest: ~12.6 V full, ~12.2 V half. Test each battery separately; a
   24 V reading of 24.4 V can hide one battery at 11.6 V and one at 12.8 V.
2. Load or conductance-test each battery. Replace series batteries as a matched pair.
3. Engine running at fast idle, all loads on: system should hold about 27–28.5 V.
   Below 26 V = not charging; above ~29.5 V = regulator fault, boiling batteries.
4. Check the alternator belt, then the **output cable and ground voltage drops**.

## 3. Voltage-drop testing (the test that finds cable faults)
Measure across a circuit while it carries current — meter leads at each end of a
cable or connection, not to ground.
- Starter positive cable during cranking: under about 0.5 V.
- Starter ground path (starter case to battery negative): under about 0.5 V.
- Alternator output to battery positive while charging: under about 0.5 V.
(Draft note: OEMs publish specific drop limits; 0.5 V per side is a common
working figure, not a standard.)
A corroded frame ground strap is the classic cause of slow cranking and odd ECM
codes together.

## 4. J1939 CAN network
- Two twisted wires: **CAN-H (yellow)** and **CAN-L (green)**, plus shield on older
  three-wire harnesses. The backbone has a **120 Ω terminating resistor at each end**.
  Stubs to ECMs should be short (J1939 limits them to about 1 m).
- **Resistance check** (key off, battery disconnected): measure CAN-H to CAN-L at the
  9-pin diagnostic port.
  - ~60 Ω = both terminators present and backbone intact.
  - ~120 Ω = one terminator missing or the backbone open between them.
  - ~0 Ω = CAN-H shorted to CAN-L.
  - Open/very high = both terminators missing or port wiring open.
- **Voltage check** (key on): CAN-H to ground about 2.5–3.5 V, CAN-L to ground about
  1.5–2.5 V, the two summing near 5 V. Either one at 0 V or at battery voltage means a
  short to ground or to power.
- **Isolate**: unplug ECMs one at a time; when the network recovers, the last one
  unplugged (or its stub) is the fault. An oscilloscope shows reflections and noise
  that a meter cannot.

## 5. Harness and connector repair
- Use the OEM connector kit and the correct crimp tool for Deutsch DT/DTM/HD or AMP
  terminals; check pull-out after each crimp.
- Splice with sealed, adhesive-lined heat-shrink butt splices. Never twist-and-tape.
- For CAN wiring, keep the twist up to the splice and stagger splices.
- Do not pierce insulation with back-probes; it lets water wick into the copper.
- Re-route and clip the harness away from the chafe point that caused the damage.

## Gotchas
- Welding on a machine without disconnecting batteries and ECMs can destroy
  controllers — see the field welding skill
  `repair-maintenance.heavy-equipment-industrial-machinery-repair.field-welding-repair.crack-gouge-repair-and-hardfacing-wear-parts`.
- Jump-starting from a 24 V source onto a 12 V tap, or reversed, kills modules.
- Intermittent faults: wiggle-test harnesses at clamps, hinges and articulation joints.

## Verify
- [ ] Each battery tested separately; charging holds 27–28.5 V under load.
- [ ] Voltage drops on starter and charging cables within limits.
- [ ] CAN-H to CAN-L reads ~60 Ω at the port; voltages in range.
- [ ] Repairs sealed, harness secured, no communication codes after a work cycle.
