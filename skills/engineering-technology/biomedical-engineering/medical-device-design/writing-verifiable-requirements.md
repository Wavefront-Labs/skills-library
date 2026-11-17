---
id: engineering-technology.biomedical-engineering.medical-device-design.writing-verifiable-requirements
name: writing-verifiable-requirements
category: engineering-technology
field: biomedical-engineering
product: medical-device-design
tags: [verifiable-requirements, design-inputs, product-requirements, requirements-engineering, shall-statements, requirement-quality]
level: practitioner
status: draft
description: "Write design input requirements that are singular, unambiguous, measurable and verifiable, with units, conditions and a named verification method."
sources: ["INCOSE Guide to Writing Requirements (current edition)", "ISO 13485 Medical devices - Quality management systems (design and development inputs)", "IEEE/ISO/IEC 29148 Requirements engineering"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Writing verifiable requirements

**Goal:** each design input can be tested, and a different engineer would test it the same way.

## Rules
1. **One requirement per statement** ("The device shall ..."); avoid "and" joining two tests.
2. **Measurable:** give a quantity, unit, tolerance and condition. Bad: "The handle shall be comfortable." Better: "The handle shall allow a 5th percentile female hand to reach the trigger with a grip span of 45-60 mm" and test with user data.
3. **Unambiguous:** avoid "fast", "robust", "user-friendly", "etc.", "as appropriate".
4. **Conditions:** state the environment (temperature, humidity, fluid, sterile state), the life stage (new, aged, after sterilisation, after transit) and the user.
5. **Rationale and source:** note the user need, hazard, standard clause or regulation that drives each line.
6. **Verification method** named in the requirement record: test, inspection, analysis, demonstration or review.
7. **Priority and risk link:** mark requirements that are risk controls (they need stronger evidence).
8. **No design solution** in inputs unless a constraint (for example "the device shall use a 10 Fr introducer").
9. **Unique IDs** and version control; changes go through change control (see design-change-control).

## Example
"The infusion set shall deliver 1.0 mL/h +/- 5% (95% confidence, 90% reliability) at 20-25 C after 3 years of accelerated ageing." Verification: bench test per protocol with the stated sample size.

## Gotchas
- Requirements copied from competitor datasheets without clinical reason.
- Missing negative requirements (what the device shall not do, such as leakage, particulates).
- Mixing user needs and design inputs in one table without traceability.

## Verify
- [ ] A reviewer who did not write the requirement can write the test.
- [ ] Every requirement traces to a need or standard and to a verification line.
- [ ] Ambiguous words removed by review.
