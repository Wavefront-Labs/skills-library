---
id: engineering-technology.biomedical-engineering.device-verification-validation.software-risk-control
name: software-risk-control
category: engineering-technology
field: biomedical-engineering
product: device-verification-validation
tags: [software-risk-control, software-verification, iec-62304-testing, iec-62304, software-risk-management, watchdog, plausibility-check, segregation]
level: advanced
status: gated
description: "Implement and verify software risk controls under IEC 62304 clause 7: identify hazard-contributing software, define controls, segregate items and verify each measure."
sources: ["IEC 62304 Medical device software - Software life cycle processes (clause 7 software risk management; confirm edition)", "ISO 14971 Application of risk management to medical devices", "AAMI TIR32 Medical device software risk management (confirm current status)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Software risk controls

**Goal:** show that software that can contribute to a hazardous situation is controlled, and that every software control is verified.

Practice guidance; clause structure follows IEC 62304 (confirm edition and any regional amendments).

## Workflow (IEC 62304 clause 7 outline)
1. **Identify software items that could contribute to hazardous situations** from the ISO 14971 analysis, including failure of SOUP and sequences of events (wrong data displayed, wrong calculation, stuck output, lost alarm).
2. **Identify causes** at the software level: defects, unexpected inputs, timing, memory, data corruption, interface failure.
3. **Define risk control measures:**
   - Prefer controls outside the software (hardware interlock, independent monitor, mechanical limit).
   - Inside software: input validation and range checks, plausibility checks between redundant sensors, watchdog timers and heartbeat, CRC on stored and communicated data, safe-state transitions, defensive defaults, version and compatibility checks, alarm on failure to compute.
   - Architectural: segregate high-risk functions from other code (separate process, memory protection, or processor), reducing the scope of class C items.
4. **Implement** the controls as software requirements with traceability to the hazard.
5. **Verify** each control: unit and integration tests, fault injection (corrupt inputs, force sensor dropout, pull power during write), static analysis and code review for critical items, timing tests under load.
6. **Evaluate new hazards** introduced by the controls (for example a watchdog reset during therapy delivery).
7. **Manage changes:** analyse the impact of every software change on risk controls and re-verify affected controls (clause 7.4 (gated: unconfirmed, source is paywalled or blocked)).

## Gotchas
- Relying on "we will test it well" as the only risk control.
- Fault handling that continues therapy after a failed self-test.
- Untested recovery after reset or power loss.

## Verify
- [ ] Traceability from each hazard cause to a control, requirement and test result.
- [ ] Fault-injection tests recorded and passed.
- [ ] Residual risk after controls recorded in the risk file.
