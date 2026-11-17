---
id: engineering-technology.automotive-vehicle-engineering.matlab-simulink.drive-cycle-vehicle-plant-model
name: drive-cycle-vehicle-plant-model
category: engineering-technology
field: automotive-vehicle-engineering
product: matlab-simulink
tags: [matlab, simulink, powertrain-blockset, vehicle-dynamics-blockset, plant-model, longitudinal-dynamics, drive-cycle, wltp, wltc, ftp-75, road-load, coastdown, fixed-step-solver, ode4, data-dictionary, sldd, model-reference, mil, sil, pil, hil, simulink-real-time, speedgoat, embedded-coder, energy-consumption, vehicle-simulation, hil-preparation, vehicle-longitudinal-model, drive-cycle-simulation]
level: practitioner
status: gated
description: "Build a longitudinal vehicle/powertrain plant in Simulink driven by WLTP/FTP-75, choose fixed-step solvers, manage data dictionaries and step it MIL to SIL to HIL."
sources:
  - "MathWorks Powertrain Blockset and Vehicle Dynamics Blockset documentation: Longitudinal Driver (https://www.mathworks.com/help/vdynblks/ref/longitudinaldriver.html)"
  - "MathWorks: Choose a solver (https://www.mathworks.com/help/simulink/ug/choose-a-solver.html)"
  - "MathWorks: Estimate computation costs (https://www.mathworks.com/help/simscape/ug/estimate-computation-costs.html)"
  - "EPA dynamometer drive schedules (https://www.epa.gov/vehicle-and-fuel-emissions-testing/dynamometer-drive-schedules)"
  - "UN GTR No. 15 (WLTP) (https://unece.org)"
licence: Apache-2.0
version: 5
updated: 2026-11-17
aliases: []
---

# Drive-cycle vehicle plant model in Simulink (and getting it HIL-ready)

**Goal:** a longitudinal vehicle + powertrain plant that follows WLTC or FTP-75, predicts
energy/fuel within a few percent of test data, and runs unchanged from desktop MIL to a
real-time HIL target. Controller design itself is a separate skill; this is the plant.

## 1. Start from a reference application, not a blank canvas
Powertrain Blockset ships conventional, EV and hybrid (P0–P4) reference applications
(open them from the Blockset's examples page; names vary by release). They already wire **Drive Cycle Source** →
**Longitudinal Driver** (a PI driver with feed-forward) → controller → plant →
**Vehicle Body 1DOF Longitudinal**. Strip what you do not need; keep the signal buses.
Vehicle Dynamics Blockset's 3DOF/14DOF bodies are for lateral/pitch work (e.g. torque
vectoring), not cycle energy.

## 2. The longitudinal equation you are actually solving
```
m_eff · dv/dt = F_tractive − F_roadload − m·g·sin(θ)
F_roadload    = A + B·v + C·v²          (coastdown coefficients, a.k.a. F0, F1, F2)
m_eff         = m · (1 + δ)             (δ ≈ 0.03–0.05 for an EV, higher in low gears of an ICE; rule of thumb (gated: unconfirmed, source is paywalled or blocked))
```
Use measured coastdown A/B/C when you have them — they bundle tyre, bearing, brake drag and
aero; physical Crr/CdA terms are for concept work.

Worked check: A = 150 N, B = 1.0 N/(m/s), C = 0.42 N/(m/s)² at 100 km/h (27.8 m/s) gives
150 + 28 + 324 = 502 N → **14 kW at the wheels**. If your model needs 20 kW to cruise at
100 km/h, a unit or efficiency is wrong before you go any further.

## 3. Drive cycle input
- WLTC Class 3b: 1800 s, ~23.3 km (gated: unconfirmed, source is paywalled or blocked); FTP-75: UDDS plus a 10-minute soak and a repeat of its first 505 s (EPA dynamometer drive schedules page); take duration and distance from the regulation text you are certifying to (40 CFR Part 86 for FTP-75) — cycle variants exist (Class 3a, regional).
- Cycles are 1 Hz tables: interpolate linearly, or the driver PI spikes torque each second.
- Track speed error: WLTP allows roughly ±2 km/h / ±1 s around the trace (gated: unconfirmed, source is paywalled or blocked) (check the current GTR 15 amendment). If your driver violates that, the energy figure is invalid.
- Integrate distance and confirm it matches the cycle distance within ~0.5%.

## 4. Solver choice
- **Desktop exploration:** variable-step `ode23t` or `ode15s` handles stiff driveline
  compliance and clutch lock-up events efficiently.
- **Anything going to code generation or HIL:** fixed-step, usually `ode3` or `ode4`
  (or `ode1` for purely discrete controllers), base rate 1 ms for powertrain plants.
  Switch to fixed-step **early**: discontinuities, zero-crossings and algebraic loops that
  variable-step hid will appear now, not on the rig.
- Rule of thumb: step ≤ 1/10–1/20 of the period of the fastest mode you keep. A 10 Hz
  driveshaft torsional mode is fine at 1 ms; a stiff clutch model at 400 Hz is marginal —
  soften it or remove the mode deliberately and document why.
- Inverter switching and motor current loops (tens of µs) need an FPGA or averaged model.

## 5. Data dictionaries and model structure
- Put every parameter in a `.sldd` as `Simulink.Parameter` (with units and min/max) and
  every bus as `Simulink.Bus`. Store the configuration set in the dictionary too and use a
  Configuration Reference so MIL, SIL and HIL share one source of truth for solver/step.
- Variants (mass, battery size, ratio set) go in variant parameters or referenced
  dictionaries, not base-workspace scripts.
- Split controller and plant into separate **referenced models**. This is what lets you
  flip the controller to SIL later without touching the plant.

## 6. MIL → SIL → HIL
1. **MIL:** closed-loop on desktop; baseline energy/fuel on each cycle; save logged
   signals as the reference.
2. **SIL:** set the controller model reference to Software-in-the-loop (Embedded Coder).
   Run back-to-back against MIL in the same harness; differences usually come from data
   types, saturation or uninitialised states.
3. **PIL (optional):** same on the target processor for timing and fixed-point checks.
4. **HIL:** build the plant for a real-time target (Simulink Real-Time on Speedgoat, or a
   dSPACE/NI/ETAS flow), map bus signals to I/O or CAN, and watch task execution time —
   size the step so Ts >= TET_max + HLT_max (Simscape "Estimate Computation Costs" page; its worked example reserves a 20% margin; agree your own headroom with the HIL vendor). Any overrun invalidates the run.

## Gotchas
- Regen limits (battery charge power, friction-brake blending) move cycle energy by
  several percent; model the blending strategy, not just negative motor torque.
- Set thermal initial conditions deliberately: FTP-75 is a cold-start cycle.

## Verify
- [ ] Constant-speed road-load power matches the hand calculation from A/B/C.
- [ ] Driver stays inside the cycle speed tolerance; integrated distance matches the cycle.
- [ ] Model runs fixed-step at the HIL step with no algebraic loops and no warnings.
- [ ] All parameters, buses and the configuration set live in the data dictionary.
- [ ] SIL results match MIL within the agreed tolerance on every test cycle.
- [ ] HIL task execution time has margin and no overruns across a full cycle.
