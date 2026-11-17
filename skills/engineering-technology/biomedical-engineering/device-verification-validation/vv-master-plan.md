---
id: engineering-technology.biomedical-engineering.device-verification-validation.vv-master-plan
name: vv-master-plan
category: engineering-technology
field: biomedical-engineering
product: device-verification-validation
tags: [vv-master-plan, verification-planning, vv-planning, test-strategy, design-verification, design-validation, v-model, test-plan]
level: practitioner
status: verified
description: "Write a V and V master plan: scope, strategy by requirement, responsibilities, acceptance rules, sample size rationale and linkage to risk and traceability."
sources: ["https://www.ecfr.gov/current/title-21/chapter-I/subchapter-H/part-820","https://www.iso.org/standard/59752.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# V&V master plan

**Goal:** one document that says how every design input will be verified and how the device will be validated for its intended use, before anyone writes a protocol.

Practice guidance; the design-control rules come from ISO 13485 and your market's regulation. In the US, 21 CFR Part 820 (the Quality Management System Regulation) now requires a QMS complying with ISO 13485 (incorporated by reference in 820.10 and 820.7), and its old design-control section 820.30 is reserved (eCFR checked 2026-10-19). Confirm the current EU MDR text separately.

## Contents
1. **Scope and device description:** intended use, user, environment; configuration under test.
2. **Strategy:** a table mapping each design input to a method (test, inspection, analysis, demonstration, similarity), the protocol or report that will hold the evidence, and the phase (design, pilot, final).
3. **Verification versus validation:** verification shows outputs meet inputs; validation shows the device meets user needs and intended use (clinical or simulated-use evidence, summative usability, software validation).
4. **Risk-based depth:** use the risk file to set the rigor (sample size, confidence, margin) for tests of risk controls; higher severity or lower detectability gets more samples (see confidence-reliability-sampling).
5. **Test method validation:** list methods needing validation before use (see tmv-procedure).
6. **Sample sources:** production-equivalent units from validated processes; label the build configuration; include worst-case tolerances and aged and sterilised units where relevant.
7. **Acceptance and deviations:** pass/fail rules and how deviations and failures are handled (see test-deviation-handling).
8. **Roles and schedule:** owners, labs, calibrated equipment and the sequencing (for example verify the design before validation on final design; design freeze rules).
9. **Traceability:** link to the traceability matrix (see traceability-matrix) and risk controls.
10. **Change handling:** what triggers retest after design changes.

## Gotchas
- Plans that list protocols but no acceptance criteria.
- Using engineering prototypes for validation evidence.
- Forgetting aging, sterilisation, shipping and use-environment conditions.

## Verify
- [ ] Every design input and every risk control has a verification line.
- [ ] Validation covers every user need and intended use claim.
- [ ] Plan approved by design review before testing begins.
