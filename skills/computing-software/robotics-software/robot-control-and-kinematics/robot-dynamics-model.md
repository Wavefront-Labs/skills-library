---
id: computing-software.robotics-software.robot-control-and-kinematics.robot-dynamics-model
name: robot-dynamics-model
category: computing-software
field: robotics-software
product: robot-control-and-kinematics
tags: [robot-dynamics, lagrange, inertia-matrix, coriolis, gravity-compensation, computed-torque, dynamics-control]
level: advanced
status: draft
description: "Use the manipulator dynamic model B(q)qdd + C qd + g = tau for gravity compensation and computed torque."
sources:
  - https://control.ros.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Manipulator dynamics
- Model: `B(q) qdd + C(q,qd) qd + F qd + g(q) = tau`, where B is the symmetric positive-definite inertia matrix, C the Coriolis/centrifugal terms, g gravity.
- Gravity compensation: `tau = g(q)` alone holds the arm still; add PD for a regulated pose: `tau = g(q) + Kp (qd - q) - Kd qdot`.
- Computed torque (inverse-dynamics) control: `tau = B(q)(qdd_d + Kd (qd_d - qd) + Kp (q_d - q)) + C qd + g`, giving linear error dynamics `edd + Kd ed + Kp e = 0` if the model is exact.
- Get B, C, g from URDF with libraries such as Pinocchio (`rnea`, `crba`) or KDL (`ChainDynParam`); check inertial parameters (mass, COM, inertia) because model error dominates performance.
- Geared servos with high reduction hide dynamics; independent joint PID often suffices.

## Gotchas
- URDF inertias are often guesses; a bad g(q) makes the arm drift or slam.
- Friction (Coulomb/viscous) matters at low speed; identify it.

## Self-check
`tau = g(q)` in simulation holds a pose with negligible drift.
