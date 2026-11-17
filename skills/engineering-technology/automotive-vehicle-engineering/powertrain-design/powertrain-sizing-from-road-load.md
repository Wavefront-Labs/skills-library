---
id: engineering-technology.automotive-vehicle-engineering.powertrain-design.powertrain-sizing-from-road-load
name: powertrain-sizing-from-road-load
category: engineering-technology
field: automotive-vehicle-engineering
product: powertrain-design
tags: [powertrain, powertrain-sizing, road-load, coastdown, tractive-effort, gradeability, acceleration, top-speed, gear-ratio, final-drive, transmission, e-motor, electric-motor, engine, traction-limit, adhesion, rotational-inertia, efficiency-map, wltp, drive-cycle, hybrid, ev, bev]
level: practitioner
status: gated
description: "Size motor/engine power, torque and gear ratios from road-load coefficients, gradeability, acceleration and top-speed targets, then check drive-cycle energy."
sources:
  - "Gillespie, Fundamentals of Vehicle Dynamics (SAE), chapters on acceleration and road loads"
  - "Ehsani et al., Modern Electric, Hybrid Electric and Fuel Cell Vehicles (CRC)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Powertrain sizing from road load

**Goal:** turn vehicle targets (top speed, 0–100 km/h, gradeability, towing) into a
peak power, peak torque, maximum speed and ratio set for the propulsion machine, before
anyone commits to hardware.

## 1. Write down the road load
```
F_rl(v) = A + B·v + C·v²                        (from coastdown, or:)
F_rl(v) ≈ m·g·Crr + ½·ρ·Cd·Af·v²                 (concept stage)
F_grade = m·g·sin(θ)       F_accel = m·(1+δ)·a
```
Concept values: Crr 0.007–0.010 on low-rolling-resistance tyres (gated: unconfirmed, source is paywalled or blocked), ρ = 1.2 kg/m³,
δ (rotational inertia factor) ~0.05 for a single-speed EV, up to 0.3+ in first gear of
a manual ICE car (gated: unconfirmed, source is paywalled or blocked).

## 2. Top speed sets continuous power at high speed
`P_wheel = F_rl(v_max) · v_max`, then divide by driveline efficiency.

**Example (EV):** m = 1800 kg, Cd = 0.28, Af = 2.3 m², Crr = 0.009, v_max = 180 km/h
(50 m/s). Aero = 0.5·1.2·0.28·2.3·50² = 966 N; rolling = 159 N; total 1125 N.
P_wheel = 56 kW; at 90% motor+inverter+gear efficiency → **~63 kW** must be sustainable
at top speed (check the motor's *continuous* rating there, not its 10-second peak).

## 3. Top speed and max machine speed set the overall ratio
`i_overall ≤ ω_motor,max · r_dyn / v_max`. With 16 000 rpm (1675 rad/s), r_dyn = 0.33 m:
i ≤ 1675·0.33/50 = 11.06. Pick ~10.5 to leave margin for tyre growth and a speed
limiter. For an ICE, the top gear is usually set so v_max falls slightly past peak power
(or on it), and overdrive ratios beyond that are for cruise fuel economy.

## 4. Acceleration sets peak power and torque
For a machine that is torque-limited up to base speed v_b and power-limited above it,
ignoring road load:
```
t(0→v_f) ≈ m_eff · (v_b² + v_f²) / (2 · P)
```
Example: 0–100 km/h (27.8 m/s) in 7.0 s, m_eff = 1.05·1800 = 1890 kg, v_b = 10 m/s:
P ≈ 1890·(100 + 772)/(2·7.0) ≈ 118 kW at the wheels. Add road load and losses →
**~130–140 kW peak**. Low-speed tractive force F = P/v_b ≈ 118 000/10 = 11.8 kN, i.e.
wheel torque ≈ 11.8 kN · 0.33 m ≈ 3.9 kNm, motor torque ≈ 3900 / (10.5·0.97) ≈
**380 Nm**. Note 11.8 kN is ~0.67 g on this car — see step 5 before believing it. Then simulate
properly (the formula is a sizing estimate, not a performance claim).

## 5. Check the traction limit
Maximum tractive force on the driven axle ≈ μ · W_driven,dynamic. Under acceleration,
load moves rearward by m·a·h/L. For FWD, a_max ≈ μ·(b/L) / (1 + μ·h/L) (b = CG to rear
axle); with μ ≈ 1.0, 60% front weight and h/L ≈ 0.2 that is only ~0.5 g. RWD gives
μ·(lf/L)/(1 − μ·h/L) (lf = CG to front axle): 0.5 g with 60% front weight, 0.625 g at 50/50,
0.75 g with 60% rear weight (μ = 1, h/L = 0.2, computed). AWD approaches μ. The 0.67 g example
above therefore needs AWD, or a rear-biased RWD car (about 53% or more rear weight); there is no point sizing first-gear torque beyond what the axle can use. Check
gradeability at the same time: a 30% grade (θ ≈ 16.7°) needs m·g·(Crr·cosθ + sinθ)
≈ 5.2 kN for the example car — usually covered by the acceleration torque, but towing
cases (vehicle + trailer mass) often are not.

## 6. Ratio spacing (multi-speed)
First gear from launch/gradeability torque, top gear from step 3; fill in between with
progressive spacing (steps shrink in higher gears) so that each upshift lands near peak
power. Typical step ratios 1.2–1.5 (gated: unconfirmed, source is paywalled or blocked); wider steps cost acceleration, narrower ones cost
mass and shift count.

## 7. Close the loop on the drive cycle
Run the candidate on WLTC/FTP-75 in a plant model (see
`engineering-technology.automotive-vehicle-engineering.matlab-simulink.drive-cycle-vehicle-plant-model`).
Plot operating points on the efficiency map: most cycle points sit at low torque and
moderate speed, so a machine sized only for performance can waste several percent of
cycle energy at light load. Iterate ratio and machine size against that, not peak
efficiency alone.

## Gotchas
- Peak vs continuous ratings: e-motors and inverters derate thermally within seconds to
  minutes; repeated launches or long grades must use continuous curves.
- Battery power at low SOC and cold temperature often limits acceleration before the
  motor does — check the pack (see the ev-battery-systems skill).
- Use dynamic rolling radius, not unloaded radius.

## Verify
- [ ] Road-load coefficients sourced (coastdown) or concept assumptions stated.
- [ ] Continuous power covers top speed and the worst sustained grade/towing case.
- [ ] Overall ratio respects maximum machine speed with margin.
- [ ] Peak torque does not exceed what the driven axle can transmit.
- [ ] Drive-cycle simulation shows operating points in a sensible region of the
      efficiency map.
