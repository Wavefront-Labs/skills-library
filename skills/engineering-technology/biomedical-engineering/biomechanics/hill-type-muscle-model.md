---
id: engineering-technology.biomedical-engineering.biomechanics.hill-type-muscle-model
name: hill-type-muscle-model
category: engineering-technology
field: biomedical-engineering
product: biomechanics
tags: [hill-type-muscle, musculoskeletal-modeling, opensim, muscle-model, activation-dynamics, force-length, force-velocity, tendon-slack-length]
level: advanced
status: gated
description: "Build and parameterise a Hill-type muscle-tendon model: activation dynamics, force-length and force-velocity curves, tendon, pennation, and sensitivity to tendon slack length."
sources: ["Zajac, Muscle and tendon: properties models scaling and application to biomechanics and motor control (Crit Rev Biomed Eng 1989)", "Millard et al., Flexing computational muscle: modeling and simulation of musculotendon dynamics (J Biomech Eng 2013)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Hill-type muscle-tendon model

**Goal:** compute muscle force from neural excitation and muscle-tendon length, for use in forward dynamics and static optimisation.

## Components
- **Activation dynamics:** first-order lag from excitation u to activation a with different time constants for activation and deactivation (OpenSim Millard2012EquilibriumMuscle defaults: 10 ms activation and 40 ms deactivation time constants, read from the opensim-core source).
- **Contractile element (CE):** force F_CE = a F_max f_L(l) f_V(v), with force-length f_L (bell-shaped, peak at optimal fibre length l_opt) and force-velocity f_V (Hill hyperbola; force falls with shortening velocity, reaching zero at maximum shortening velocity of the order of 10 l_opt per second for typical fibres, with eccentric force plateau of the order of 1.4 times isometric: OpenSim ForceVelocityCurve default max_eccentric_velocity_force_multiplier = 1.4; the 10 l_opt/s maximum shortening velocity is a textbook figure (gated: unconfirmed, source is paywalled or blocked)).
- **Parallel elastic element (PE):** passive force when stretched beyond l_opt.
- **Tendon:** series elastic element, nonlinear (toe region, then linear), strain at maximum isometric force of order 4-5% (OpenSim TendonForceLengthCurve default strain_at_one_norm_force = 0.049; Zajac-style generic values are lower); **tendon slack length** is the length at which tendon begins to carry force.
- **Pennation angle:** fibre force projects onto the tendon line by cos(alpha); muscle thickness constant makes alpha vary with length.

## Parameters
Peak isometric force F_max (from physiological cross-sectional area times specific tension of roughly 20-30 N/cm2 (gated: unconfirmed, source is paywalled or blocked), or from literature data), l_opt, tendon slack length, pennation. These are uncertain; tendon slack length strongly influences the operating range, and published models differ.

## Workflow
1. Choose a validated model (for example the OpenSim Millard muscles).
2. Scale parameters with limb size (see opensim-model-scaling).
3. Check each muscle's force-length operating range over the joint range of motion.
4. Calibrate tendon slack length so that muscles operate on a reasonable portion of the curve.
5. Run sensitivity analysis of simulated force to parameters.

## Verify
- [ ] Isometric force-joint angle curves are physiologically plausible.
- [ ] Activation dynamics step response matches intended time constants.
- [ ] Muscle forces from simulation checked against EMG timing.
