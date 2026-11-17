---
id: engineering-technology.aerospace-engineering.spacecraft-systems-design.spacecraft-fault-protection
name: spacecraft-fault-protection
category: engineering-technology
field: aerospace-engineering
product: spacecraft-systems-design
tags: [fault-protection, fdir, safe-mode, autonomy, fault-detection, watchdog, reliability-fdir]
level: practitioner
status: draft
description: "Design spacecraft fault protection (FDIR): detection, isolation, recovery and safe mode, with time-to-criticality, false-alarm control and fault-injection testing."
sources:
  - "NASA Systems Engineering Handbook"
  - "Fortescue et al., Spacecraft Systems Engineering"
  - "Wertz and Larson, Space Mission Analysis and Design"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Fault protection

**Goal:** the spacecraft survives anomalies without waiting for ground action, and never makes them worse.

## Layers
- Unit-level protection (hardware over-current, thermostats, watchdog timers).
- Subsystem-level monitors (limit checks, rate checks, consistency checks between redundant sensors).
- System-level safe mode: stable attitude (often sun-pointing and slowly spinning or power-positive), minimum loads, receiver on, simple telemetry.
- Ground intervention.

## Design steps
1. From FMEA and hazard analysis list failures to cover and their time to criticality (how quickly damage results). Failures faster than ground can respond need onboard action.
2. Define the detection (monitor, threshold, persistence count), isolation (which unit or path), and recovery (switch to redundant, reset, safe mode).
3. Choose thresholds above normal variation but below damage; use persistence counters to avoid false alarms from single-event upsets.
4. Keep the safe mode simple, independent of complex software where possible, and test it for entry from every mode and for exit.
5. Cover critical events (launch separation, deployments, orbit insertion) with specific protection.
6. Test by fault injection in the hardware-in-the-loop testbed and flight software; verify no fault response triggers another.
7. Document an operator recovery procedure for each safe mode.

## Gotchas
- Fault protection that triggers wrongly can cause the loss (false positive); balance sensitivity.
- Cascade: a response using a unit already failed. Check dependencies.
- After a reset, state variables may be lost; plan state recovery.

## Verify
- [ ] Every credible failure in the list has an injection test showing the intended response within the required time.
