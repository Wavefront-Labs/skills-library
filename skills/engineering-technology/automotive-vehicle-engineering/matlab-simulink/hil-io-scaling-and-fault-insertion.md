---
id: engineering-technology.automotive-vehicle-engineering.matlab-simulink.hil-io-scaling-and-fault-insertion
name: hil-io-scaling-and-fault-insertion
category: engineering-technology
field: automotive-vehicle-engineering
product: matlab-simulink
tags: [fault-injection, fault-insertion, hil-preparation, hil, io-scaling, fault-insertion-unit, diagnostics-testing, signal-conditioning, dtc-testing]
level: practitioner
status: gated
description: "Scale HIL inputs and outputs to the ECU's real electrical levels and build fault insertion (open, short to ground or battery, signal faults) driven by test cases."
sources:
  - "Simulink Real-Time documentation (https://www.mathworks.com/help/slrealtime/)"
  - "ISO 26262 parts 4 and 6 (verification and fault injection concepts; confirm edition) (https://www.iso.org)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# HIL I/O scaling and fault insertion

**Goal:** the ECU sees realistic voltages, currents and loads, and every diagnostic and safety mechanism can be provoked on demand, repeatably.

## 1. Build the I/O list from the ECU pin-out
For every pin record: type (analogue sensor, ratiometric 5 V, PWM in/out, resolver, CAN, digital in, high-side/low-side drive), range, and the plant signal it maps to. Create one scaling table: engineering unit to volts (or frequency/duty) with gain, offset and saturation limits, kept in a data dictionary, not hard-coded in blocks.

## 2. Scaling rules
- Ratiometric sensors scale with the ECU's reference supply: model the 5 V reference so a supply fault is visible.
- Output loads: provide the real load or a load emulation (injectors, solenoids, motor phase); a missing load triggers open-load diagnostics.
- One unit test per channel: drive a known value, read the ECU's measured value via the calibration tool, confirm within tolerance.
- Never connect high-voltage traction power to a standard HIL rack. Use a low-voltage or purpose-built emulation and follow the rack vendor's safety instructions.

## 3. Fault insertion
Two layers:
1. **Hardware fault insertion (FIU/switch boards):** open circuit, short to ground, short to battery, short between pins, resistive faults. Cross-check against the load and the rack's rated currents so the board is not damaged.
2. **Model-level faults:** sensor stuck, offset, noise, plausibility breaks, delayed CAN frames, signal dropouts, wrong checksum or counter. Implement as multiplexed switches on the plant-to-I/O path controlled by a fault variable.

## 4. Drive faults from tests
Derive the fault list from the FMEA, the diagnostics requirements and the safety concept (ISO 26262 safety mechanisms). Each test case: pre-condition, fault, duration, expected DTC, expected degraded behaviour, fault-reaction time. Automate with a script or Simulink Test sequence; log reaction time against the fault tolerant time interval (FTTI, an ISO 26262 term; definition and edition (gated: unconfirmed, source is paywalled or blocked)).

## Verify
- [ ] Every ECU pin has a row in the I/O scaling table with units and limits.
- [ ] Each channel has a recorded calibration-tool readback check.
- [ ] Each safety mechanism and DTC has at least one fault-insertion case with expected reaction.
- [ ] FIU current ratings checked against the ECU load.
- [ ] Fault tests are scripted and repeatable, not manual.
