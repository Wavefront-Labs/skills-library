---
id: engineering-technology.automotive-vehicle-engineering.matlab-simulink.real-time-plant-model-simplification
name: real-time-plant-model-simplification
category: engineering-technology
field: automotive-vehicle-engineering
product: matlab-simulink
tags: [realtime-plant-model, hil-preparation, hil, real-time, plant-model, fixed-step, simulink-real-time, model-reduction, turnaround-time, task-execution-time, overrun]
level: practitioner
status: gated
description: "Reduce a vehicle plant model so it runs inside its fixed step on a HIL target: find stiff subsystems, cut states, swap solvers, and prove execution time headroom."
sources:
  - "MathWorks: Estimate computation costs (https://www.mathworks.com/help/simscape/ug/estimate-computation-costs.html)"
  - "Simulink Rate Transition block (https://www.mathworks.com/help/simulink/slref/ratetransition.html)"
  - "Simulink Real-Time: execution profiling (https://www.mathworks.com/help/slrealtime/ug/execution-profiling-for-real-time-application.html)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Real-time plant model simplification

**Goal:** a plant that executes every step in well under the step size on the real-time target, with the accuracy the controller test actually needs.

## 1. Set the step size from the controller test, not from habit
Typical HIL base steps are 1 ms (powertrain, chassis) and 50-100 us or less for power electronics/motor current loops (industry practice (gated: unconfirmed, source is paywalled or blocked)). The plant must resolve the fastest dynamics the ECU can excite: brake hydraulics, tyre relaxation at low speed, inverter current loop. Anything faster than the step is modelled as a static or quasi-static element.

## 2. Measure before cutting
Run the model on the target (or in Accelerator mode with profiling) and record **task execution time (TET)** per step. For fixed-step solvers the minimum step is Ts_min = TET_max + HLT_max (HLT = hardware latency time; Simscape "Estimate Computation Costs" page, whose example reserves a 20% margin). Common team thresholds of 70-80% of the step (gated: unconfirmed, source is paywalled or blocked); confirm your own with the HIL vendor. Look at the worst-case sample, not the mean: an overrun on a rare step still invalidates the test.

## 3. Cut cost in this order
1. Replace variable-step or algebraic-loop subsystems (tyre slip with implicit solves, hydraulics with stiff orifice equations) by fixed-step friendly forms: first-order lags, explicit relaxation-length tyre models.
2. Replace online-computed maps (engine, motor efficiency, battery OCV) by 1-D/2-D lookup tables with precomputed breakpoints; share pre-lookup blocks across tables.
3. Reduce states: drop wheel-hop or body-bounce DOFs if the ECU function (cruise control, TCU shift) is insensitive; keep them for ABS/ESC and damper control tests.
4. Split rates: run slow thermal and SOC dynamics at 10-100 ms and fast electrical dynamics at the base step, with explicit Rate Transition blocks (watch the latency each adds).
5. Remove scopes, `To Workspace`, and logging not needed on target; log through the real-time tool's signal logging instead.
6. Use the fixed-step solver the target requires (`ode1`/`ode3` fixed-step is common); verify results against the variable-step offline model with an agreed tolerance.

## 4. Check accuracy after every cut
Run the same manoeuvre (WLTC, step-steer, brake stop) on the full offline model and the reduced one; compare the signals the ECU reads. Set the acceptance in advance (for example speed error within a few percent, no phase shift visible at the controller's crossover frequency).

## Failure modes
- Algebraic loops hidden in the plant: a one-step unit delay fixes it only if the physics tolerates it.
- Integrator drift from fixed-step integration at too coarse a step: SOC or position wanders at standstill.
- Overrun appears only when many ECU faults are injected (extra branches execute): test the worst case.

## Verify
- [ ] Step size justified by the fastest dynamic the test excites.
- [ ] Worst-case TET measured on the target with the agreed headroom.
- [ ] Reduced vs full model comparison recorded with tolerances.
- [ ] No algebraic loops, no variable-step blocks, no unintended Rate Transition delays.
