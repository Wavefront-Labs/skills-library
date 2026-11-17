---
id: engineering-technology.systems-engineering.verification-validation.verification-cross-reference-matrix
name: verification-cross-reference-matrix
category: engineering-technology
field: systems-engineering
product: verification-validation
tags: [verification-validation, v-and-v, vcrm, verification-cross-reference-matrix, requirements-verification-matrix, verification-matrix, inspection, analysis, demonstration, test, test-readiness-review, trr, qualification, acceptance-testing, verification-closure, nasa-se-handbook, test-plan, validation, compliance-matrix]
level: practitioner
status: docs-checked
description: "Plan and close verification with a verification matrix: analysis, inspection, demonstration or test per requirement, success criteria, qualification vs acceptance, TRR."
sources:
  - "https://www.nasa.gov/wp-content/uploads/2018/09/nasa_systems_engineering_handbook_0.pdf"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Verification cross-reference matrix — prove every requirement, and prove you proved it

**Goal:** assign each "shall" a verification method and success criterion early, then drive the matrix to closure with traceable evidence before acceptance.

## 1. Verification vs. validation (NASA SE Handbook)
- **Verification:** proof of compliance with requirements, that the product can meet each "shall" statement, shown by test, analysis, inspection or demonstration (or a combination). It relates back to the approved requirements set.
- **Validation:** shows the product accomplishes its intended purpose in the intended environment and meets stakeholder expectations. It relates back to the ConOps and can be done in each development phase, not only on end products. Keep asking "are we building the right product?".
- Validation differs from qualification: validation focuses on expected environments and operations; qualification covers worst-case loads and environments.

## 2. The four methods (handbook definitions, paraphrased)
| Method | What it is | Typical evidence |
|---|---|---|
| **Analysis** | Mathematical modelling and analytical techniques predict suitability from calculated data or lower-level verifications; used when a prototype or built product is not available. Includes modelling, simulation and verification by similarity to a heritage product | Analysis report with model description |
| **Inspection** | Visual examination of a realised end product, generally for physical design features or identification; can include inspection of drawings, documents or records | Inspection record |
| **Demonstration** | Showing that use of the end product achieves the specified requirement; a basic confirmation of capability, differing from test by the lack of detailed data gathering; may use mock-ups | Witnessed procedure |
| **Test** | Use of the end product (or breadboard, brassboard, prototype) to obtain detailed data under controlled conditions; the most resource-intensive technique | Procedure, data, report |

Choose the method by engineering judgement as the most effective way to show conformance.

## 3. Matrix columns
The handbook's example requirements verification matrix (Appendix D, Table D-1) has: requirement number, document, paragraph, shall statement, verification success criteria, verification method (analysis, inspection, demonstration, test), facility or lab, phase, acceptance requirement?, preflight acceptance?, performing organisation, results. Only "shall" requirements go in the matrix, each with a unique identifier and its source document. Add procedure and report IDs and an approver column if your programme needs them.
- Write the success criterion so a pass/fail call is possible (the handbook's checklist asks that precise requirements facilitate test success criteria).
- Keep the matrix traceable to the requirements tool (see engineering-technology.systems-engineering.doors.structuring-doors-modules-and-traceability).

## 4. Verification, qualification, acceptance, certification (handbook)
- **Verification** is formal, once per design regardless of the number of flight units.
- **Qualification** is a subset of verification performed at the extremes of the environmental envelope to show the design operates with the expected margins; once per design.
- **Acceptance** is a smaller subset performed on each unit built, with an Acceptance Data Package shipped with the unit; criteria show manufacturing and workmanship conform to the design previously verified or qualified.
- **Certification** is the audit by which the body of evidence goes to the certifying authority.
- A **protoflight unit** is a flight unit used when no qualification unit is built; a limited version of qualification test ranges is applied. Environment test levels and margins come from your programme's standard or contract, not from this skill.

## 5. Test readiness review (TRR)
The handbook defines a TRR as a review that ensures the test article (hardware/software), test facility, support personnel and test procedures are ready for testing and for data acquisition, reduction and control. Define your own entry checklist in the verification plan.

## 6. Closure
The handbook describes the Functional Configuration Audit (verifies via test results that the product has met the functional baseline requirements; precedes the PCA) and the Physical Configuration Audit (verifies that the product corresponds to the build-to baseline documentation). Close a row only when its success criterion is met and the evidence is approved.

## Gotchas
- Analysis relying on an unvalidated model is weak evidence; correlate models with test data.
- Changing a requirement after its test reopens that row.
- Interface requirements need verification on both sides (see engineering-technology.systems-engineering.interface-management.n2-diagrams-and-icd-authoring).
- Verification by similarity needs a documented comparison with the heritage product.

## Verify
- [ ] Every "shall" row has a method, success criterion and source document.
- [ ] Test and demonstration rows point to an approved procedure; analysis rows to a report.
- [ ] A TRR is held before each formal test.
- [ ] Closed rows cite approved evidence; open rows have a plan and date.
- [ ] A separate validation plan covers stakeholder expectations and the ConOps.

## Checked
2026-11-01. Confirmed in the NASA Systems Engineering Handbook (SP-2016-6105 Rev 2): verification versus validation definitions, the four methods and their definitions (including similarity under analysis), the Appendix D verification matrix columns, the verification/qualification/acceptance/certification box, protoflight unit definition, TRR definition, FCA and PCA definitions. Removed (not readable in free sources; ISO/IEC/IEEE 15288, INCOSE handbook and SMC-S-016 are paywalled or unread): the 6 dB and 10 degC qualification deltas, example latency/time figures, the 15288 attributions, the six-point TRR entry list, FRACAS wording and the "cheapest method" advice.
Method: documentation only; no commands were run.
