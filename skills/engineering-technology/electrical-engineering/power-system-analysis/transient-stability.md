---
id: engineering-technology.electrical-engineering.power-system-analysis.transient-stability
name: transient-stability
category: engineering-technology
field: electrical-engineering
product: power-system-analysis
tags: [critical-clearing-time, electrical-engineering, equal-area-criterion, inertia-constant, power-system-analysis, rotor-angle-stability, swing-equation, transient-stability]
level: advanced
status: draft
description: "Assess rotor-angle transient stability with the swing equation, equal-area criterion and critical clearing time."
sources:
  - "https://standards.ieee.org/"
  - "https://www.ncees.org/engineering/pe/electrical-computer/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Transient stability: swing equation and equal-area criterion

- **Swing equation (per unit):** `(2H / w_s) d2delta/dt2 = Pm - Pe`, `Pe = Pmax sin(delta)`, delta in radians, `w_s = 2 pi f`.
- **Equal-area:** the system is stable if the accelerating area during the fault `A1` can be matched by decelerating area `A2` before `delta_max = pi - delta_0` (post-fault).
- **Critical clearing angle (fault with Pe = 0):** `cos(delta_cr) = (Pm/Pmax)(delta_max - delta_0) + cos(delta_max)`.
- **Critical clearing time (Pe = 0 during the fault):** `t_cr = sqrt(2 H (delta_cr - delta_0) / (pi f Pm))`.
- **Example:** H = 5 s, f = 60 Hz, Pm = 0.8, Pmax = 2.0. `delta_0 = 0.4115` rad, `delta_max = 2.7301`, `cos(delta_cr) = 0.4 x 2.3186 - 0.9165 = 0.0109`, `delta_cr = 1.560` rad, `t_cr = 0.28 s`.
- **Practice:** real studies use time-domain simulation with generator, exciter, governor and load models in a dynamic study tool; the single-machine infinite-bus model gives screening intuition. Faster breakers, higher H, and greater post-fault transfer capability extend `t_cr`.

**Verify:** simulate the same case and see the angle swing recover when clearing at 90 percent of `t_cr` and diverge at 110 percent.

**Scope note:** Professional guidance only: design, selection, settings and sign-off belong to a qualified engineer or licensed electrician working to the code and standard editions adopted in the project jurisdiction. Standard clause numbers, limits and table values cited from memory are unconfirmed against the paywalled text (gated: unconfirmed, source is paywalled or blocked); worked arithmetic was recomputed.
