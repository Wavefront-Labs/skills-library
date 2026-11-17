---
id: engineering-technology.aerospace-engineering.spacecraft-systems-design.fmea-for-spacecraft
name: fmea-for-spacecraft
category: engineering-technology
field: aerospace-engineering
product: spacecraft-systems-design
tags: [spacecraft, reliability, fdir, fmea, fmeca, failure-modes, severity-classification, single-point-failure]
level: practitioner
status: draft
description: "Run a spacecraft FMEA or FMECA: item functions, failure modes, effects, severity, detection and compensation, and tie results to redundancy and fault protection design."
sources:
  - "ECSS-Q-ST-30-02C (Failure modes effects and criticality analysis)"
  - "MIL-STD-1629A"
  - "NASA Systems Engineering Handbook (risk and reliability)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Spacecraft FMEA

**Goal:** a systematic list of how each element can fail and what happens next.

## Table columns
Item and function, failure mode, failure cause, local effect, next-higher-level effect, end effect on the mission, detection method, compensating provision (redundancy, fault protection), severity category, probability or likelihood (for criticality analysis), recommended action, and remarks.

## Severity classes
Programme-defined categories: catastrophic (loss of life or vehicle or mission), critical (loss of mission or major degradation), marginal and negligible. ECSS defines severity categories 1 to 4 in its FMECA standard; use the standard your programme invokes.

## Procedure
1. Start from the functional architecture (functional FMEA), then the hardware design (hardware FMEA) as design matures; software and interface FMEAs add coverage.
2. Identify single-point failures with high severity; mitigate by redundancy, design change, or accept with approval (a "critical items list").
3. Check detection: can fault protection detect the failure and recover autonomously within the time to critical effect?
4. Cross-check with fault tree analysis for top-level events.
5. Feed results to test planning and operations procedures.

## Gotchas
- An FMEA done after design freeze changes nothing; start early and iterate.
- Common-cause failures (shared power, shared software) escape independent-failure analysis.

## Verify
- [ ] Every single-point failure with high severity has a documented mitigation or approved waiver.
