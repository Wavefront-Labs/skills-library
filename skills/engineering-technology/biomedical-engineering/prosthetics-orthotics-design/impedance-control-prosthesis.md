---
id: engineering-technology.biomedical-engineering.prosthetics-orthotics-design.impedance-control-prosthesis
name: impedance-control-prosthesis
category: engineering-technology
field: biomedical-engineering
product: prosthetics-orthotics-design
tags: [impedance-control, powered-prosthesis, exoskeleton, finite-state-machine, joint-impedance, powered-ankle, stiffness-damping]
level: advanced
status: gated
description: "Implement joint impedance control for powered lower-limb prostheses: torque law, per-gait-phase stiffness, damping and equilibrium angle, tuning and safety limits."
sources: ["Sup, Bohara and Goldfarb, Design and control of a powered transfemoral prosthesis (Int J Robot Res 2008)", "Au, Weber and Herr, Powered ankle-foot prosthesis improves walking metabolic economy (IEEE Trans Robotics 2009)", "Hogan, Impedance control: an approach to manipulation (J Dyn Syst Meas Control 1985)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Impedance control for powered prostheses

**Goal:** make a powered joint behave like a tunable spring and damper that changes by gait phase.

Research and design guidance; any commercial or clinical use needs risk management and regulatory review.

## Control law
Joint torque: tau = K (theta_eq - theta) - B theta_dot, where K is stiffness (Nm/rad), B damping (Nm s/rad), theta_eq the equilibrium angle.
Add a feed-forward push-off torque in late stance where the biological ankle supplies net positive work.

## Finite state machine
1. **Early stance** (heel strike to foot flat): low K and some B to absorb impact; theta_eq slightly plantarflexed.
2. **Mid stance:** higher K as the shank rotates over the foot.
3. **Late stance (push-off):** trigger on shank angle or ankle torque, reduce damping, raise theta_eq plantarflexion to deliver work.
4. **Swing:** dorsiflex to clear the foot; low K.
Transitions use thresholds on load (from a load cell), joint angle and angular velocity, with hysteresis to avoid chatter.

## Tuning
1. Start from able-bodied joint data scaled by body mass (torque-angle curves, stiffness estimated as the slope of the quasi-stiffness curve in each phase).
2. Tune K, B and theta_eq per phase on a treadmill with the clinician and user; adjust by walking speed, with parameter scheduling or velocity-dependent switching.
3. Limit current, torque, velocity and joint range in hardware and software (hard stops and torque limits).

## Gotchas
- Instability from high stiffness with sensor delay; keep the loop rate high (about 1 kHz (gated: unconfirmed, source is paywalled or blocked)) and filter sensors with low latency.
- Misdetected phase transitions cause stumbles; include a safe fallback to a passive-like mode.
- Battery sag changes available torque.

## Verify
- [ ] Phase detection verified across walking speeds and terrain.
- [ ] Torque, speed and angle limits enforced and tested.
- [ ] Failsafe on power loss and on sensor fault.
