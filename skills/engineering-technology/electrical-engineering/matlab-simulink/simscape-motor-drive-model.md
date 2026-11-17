---
id: engineering-technology.electrical-engineering.matlab-simulink.simscape-motor-drive-model
name: simscape-motor-drive-model
category: engineering-technology
field: electrical-engineering
product: matlab-simulink
tags: [electrical-engineering, matlab, matlab-simulink, pmsm-model, simscape-electrical, simscape-field-oriented-control, simscape-inverter-averaged-model, simscape-motor-drive, simscape-motor-drive-model]
level: advanced
status: draft
description: "Model a PMSM drive in Simscape Electrical: machine block, inverter, field-oriented control and averaged vs switching inverter models."
sources:
  - "https://www.mathworks.com/help/sps/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Motor drive model in Simscape Electrical

1. **Plant:** use a PMSM block with parameters from the machine datasheet (stator resistance, d and q inductances, flux linkage or back-EMF constant, pole pairs, inertia, friction); attach a mechanical load (torque source or inertia) through the rotational connectors.
2. **Inverter:** choose the switching-level converter (detailed switch blocks driven by PWM, requires a small fixed step) or an averaged converter (voltage source driven by duty ratios, allows larger steps for control design).
3. **Control:** implement field-oriented control in Simulink: Clarke/Park transforms (library blocks exist), two PI current controllers with dq decoupling, speed PI loop, and SVPWM or PWM generation. Sample the controller at the PWM rate with a discrete sample time.
4. **Sensors and measurement:** use ideal current/voltage sensors with Simscape-to-Simulink converters; add measurement delay and quantisation if needed for realism.
5. **Tuning:** place current loop bandwidth at a tenth of PWM frequency; tune with the Control System Tuner on a linearised model or use pole placement formulas.
6. **Step workflow:** simulate with the speed reference step, then add load torque disturbance; log phase currents, `id`, `iq`, torque and DC bus voltage.

**Caveat:** block names, library paths and parameter sets are described from general Simscape Electrical practice; confirm in the installed release documentation (draft, not re-run in this entry).

**Verify:** `id` follows 0 within a few percent and torque follows `iq` linearly; compare the averaged and switching models at the same operating point.

**Scope note:** Professional guidance only: design, selection, settings and sign-off belong to a qualified engineer or licensed electrician working to the code and standard editions adopted in the project jurisdiction. Standard clause numbers, limits and table values cited from memory are unconfirmed against the paywalled text (gated: unconfirmed, source is paywalled or blocked); worked arithmetic was recomputed.
