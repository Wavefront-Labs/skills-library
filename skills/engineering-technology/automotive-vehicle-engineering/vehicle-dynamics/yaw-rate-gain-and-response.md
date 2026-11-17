---
id: engineering-technology.automotive-vehicle-engineering.vehicle-dynamics.yaw-rate-gain-and-response
name: yaw-rate-gain-and-response
category: engineering-technology
field: automotive-vehicle-engineering
product: vehicle-dynamics
tags: [yaw-rate-gain, yaw-gain, yaw-damping, characteristic-speed, critical-speed, bicycle-model]
level: practitioner
status: gated
description: "Compute steady yaw-rate gain, characteristic or critical speed and yaw damping from the bicycle model and relate them to measured transient response."
sources:
  - "Gillespie, Fundamentals of Vehicle Dynamics"
  - "Milliken and Milliken, Race Car Vehicle Dynamics"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Yaw-rate gain and response

- Steady yaw gain: `r/delta = (V/L)/(1 + K*V^2/(L*g))` where K is the understeer gradient in rad per g (dimensionless) and V speed; with K in rad per (m/s^2) use `1 + K*V^2/L`. (The earlier form lacked L; recomputed: with K = 0.0236 rad/g and L = 2.7 m the gain peaks at V_char = 33.5 m/s and equals half the neutral-steer value there.)
- Understeer vehicle: gain peaks at the **characteristic speed** `V_char = sqrt(g*L/K)` (K in rad/g form: `V_char = sqrt(L*g/K_rad_per_g)`).
- Oversteer (K < 0): there is a **critical speed** `V_crit = sqrt(-g*L/K)` above which the steady response is unstable.
- Yaw damping comes from tyre cornering stiffnesses and wheelbase; it falls with speed and with more rearward CG. Poor damping shows as yaw overshoot and a lightly damped oscillation after a step.
- Link: `C_alpha` front/rear, mass, inertia and CG position in a two-degree-of-freedom state-space model give natural frequency and damping ratio.

**Gotchas:** linear model only valid below about 0.4 g (gated: unconfirmed, source is paywalled or blocked); use measured gain at several speeds to verify.

## Verify
- [ ] Measured yaw gain vs speed curve peaks near the predicted V_char.
- [ ] Damping ratio from step test close to the model's value.
