---
id: engineering-technology.automotive-vehicle-engineering.chassis-suspension-design.kinematics-and-compliance-rig-testing
name: kinematics-and-compliance-rig-testing
category: engineering-technology
field: automotive-vehicle-engineering
product: chassis-suspension-design
tags: [kc-rig, kc-testing, k-and-c-rig, suspension-kinematics-test, compliance-testing, bump-steer-measurement, suspension-characterisation, roll-steer, model-correlation, kinematics-compliance]
level: practitioner
status: draft
description: "Run kinematics and compliance (K and C) rig tests: set-up, kinematic sweeps, compliance load cases, outputs to report, and use for multibody model correlation."
sources:
  - "Reimpell, Stoll and Betzler, The Automotive Chassis (chapter list)"
  - "Milliken and Milliken, Race Car Vehicle Dynamics (chapter list)"
  - "SAE vehicle dynamics test practice for suspension characterisation (confirm standard and rig vendor procedures)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Kinematics and compliance (K and C) rig testing

## 1. Purpose
A K and C rig measures the suspension and steering system characteristics on the complete vehicle (or axle): how toe, camber and track change with wheel travel, roll and steer (kinematics), and how wheels move under forces and moments at the tyre contact patch (compliance). Results define suspension targets, verify prototype build against design, and correlate multibody models.

## 2. Set-up
Vehicle at design ride height with specified load and fluids; tyres inflated per spec; vehicle body clamped (or constrained) at the sills and subframes; wheels on moving pads that can displace vertically, lateral, longitudinal and rotate, with force and moment sensing; steering robot or rack actuator for steer tests; instruments for wheel angles, positions and spring/damper deflections. Condition the suspension by cycling before measuring to remove friction history and use consistent hysteresis handling.

## 3. Test sequences
Kinematic:
- **Parallel wheel travel** (bump and rebound): toe, camber, track change, wheelbase change, caster, and anti-dive geometry (see suspension kinematics).
- **Opposite wheel travel** (roll): roll steer, roll camber, roll centre location.
- **Steer sweeps:** steering ratio, Ackermann, caster and kingpin angle change, scrub (see Ackermann geometry).
Compliance:
- **Lateral force** at the contact patch (both wheels same direction or opposite): lateral force steer, camber compliance, lateral stiffness.
- **Longitudinal force** (drive, brake): braking and drive force steer and anti-dive compliance.
- **Aligning torque:** aligning torque steer.
Use quasi-static loading with specified force range and repeat directions to capture friction.

## 4. Outputs
Slopes and values at design position: bump steer (deg/m of travel or per 25 mm), roll steer, compliance steer (deg per kN), camber compliance (deg per kN), vertical wheel rate, roll stiffness and effective stiffness with and without anti-roll bar. Plot curves with hysteresis and report at the vehicle's design load.

## 5. Use
- Compare with design intent and Adams/CarSim kinematic predictions to find bushing rates or hardpoint errors (see bushing rate selection).
- Parameterise multibody models with measured compliance.
- Check build variation between prototypes.
- Link to subjective feel with correlation studies.

## Verify
- [ ] Vehicle at specified ride height, load and tyre pressure; preconditioned before measurement.
- [ ] Both kinematic and compliance sweeps run, with hysteresis reported.
- [ ] Results compared with model predictions; differences explained.
- [ ] Rig and sensor calibration records referenced.
