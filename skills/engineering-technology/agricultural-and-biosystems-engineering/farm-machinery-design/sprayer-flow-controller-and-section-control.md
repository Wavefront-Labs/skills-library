---
id: engineering-technology.agricultural-and-biosystems-engineering.farm-machinery-design.sprayer-flow-controller-and-section-control
name: sprayer-flow-controller-and-section-control
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: farm-machinery-design
tags: [agricultural-and-biosystems-engineering, farm-machinery-design, spray-rate-controller, sprayer-design, pwm-nozzles, flow-meter-calibration, section-valves, rate-control]
level: practitioner
status: draft
description: "Set up a sprayer rate controller: flow meter and speed calibration, control valve or PWM nozzles, boom section valves and verification of applied rate."
sources:
  - "Srivastava, Goering, Rohrbach & Buckmaster, Engineering Principles of Agricultural Machines (ASABE)"
  - "ASABE Standards, Engineering Practices and Data (https://www.asabe.org)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Sprayer flow controller and section control

**Goal:** hold the set L/ha as speed changes and as sections switch.

## Components
- Flow meter (turbine or magnetic) with a K factor (pulses per litre), speed source (radar or GNSS) and pressure sensor.
- Control valve (servo) trims bypass flow; PWM (pulse-width modulation) nozzle systems keep pressure steady and vary flow by duty cycle, often at about 10 Hz or higher (manufacturer specific).
- Section valves, each with a boom-section width entered in the controller.

## Calibration
1. **Flow meter K factor**: collect and weigh or measure a known volume from the sprayer into a container and compare with the totalizer; adjust the K factor until within 2 percent.
2. **Speed**: calibrate over a measured distance.
3. **Boom width and section widths**: enter measured values, including nozzle spacing.
4. **Pressure**: check gauge accuracy against a test gauge.
5. **Nozzle flow check** with a calibrated jug on each nozzle; replace nozzles that deviate more than 10 percent from the average.

## Gotchas
- Controller response time: at speed changes the pressure can leave the nozzle range; keep the pressure window in the nozzle chart.
- Do not rely on pressure alone for rate; with worn nozzles the pressure/flow link breaks.
- Foam and air in lines lead to flow-meter errors.

## Verify
- [ ] Tank volume used on a measured area matches the controller's recorded volume.
- [ ] No section overlap or skips on headlands in field check.
