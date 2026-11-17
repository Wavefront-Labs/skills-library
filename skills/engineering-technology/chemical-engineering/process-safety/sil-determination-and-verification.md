---
id: engineering-technology.chemical-engineering.process-safety.sil-determination-and-verification
name: sil-determination-and-verification
category: engineering-technology
field: chemical-engineering
product: process-safety
tags: [chemical-engineering, process-safety, ps-lopa-and-sil, sil-determination-and-verification, sil, safety-integrity-level, iec-61511, iec-61508, safety-instrumented-function, sif, sis, pfdavg, hardware-fault-tolerance, functional-safety]
level: advanced
status: verified
description: "Determine the required SIL for a safety instrumented function from LOPA or a risk graph and verify it (PFDavg, architecture, proof test) under IEC 61511."
sources:
  - "https://www.iec.ch"
  - "CCPS Guidelines for Hazard Evaluation Procedures, CCPS Layer of Protection Analysis, API Standards 520 521 526 and 2000, IEC 61511, OSHA 29 CFR 1910.119, EU Seveso III Directive 2012/18/EU, Crowl and Louvar Chemical Process Safety, Lees Loss Prevention in the Process Industries"
  - "https://www.aiche.org"
  - "https://www.osha.gov"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SIL determination and verification

**Goal:** a defensible SIL target and a design that demonstrably meets it. Safety instrumented systems must be specified, designed, installed, validated and maintained by competent functional safety engineers under IEC 61511 (process sector, built on IEC 61508) and the applicable local regulations; this skill is an outline, not a substitute.

## Lifecycle view (IEC 61511)
Hazard and risk assessment, allocation of safety functions, safety requirements specification (SRS), design and engineering, verification, installation and commissioning, validation, operation and maintenance, modification, decommissioning; functional safety assessment and management throughout.

## Determine the target SIL
1. From LOPA: required risk reduction factor (RRF) = f_mitigated (without the SIF) / f_tolerable. Convert to a target PFDavg = 1/RRF.
2. SIL bands for **low demand mode** (average probability of failure on demand): SIL 1: 1e-2 to below 1e-1; SIL 2: 1e-3 to below 1e-2; SIL 3: 1e-4 to below 1e-3; SIL 4: 1e-5 to below 1e-4 (SIL 4 is rare in the process industry; band edges from the IEC 61508/61511 low-demand table, (gated: unconfirmed, source is paywalled or blocked)). Other methods: risk graph, calibrated matrix.

## Verification elements
1. **PFDavg**: for a 1oo1 channel with dangerous undetected failure rate lambda_DU and proof test interval TI, PFDavg is approximately lambda_DU x TI/2; for 1oo2 about (lambda_DU TI)^2/3 (simplified, ignoring diagnostics) plus common cause (beta) contribution. Sum sensor, logic solver and final element subsystems.
2. **Proof test coverage and interval**: imperfect tests leave a fraction of failures undetected until a later full test, increasing PFDavg.
3. **Architectural constraints**: hardware fault tolerance and safe failure fraction (or the "route 2H" option) limit the SIL claimed for each subsystem.
4. **Systematic capability** of devices (certified or proven in use per the standard).
5. **Spurious trip rate** as a plant availability check.
6. Response time within the process safety time.

## Worked check
Single transmitter-logic-valve with total lambda_DU = 0.02 per year and a one-year test interval: PFDavg about 0.02 x 1/2 = 0.01, at the boundary of SIL 1 and SIL 2; to claim SIL 2 with margin reduce the proof test interval, add redundancy or select devices with lower lambda_DU.

## Gotchas
- Failure rate data must come from certified data sheets or reliable sources and be applied under stated conditions.
- Bypass, maintenance override and operating procedures have to be managed.

## Verify
- [ ] SRS lists function, SIL, process safety time, trip and reset logic, failsafe state.
- [ ] Verification calculation with data sources reviewed by a competent person.
