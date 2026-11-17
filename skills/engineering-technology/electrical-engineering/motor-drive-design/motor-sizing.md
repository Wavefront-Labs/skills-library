---
id: engineering-technology.electrical-engineering.motor-drive-design.motor-sizing
name: motor-sizing
category: engineering-technology
field: electrical-engineering
product: motor-drive-design
tags: [duty-cycle-thermal-sizing, electrical-engineering, load-torque-speed-curve, motor-drive-design, motor-selection, motor-sizing, rms-torque, service-factor]
level: practitioner
status: draft
description: "Size and select a motor from load torque-speed, duty cycle and thermal limits, with service factor and derating."
sources:
  - "https://www.iec.ch/"
  - "https://www.nema.org/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Motor sizing and selection

1. Define the load: required shaft power `P = T w`, torque-speed curve (constant torque, variable torque such as fans and pumps `T ~ n^2`, constant power), starting torque and inertia.
2. Power from process: pump `P = rho g Q H / eta`, fan `P = Q dp / eta`, hoist `P = m g v / eta`.
3. **Duty cycle:** compute RMS torque over the cycle, `T_rms = sqrt(sum(T_i^2 t_i)/sum t_i)`, and choose a motor with continuous torque above it; reduce for low speed with self-cooled motors on drives.
4. **Margins:** the motor breakdown (pull-out) torque must exceed the peak load torque under 90 percent voltage; starting torque must exceed the load breakaway torque with margin.
5. **Derating:** altitude above 1000 m and ambient above 40 C reduce rating (check the manufacturer); service factor 1.15 is available margin, not a design target.
6. **Inertia:** check the acceleration time `t = J dw / (T_motor_avg - T_load)` against the thermal capability for repeated starts.
7. Choose frame, enclosure (IP), cooling and insulation class (class F with B rise is common).

**Verify:** compare the calculated load point with the motor datasheet efficiency and current; confirm steady-state temperature rise at the duty.

**Scope note:** Professional guidance only: design, selection, settings and sign-off belong to a qualified engineer or licensed electrician working to the code and standard editions adopted in the project jurisdiction. Standard clause numbers, limits and table values cited from memory are unconfirmed against the paywalled text (gated: unconfirmed, source is paywalled or blocked); worked arithmetic was recomputed.
