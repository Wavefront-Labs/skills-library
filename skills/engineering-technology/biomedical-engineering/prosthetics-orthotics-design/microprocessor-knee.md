---
id: engineering-technology.biomedical-engineering.prosthetics-orthotics-design.microprocessor-knee
name: microprocessor-knee
category: engineering-technology
field: biomedical-engineering
product: prosthetics-orthotics-design
tags: [microprocessor-knee, prosthetic-knees, knee-mechanisms, mpk, stance-control, swing-phase, stumble-recovery, sensor-fusion]
level: advanced
status: draft
description: "Understand microprocessor-controlled prosthetic knees: sensors, stance and swing control, stumble recovery, selection criteria and engineering validation concerns."
sources: ["Peer-reviewed comparisons of microprocessor and non-microprocessor prosthetic knees in the Journal of Rehabilitation Research and Development and Archives of Physical Medicine and Rehabilitation (search and confirm current evidence)", "Manufacturer clinician guides for current units"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Microprocessor-controlled prosthetic knees

**Goal:** know how MPKs sense gait and change resistance, to evaluate designs, compare units and plan testing.

Fitting and programming are done by trained prosthetists following manufacturer instructions; coverage and prescription rules vary by country and payer.

## Architecture
- **Sensors:** knee angle, knee moment or axial load (strain gauge in pylon or knee), accelerometer or IMU, sometimes ankle moment. Sensor sampling is typically hundreds of Hz.
- **Actuation:** variable resistance, not power: hydraulic or pneumatic valves, magnetorheological fluid, or a clutch-brake changes damping electronically; a few designs add motors (powered knee).
- **Controller:** finite-state machine per gait phase (stance, pre-swing, swing, extension) detecting events from load and angle.

## Functions
- **Stance:** high resistance (often with yielding stance flexion for stairs and ramps) to prevent buckling.
- **Swing:** resistance changes with walking speed (cadence-adaptive), so one knee works across slow and fast gait.
- **Stumble recovery:** stance control engages if a trip is detected mid-swing.
- **Modes:** standing, sit, cycling, stair, locking; set by user action or gesture.
- **Battery:** days to a couple of days on a charge in typical designs; plan for charge discipline.

## Selection and evidence
Published studies show improved safety and stability for some users, especially with variable cadence and uneven terrain; effect depends on baseline function, so selection uses functional level and goals. Water exposure, weight limits and cost are practical constraints.

## Engineering test points
- Sensor calibration drift; event detection on stairs and ramps; behaviour on low battery (must fail to a safe stance resistance); electromagnetic immunity; IP rating; fatigue of pylon and attachments.

## Verify
- [ ] Failsafe state defined and tested.
- [ ] Gait-phase detection across speeds and terrain.
- [ ] Prosthetist configuration and user trial documented.
