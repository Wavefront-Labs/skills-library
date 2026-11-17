---
id: engineering-technology.automotive-vehicle-engineering.powertrain-design.creep-and-launch-torque-calibration
name: creep-and-launch-torque-calibration
category: engineering-technology
field: automotive-vehicle-engineering
product: powertrain-design
tags: [creep-torque, creep, launch, hill-hold, driveability, torque-converter, automatic-transmission, ev-creep, standstill]
level: practitioner
status: draft
description: "Calibrate creep torque and the launch ramp so the vehicle moves off smoothly, holds on grades, and does not overheat the clutch, converter or motor."
sources:
  - "Guzzella and Sciarretta, Vehicle Propulsion Systems (chapter list)"
  - "Happian-Smith, Introduction to Modern Vehicle Design (chapter list)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Creep and launch torque calibration

## 1. What creep is
With the pedal released the vehicle moves slowly (walking pace) for parking and traffic. Automatic transmissions with torque converters produce creep naturally from idle; DCT/AMT and EVs must command it deliberately. Some EV programmes offer a selectable no-creep mode; check the target market's expectations.

## 2. Set the creep curve
Creep torque as a function of speed: highest at zero speed, fading to zero at a cap speed (a few km/h; the exact value is a programme choice). Add dependences on:
- **Gradient** (from accelerometer or brake pressure model): raise torque uphill to avoid roll-back, reduce downhill.
- **Brake pressure:** release creep when the brake is applied firmly, to save energy and avoid fighting the brakes.
- **Gear/drive mode** and battery limits.
Implement as a 2-D table (speed x grade) with smooth interpolation.

## 3. Launch ramp
From standstill with pedal applied: demand rises with the pedal map, but the **clutch or motor torque ramp** must be shaped to avoid a bump when the driveline takes load (see shuffle damping). For wet/dry clutches, command clutch pressure to match target slip and torque; limit slip energy to protect the clutch (see clutch sizing).

## 4. Hill hold and standstill
Hold brake pressure for a short time after brake release, or hold the vehicle with the electric parking brake or motor torque; define the handover to driver torque to avoid roll-back. Hill hold on electrified drive needs thermal limits on motor current at stall.

## 5. Thermal protection
Stall or slow-speed torque causes high clutch slip heat or motor/inverter current at zero speed. Derate creep and launch torque as clutch or inverter temperatures approach limits and warn the driver.

## Verify
- [ ] Creep tested up and down slopes of the specified range, loaded and unloaded.
- [ ] No roll-back during brake-to-pedal transition.
- [ ] Clutch/inverter temperatures within limits during repeated stop-go and a sustained hill hold.
- [ ] Creep disables correctly with brake applied and in park/neutral.
