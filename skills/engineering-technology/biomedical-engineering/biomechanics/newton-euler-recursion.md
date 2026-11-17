---
id: engineering-technology.biomedical-engineering.biomechanics.newton-euler-recursion
name: newton-euler-recursion
category: engineering-technology
field: biomedical-engineering
product: biomechanics
tags: [newton-euler, inverse-dynamics, joint-moments, free-body-diagram, net-joint-moment, recursion, gait]
level: advanced
status: gated
description: "Compute net joint forces and moments by Newton-Euler recursion from the foot upward, with 2D equations, sign conventions and closure checks."
sources: ["Winter, Biomechanics and Motor Control of Human Movement (inverse dynamics chapters)", "Zatsiorsky, Kinetics of Human Motion", "Vaughan, Davis and O'Connor, Dynamics of Human Gait"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Newton-Euler recursion for inverse dynamics

**Goal:** the net force and moment at each joint from measured motion and ground reaction force.

## Planar equations (segment i, proximal joint P, distal joint D)
Unknown proximal joint force F_P and moment M_P; known distal joint force F_D and moment M_D from the previous segment (equal and opposite).
- Linear: F_P + F_D + m g = m a, with a the COM acceleration; solve F_P = m a - m g - F_D (signs depend on the direction conventions you choose).
- Angular about the COM: M_P + M_D + (r_P x F_P) + (r_D x F_D) = I alpha, with r vectors from the COM to the application points.

## Algorithm for the lower limb
1. Free-body the **foot**: distal force = ground reaction force at the centre of pressure, moment = free moment if available. Solve for the ankle force and moment.
2. Pass the equal-and-opposite ankle loads to the **shank**; solve for the knee loads.
3. Repeat for the **thigh** to get the hip loads.
4. Optionally continue to the pelvis and trunk.

## Data preparation
- Smooth positions before differentiating, with the same cutoff for kinematics and force data (see butterworth-data-filtering).
- Compute COM accelerations from filtered COM positions (or from analytic differentiation of splines).
- Use consistent coordinates: segment COM, joint centres and force-plate data in one global frame.

## Reporting
- Joint moments are net muscle moments only; they do not equal individual muscle forces and hide co-contraction.
- Normalise by body mass (Nm/kg) or by body weight times height.
- Define extension or flexion positive; plot with the sign convention.

## Verification
- [ ] **Closure check:** a top-down recursion from the trunk should return near the measured GRF (residual tests data consistency).
- [ ] Sanity values: ankle plantarflexor moment peak in late stance of about 1.5 Nm/kg in normal walking; knee moments about 0.5 Nm/kg (textbook magnitudes (gated: unconfirmed, source is paywalled or blocked)).
- [ ] Unit and sign checks with a static standing pose (moment equals weight times lever arm).
