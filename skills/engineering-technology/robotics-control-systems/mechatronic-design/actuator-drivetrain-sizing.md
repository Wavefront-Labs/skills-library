---
id: engineering-technology.robotics-control-systems.mechatronic-design.actuator-drivetrain-sizing
name: actuator-drivetrain-sizing
category: engineering-technology
field: robotics-control-systems
product: mechatronic-design
tags: [mechatronic-design, actuator-sizing, motor-sizing, servo-motor, bldc, stepper, gearbox, gear-ratio, harmonic-drive, planetary-gearbox, belt-drive, ball-screw, drivetrain, reflected-inertia, inertia-ratio, inertia-matching, rms-torque, peak-torque, speed-torque-curve, torque-constant, back-emf, motion-profile, trapezoidal-profile, thermal-derating, duty-cycle, encoder-resolution, robot-joint, motor-selection]
level: practitioner
status: draft
description: "Size a motor, gearbox and drive for a robot axis: load inertia and torque profile, RMS vs peak torque, gear ratio for inertia match, speed-torque and thermal checks."
sources:
  - "Hughes and Drury, Electric Motors and Drives (5th ed.)"
  - "Lynch and Park, Modern Robotics, ch. 8 (actuation and gearing)"
  - "Manufacturer servo sizing application notes (e.g. Maxon, Kollmorgen, Harmonic Drive catalogues)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Actuator and drivetrain sizing for a robot axis

**Goal:** pick a motor, transmission and drive that deliver the required motion profile
with margin on peak torque, continuous (RMS) torque, speed, voltage and temperature, and
with a load-to-motor inertia ratio the controller can handle.

## 1. Define the motion and the load
Write down for the worst-case move: displacement, move time, dwell, payload and the
pose with the largest gravity torque. Use a **1/3-1/3-1/3 trapezoidal profile**
(accelerate, cruise, decelerate equal thirds): its RMS torque is only ~6% above the minimum-RMS
profile and easy to compute:
`v_max = 1.5·θ/t_move`, `α = v_max/(t_move/3) = 4.5·θ/t_move²`.

Load at the joint (output side):
- inertia `J_L` about the joint axis (rod about its end `mL²/3`, point mass `mr²`);
- gravity `T_g = Σ m_i·g·r_i` at the worst pose;
- friction and process forces (seals, cable drag, tool forces) — measure or estimate 5-15%.

## 2. Torque profile at the joint, then at the motor
Joint torque per segment: `T_j = J_L·α + T_g + T_f`. Through a gear ratio `N` and
efficiency `η`:
`T_m = (J_m + J_gear_in)·N·α + T_j/(N·η)` (motoring segments; when the load
back-drives, efficiency acts the other way and the motor sees roughly `T_j·η/N`).
Reflected load inertia is `J_L/N²`; speed at the motor is `N·ω_j`.

**Worked example.** Shoulder-type joint: 2 kg link of 0.6 m (`J = 2·0.36/3 = 0.24`),
1 kg payload at 0.5 m (`0.25`) → `J_L ≈ 0.49 kg·m²`; `T_g = 2·9.81·0.3 + 1·9.81·0.5 ≈ 10.8 N·m`.
Move 90° (1.571 rad) in 0.5 s, then dwell 0.5 s:
`v_max ≈ 4.71 rad/s`, `α ≈ 28.3 rad/s²`, accel torque `0.49·28.3 ≈ 13.9 N·m`.
Joint torques (gravity worst-case throughout): accel 24.7, cruise 10.8, decel -3.1, dwell 10.8 N·m.
Harmonic drive `N = 100`, `η ≈ 0.7`; motor rotor plus wave generator `J ≈ 3e-5 kg·m²`:
- motor peak ≈ `3e-5·100·28.3 + 24.7/70 ≈ 0.085 + 0.353 ≈ 0.44 N·m`;
- motor speed `4.71·100 ≈ 471 rad/s ≈ 4500 rpm`;
- joint RMS over the 1 s cycle `= sqrt((24.7² + 10.8² + 3.1²)·0.167 + 10.8²·0.5) ≈ 13.5 N·m`,
  so motor RMS ≈ `13.5/70 ≈ 0.19 N·m` plus the rotor-inertia share.
Select a motor with continuous torque ≥ ~0.25 N·m and peak ≥ ~0.6 N·m at 4500 rpm,
or add a brake so the dwell isn't held by motor current (drops RMS sharply).

## 3. Choose the ratio
- **Inertia match** `N_opt = sqrt(J_L/J_m)` minimises motor torque for pure inertial
  acceleration (here `sqrt(0.49/3e-5) ≈ 128`). In practice, choose `N` in the range
  that keeps motor speed under its rated speed while torque is minimised; gravity-dominated
  joints favour higher `N`.
- **Inertia ratio** `J_L/(N²·J_m)`: below ~5:1 for crisp servo performance, up to
  10:1 workable, above 20-30:1 expect resonance and tuning trouble, especially with
  compliant transmissions (belts, long shafts). Here `0.49/(1e4·3e-5) ≈ 1.6`.
- Transmission traits: harmonic drives (ratio 50-160, zero backlash, η 0.6-0.8, flexible);
  planetary (3-100, some arc-minutes backlash, η 0.9-0.97 per stage); belts (low ratio,
  compliant); ball screws for linear (`F = 2π·η·T/lead`). High `N` reduces backdrivability
  and amplifies rotor inertia by `N²`, which matters for collision safety.

## 4. Check the motor against its curves
1. Every (speed, torque) point of the profile lies inside the intermittent region of
   the speed-torque curve; RMS torque at RMS speed sits inside the continuous region.
2. **Voltage:** `V_bus ≥ Ke·ω_max + I_peak·R + drive drop`, with `I = T/Kt`. Back-EMF
   at top speed is the usual reason a "big enough" motor cannot reach speed. Keep ~20% headroom.
3. **Thermal:** continuous ratings assume a stated ambient (often 25 °C) and a mounting
   heatsink; derate for 40 °C+ ambient or enclosed joints (10-30%). Copper resistance
   rises ~0.39%/K, so hot `Kt` drops slightly and `R` rises.
4. **Gearbox:** check its rated and peak (start-stop and emergency-stop) torque and
   max input speed separately; e-stop torques can exceed normal peaks by 2×.
5. **Drive:** continuous and peak current, bus voltage, regen handling (brake resistor
   if the decelerating load returns energy).

## 5. Sensing that matches the drivetrain
Output resolution = `2π/(counts_per_rev·N)` for a motor-side encoder; a 4096-count (12-bit)
encoder through 100:1 gives ~15 µrad at the joint, but backlash and harmonic-drive
flex are not seen — add an output-side encoder when absolute accuracy matters.
Mechanical resonances should be ≥ 3-5× the intended position-loop bandwidth.

Margins I'd treat as minimum: 1.5× on peak torque, 1.3× on RMS torque, 20% on speed and
voltage. Catalogue numbers vary in definition between vendors; read the footnotes.

## Verify
- [ ] Worst-case pose, payload and move are written down and justify every number.
- [ ] Peak and RMS motor torque include rotor/gear inertia and efficiency direction.
- [ ] All profile points sit inside the speed-torque envelope at the actual bus voltage.
- [ ] Inertia ratio and transmission stiffness support the target servo bandwidth.
- [ ] Gearbox, drive and brake are each checked separately, including e-stop loads.
- [ ] Thermal rating derated for real ambient and mounting.
