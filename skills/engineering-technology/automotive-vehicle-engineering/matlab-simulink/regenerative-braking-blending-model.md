---
id: engineering-technology.automotive-vehicle-engineering.matlab-simulink.regenerative-braking-blending-model
name: regenerative-braking-blending-model
category: engineering-technology
field: automotive-vehicle-engineering
product: matlab-simulink
tags: [regen-blending-model, regenerative-braking, brake-blending, friction-brake, ev, simulink]
level: practitioner
status: gated
description: "Model regenerative and friction brake blending in Simulink with motor torque limits, battery power limits and front/rear distribution."
sources:
  - "Ehsani et al., Modern Electric, Hybrid Electric and Fuel Cell Vehicles"
  - "FMVSS 135 (https://www.ecfr.gov/current/title-49/part-571/section-571.135)"
  - "UN Regulation No. 13-H (https://unece.org)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Regen blending model

1. Driver brake pedal -> requested deceleration -> total wheel brake torque `Tb_total = m*a_req*Re` (with grade and road load as needed).
2. Axle split: set the ideal/limited front-rear distribution first; regen applies only on the driven axle.
3. Regen limit per axle: `T_regen = min(T_motor_max(w), P_batt_charge_max/w, T_split_request)`, converted through gear ratio; set to zero below a minimum speed (around walking pace (gated: unconfirmed, source is paywalled or blocked)) where motor torque and efficiency collapse.
4. Friction = total - regen on that axle, with rate limiting so the sum stays smooth when regen fades.
5. Respect stability rules: the regen axle must stay within the brake-distribution limits of the governing regulation (UN R13-H and FMVSS No. 135 "Light vehicle brake systems", 49 CFR 571.135, which applies to passenger cars and to vehicles up to 3,500 kg GVWR; confirm current editions).
6. Report energy recovered = integral of regen power x efficiency chain.

**Gotchas:** at high SOC or cold battery, charge power limits drop to near zero; the controller must cover this instantly with friction.

## Verify
- [ ] Total deceleration follows demand within tolerance when regen limit steps to zero.
- [ ] Recovered energy fraction is plausible (tens of percent of braking energy, depends on cycle (gated: unconfirmed, source is paywalled or blocked)).
