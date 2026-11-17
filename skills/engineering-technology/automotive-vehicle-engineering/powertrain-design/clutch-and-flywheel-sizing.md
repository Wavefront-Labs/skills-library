---
id: engineering-technology.automotive-vehicle-engineering.powertrain-design.clutch-and-flywheel-sizing
name: clutch-and-flywheel-sizing
category: engineering-technology
field: automotive-vehicle-engineering
product: powertrain-design
tags: [clutch-sizing, clutch, flywheel, dual-mass-flywheel, clutch-torque-capacity, launch-energy, driveline-components, friction-clutch, slip-energy]
level: practitioner
status: gated
description: "Size a friction clutch from torque capacity, mean radius and launch slip energy, and choose flywheel inertia and DMF for smoothness and heat."
sources:
  - "Heywood, Internal Combustion Engine Fundamentals (chapter list)"
  - "Happian-Smith, Introduction to Modern Vehicle Design (chapter list)"
  - "Guzzella and Sciarretta, Vehicle Propulsion Systems (chapter list)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Clutch and flywheel sizing

## 1. Torque capacity
T_capacity = mu x F_clamp x R_mean x N, where N = number of friction surfaces (2 for a single dry disc) and R_mean is the effective friction radius.
- Uniform wear (typical design assumption): R_mean = (R_o + R_i) / 2.
- Uniform pressure (new clutch): R_mean = (2/3)(R_o^3 - R_i^3)/(R_o^2 - R_i^2).
Take mu from the friction material supplier and F_clamp at end-of-life pressure-plate load, after wear and diaphragm spring relaxation.

## 2. Capacity margin
Require T_capacity above peak engine torque by a margin set by your standard (the supplier and company standard give the factor), plus allowance for torque overshoot and turbo or electric assist.

## 3. Launch slip energy
Simplified start from standstill with engine speed held at omega_e, constant clutch torque T_c, load torque T_l at the clutch, and vehicle inertia reflected to the clutch J_v:
E = 0.5 x J_v x omega_e^2 x T_c / (T_c - T_l) (integrated numerically for J_v = 2 kg m2, omega_e = 200 rad/s, T_c = 150 N m, T_l = 30 N m: 50,000 J both ways).
This is an approximation (engine speed is not constant, T_l varies with speed). Use it for first sizing and then simulate. Compare E and average power E/t_launch with supplier limits for the facing area (specific energy per area) in worst cases: loaded, towing, hill start, repeated starts.

## 4. Flywheel and DMF
- Flywheel inertia sets engine speed fluctuation at idle and low rpm; too little causes rough idle or stall, too much slows engine response and adds mass.
- A **dual-mass flywheel** places a torsional spring and damper between engine and gearbox; it moves the driveline resonance below idle and cuts transmitted torsional vibration (gated: unconfirmed, source is paywalled or blocked), but adds cost and wear. Choose spring rate and friction with the engine order excitation (see firing-order excitation).
- Thermal: flywheel mass absorbs launch heat; check peak surface temperatures to avoid hot spotting.

## 5. Other checks
Facing burst speed, release bearing travel, pedal effort and pedal ratio, clutch drag and judder (friction coefficient vs slip speed curve).

## Verify
- [ ] Torque capacity computed at worn condition and compared with the margin target.
- [ ] Launch energy cases (loaded hill, trailer) within supplier specific-energy limits.
- [ ] DMF resonance and engine order excitation checked.
- [ ] Judder and drag tests planned.
