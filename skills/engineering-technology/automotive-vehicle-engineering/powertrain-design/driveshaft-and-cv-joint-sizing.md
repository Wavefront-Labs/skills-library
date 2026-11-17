---
id: engineering-technology.automotive-vehicle-engineering.powertrain-design.driveshaft-and-cv-joint-sizing
name: driveshaft-and-cv-joint-sizing
category: engineering-technology
field: automotive-vehicle-engineering
product: powertrain-design
tags: [cv-joint, driveshaft, half-shaft, constant-velocity-joint, driveline-components, torque-capacity, joint-angle, plunge, torsional-strength]
level: practitioner
status: gated
description: "Size half-shafts and CV joints from peak wheel torque, shock factors and joint working angles; check torsional strength, fatigue, plunge and NVH."
sources:
  - "Happian-Smith, Introduction to Modern Vehicle Design (chapter list)"
  - "Reimpell, Stoll and Betzler, The Automotive Chassis (chapter list)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Driveshaft and CV joint sizing

## 1. Load cases
- **Peak drive torque at the wheel:** T_w = T_engine_peak x ratio_1st x final_drive x efficiency, then per side after the differential split. Also check the **traction-limited** torque: T = mu x F_z x r_tyre; the lower governs.
- **Shock loads:** clutch drops, tip-in, curb strikes, ABS cycling. Apply a shock factor from your OEM or supplier standard (do not invent one); many teams validate by rig tests.
- **Fatigue spectrum:** torque and joint angle histogram over the durability cycle.
- **Electric drives:** instantaneous motor torque is fast and often higher at the wheel than ICE; include motor peak and regen torque.

## 2. Shaft sizing
Solid bar torsional shear: tau = 16 T / (pi d^3) (2000 N m on a 30 mm bar gives 377 MPa, computed). Compare with yield or fatigue strength of the heat-treated steel (induction-hardened carbon or alloy steel is common) with a safety factor. Hollow shaft: tau = 16 T D / (pi (D^4 - d^4)) (equals T r / J with J = pi (D^4 - d^4)/32: both 170 MPa for D = 40 mm, d = 20 mm, 2000 N m). Include spline root diameter and stress concentration at splines and grooves, which usually govern.

## 3. Joint selection and angles
- **Fixed (outboard) joints:** Rzeppa-type ball joints handle large steering angles (gated: unconfirmed, source is paywalled or blocked); angle capability is catalogue-specific, so use supplier data.
- **Plunging (inboard) joints:** tripod or cross-groove joints allow axial plunge; working angle is smaller. A large working angle raises heat and shortens life, and tripod joints can transmit shudder and induced axial forces that affect NVH (gated: unconfirmed, source is paywalled or blocked).
Use supplier torque and angle capacity curves for life; confirm joint, boot and grease for temperature, and boot packaging at full bump, rebound and steer.

## 4. Package geometry
Check joint angles and plunge at full travel with the suspension kinematics: static, full bump, full rebound, full steer. Make sure plunge stroke does not bottom or pull out; maintain boot clearance; check intermediate shafts and their bearing supports.

## 5. NVH and durability
Check shaft first bending and torsion modes against engine or motor orders; use dampers where needed. Durability: torque-angle cycling rig, boot and grease ageing, corrosion.

## Verify
- [ ] Both peak and traction-limited torque cases checked, with documented shock factor source.
- [ ] Spline and groove stresses checked, not just the shaft barrel.
- [ ] Joint angles and plunge verified at all suspension and steering extremes.
- [ ] Supplier life calculation or rig test on the real duty cycle.
