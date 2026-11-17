---
id: engineering-technology.automotive-vehicle-engineering.chassis-suspension-design.subframe-mount-design
name: subframe-mount-design
category: engineering-technology
field: automotive-vehicle-engineering
product: chassis-suspension-design
tags: [subframe-mount, subframe, cradle, subframe-bushing, mount-stiffness, torque-roll-axis, ride-and-handling, nvh-isolation, subframe-crash-release, chassis-mount]
level: practitioner
status: gated
description: "Design subframe mounts: bush rates and layout for NVH versus handling, decoupling vibration modes, bolt joint preload, and crash release and durability checks."
sources:
  - "Reimpell, Stoll and Betzler, The Automotive Chassis (chapter list)"
  - "Happian-Smith, Introduction to Modern Vehicle Design (chapter list)"
  - "Harrison, Vehicle Refinement (chapter list)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Subframe mount design

## 1. Purpose
A subframe (cradle) carries the suspension arms and sometimes the steering rack, engine or e-drive, and is attached to the body through (usually four) mounts. The mounts isolate road and powertrain noise from the body and control subframe motion for handling.

## 2. Mount layout and rates
- **Positions:** place mounts at stiff body nodes (see body joint stiffness); a wide stance gives better roll and yaw control of the subframe.
- **Rates:** rubber or hydro-bushings with separate axial and radial rates (vertical, lateral, longitudinal at each mount). Soft mounts improve road and engine isolation; stiff mounts improve steering response, camber and toe control (compliance steer) and reduce on-centre lag.
- **Dynamic stiffness:** the stiffness at the frequency of the noise (typically 100-400 Hz for road booming (gated: unconfirmed, source is paywalled or blocked)) is higher than static; check the ratio dynamic to static for the compound, and use hydro mounts or decoupler designs where needed.
- **Compliance in handling:** subframe motion changes toe/camber; keep lateral compliance low or arrange it for compliance understeer (see compliance steer).

## 3. NVH
- Separate subframe modes from engine and road excitation orders; target first subframe bending/torsion modes above the main excitation range or well damped.
- Subframe mass and local stiffness at mounts affects transfer to body (see structure-borne road noise and transfer path analysis).
- Tuned absorbers on the subframe for narrowband problems.

## 4. Bolted joint
Preload in the mounting bolt creates the clamp load: calculate with torque-angle or yield-controlled tightening; check clamp load vs worst-case lateral and braking loads (no slip) and fatigue of the bolt thread. Use sleeves in rubber mounts to avoid crushing rubber; plan service replacement.

## 5. Crash behaviour
Subframe can stiffen the front structure or intrude: designs control the load path with collapsing, bolt shear or release features so the subframe detaches in a controlled way at a defined load (see powertrain intrusion control and crash rail design). Verify by crash CAE and test.

## 6. Durability
Rubber ageing, oil and ozone exposure; mount fatigue at high strain; verify with component rig tests and the vehicle durability schedule.

## Verify
- [ ] Mount rates (static and dynamic) specified in three directions.
- [ ] Handling and NVH both checked on the same iteration.
- [ ] Bolt preload and slip margin calculated.
- [ ] Crash release behaviour confirmed by CAE and test.
