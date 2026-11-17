---
id: engineering-technology.electrical-engineering.motor-drive-design.vector-control
name: vector-control
category: engineering-technology
field: electrical-engineering
product: motor-drive-design
tags: [clarke-park, current-loop-tuning, d-q-axis, electrical-engineering, field-oriented-control, foc, motor-drive-design, pmsm-control, sensorless-estimation, vector-control]
level: advanced
status: draft
description: "Implement field-oriented control: Clarke and Park transforms, current loop tuning, and sensorless estimation."
sources:
  - "https://standards.ieee.org/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Vector (field-oriented) control

1. **Transforms:** Clarke `(a,b,c) -> (alpha,beta)`, Park `(alpha,beta) -> (d,q)` using the rotor electrical angle `theta_e`; in the rotating frame torque is `T = 1.5 p (psi_m iq + (Ld - Lq) id iq)` for a PMSM, so control `iq` for torque and `id = 0` (or negative for field weakening / MTPA).
2. **Current loops:** PI per axis, `Kp = L * wc`, `Ki = R * wc` with bandwidth `wc` typically 1/10 to 1/20 of the PWM frequency (limited by sample delay); add decoupling feed-forward `-w_e L iq` and `w_e (L id + psi_m)`.
3. **Speed loop** bandwidth about 5 to 10 times lower than the current loop; anti-windup with saturation of the current reference.
4. **Sensors:** encoder or resolver, calibrated offset between rotor flux axis and the sensor.
5. **Sensorless:** back-EMF observers (sliding-mode or PLL) at medium and high speed; high-frequency injection at standstill for salient machines; startup in open-loop I/f then handover.
6. Limit voltage vector to the DC bus (space vector limit `Vdc/sqrt(3)`).

**Verify:** step-respond the d/q current loops and compare measured bandwidth to design; check the current waveform for sensor offset ripple.

**Scope note:** Professional guidance only: design, selection, settings and sign-off belong to a qualified engineer or licensed electrician working to the code and standard editions adopted in the project jurisdiction. Standard clause numbers, limits and table values cited from memory are unconfirmed against the paywalled text (gated: unconfirmed, source is paywalled or blocked); worked arithmetic was recomputed.
