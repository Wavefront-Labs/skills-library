---
id: energy-mining-utilities.renewable-energy-field-operations.wind-turbine-maintenance.wind-turbine-scheduled-service-and-pitch-fault-finding
name: wind-turbine-scheduled-service-and-pitch-fault-finding
category: energy-mining-utilities
field: renewable-energy-field-operations
product: wind-turbine-maintenance
tags: [renewable-energy-field-operations, wind-turbine-maintenance, wind-turbine, wtg, wind-technician, scheduled-service, annual-service, rotor-lock, loto, lockout-tagout, bolt-torque, bolt-tensioning, gearbox-oil, oil-sample, main-bearing, grease, pitch-system, pitch-battery, pitch-accumulator, pitch-motor, encoder, blade-angle, yaw-system, yaw-brake, converter-fault, gwo, climbing, rescue, nacelle]
level: advanced
status: draft
description: "Carry out a wind turbine scheduled service up-tower and fault-find a pitch system: LOTO and rotor lock, bolt torque checks, gearbox oil, pitch battery and encoder faults."
sources:
  - "GWO (Global Wind Organisation) Basic Safety Training and Basic Technical Training modules, concepts paraphrased"
  - "OEM service manual structure (generic), paraphrased; no OEM-proprietary procedures reproduced"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Wind turbine scheduled service and pitch fault-finding

**Goal:** get through a scheduled service safely and properly, and when the turbine trips on
a pitch fault, find the cause rather than resetting it until it stays tripped.

This is generic; every OEM (Vestas, Siemens Gamesa, GE, Nordex, Enercon, Goldwind...) has
its own service manual, torque tables and lock procedures — those govern.

## 1. Before climbing
- Valid GWO (or equivalent) training, rescue kit and a rescue plan; at least two
  technicians on site (never climb alone).
- Check wind speed against OEM limits for climbing, nacelle access, roof work and **hub
  entry** (hub entry usually has the lowest limit). Check lightning forecast — leave the
  turbine if storms approach.
- Agree the work with the control room; turbine to **service mode**, remote control
  blocked.

## 2. Make it safe
1. Stop the turbine, pitch blades to feather, apply yaw brake/lock as required.
2. **Rotor lock** engaged per OEM (mechanical lock pin at low speed, never at speed).
3. LOTO on the electrical isolation points for the work (main breaker, pitch, hydraulics);
   verify dead. Stored energy: pitch accumulators/batteries and hydraulic pressure must be
   discharged or locked out before working on them.

## 3. Scheduled service — typical scope
- **Bolts:** blade root, hub, main shaft, tower flanges — torque/tension check per
  the sampling regime (e.g. 10% sample, then 100% if any fail). Use calibrated tools; mark
  bolts after checking.
- **Gearbox:** oil level, sample from the correct point (running-temperature oil, clean
  bottle) for lab analysis; filter change; inspect for leaks; borescope if CMS flagged.
- **Lubrication:** main/pitch/yaw bearings and gear teeth with the specified grease and
  quantity; empty grease collectors (over-greasing blows seals).
- **Generator:** brushes and slip rings (on DFIG), cooling, cables, insulation.
- **Yaw:** brake pads/calipers, gear teeth, yaw motors.
- **Safety systems:** emergency stops, overspeed tests, fire detection, lift and fall-arrest.
- **Pitch:** see below.
Log every reading; the next team relies on it.

## 4. Pitch fault-finding
Common causes in rough order:
1. **Pitch battery/accumulator** — failed capacity or pre-charge test (batteries age;
   accumulators lose nitrogen pre-charge). Often trips during the automatic test.
2. **Encoder / position sensor** — angle mismatch between blades, noisy signal; check
   connectors in the hub (vibration loosens them) and compare blade angles.
3. **Pitch motor / drive** — overcurrent from a stiff bearing or lack of grease; brake not
   releasing.
4. **Slip ring** between nacelle and hub — intermittent communication or supply faults.
5. **Hydraulic pitch:** pressure, leaks, valve faults, oil contamination.
Use the controller's fault log with timestamps: which blade, which state (running, test,
stop), and what changed just before. Fix the cause, then reset once.

## Gotchas
- Resetting a pitch fault repeatedly can leave a blade unable to feather in an emergency
  — overspeed risk.
- Never trust a "dead" circuit in the hub without testing; pitch systems have their own
  energy storage.
- Torque values change with lubricant; use the one in the procedure.

## Verify
- [ ] Wind limits, two-person rule, rescue plan and control-room handover in place.
- [ ] Rotor lock and LOTO applied and verified; stored energy discharged.
- [ ] Bolt, oil, grease and safety checks completed and logged.
- [ ] Pitch fault cause identified and tested (battery/accumulator test passes).
- [ ] Turbine returned to auto with control room; first runs monitored.

*Uncertain:* limits and procedures are OEM- and site-specific; this skill is a framework.
