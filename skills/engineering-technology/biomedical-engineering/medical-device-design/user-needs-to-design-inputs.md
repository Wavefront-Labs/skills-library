---
id: engineering-technology.biomedical-engineering.medical-device-design.user-needs-to-design-inputs
name: user-needs-to-design-inputs
category: engineering-technology
field: biomedical-engineering
product: medical-device-design
tags: [user-needs-translation, design-inputs, traceability, qfd, requirements]
level: practitioner
status: gated
description: "Translate user needs into measurable, verifiable design inputs with traceability, and decide which needs become inputs and which stay validation targets."
sources: ["ISO 13485:2016 Medical devices - Quality management systems (clause 7.3, design and development inputs)", "FDA Quality Management System Regulation, 21 CFR Part 820, which incorporates ISO 13485:2016 by reference (eCFR 820.7); 820.10(c) points to ISO 13485 clause 7.3 for design and development, https://www.ecfr.gov/current/title-21/part-820", "https://www.iso.org"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Translating user needs into design inputs

**Goal:** every user need maps to one or more inputs that a test can pass or fail, with a record of why.

## Method
1. Number each user need. Classify: performance, safety, usability, regulatory, environmental, interface, serviceability.
2. For each, ask how the team would know the device meets it. Write inputs as shall-statements with a measurable quantity, condition and limit (see writing-verifiable-requirements).
3. Needs that cannot be verified on the bench (for example surgeon confidence) stay as validation criteria; trace them to a validation activity, not to a bench input.
4. Add inputs not stated by users: applicable standards, risk control measures from the ISO 14971 file, manufacturing and sterilisation constraints.
5. A requirements matrix links need to input to verification to validation. A house-of-quality (QFD) grid helps rank competing inputs.
6. Resolve conflicts (for example smaller diameter versus higher push force) explicitly and record the decision.

## Traps
- One input per need forced; many needs need several inputs, and some inputs satisfy several needs.
- Inputs that restate the design solution (use 316L) instead of the requirement.
- Missing the review step: design inputs must be reviewed for adequacy and approved before outputs are frozen (ISO 13485 7.3 sub-clause detail (gated: unconfirmed, source is paywalled or blocked)).

## Verify
- [ ] No orphan needs or inputs in the trace matrix.
- [ ] Every input is testable with a named method.
- [ ] Conflicts and exclusions have a recorded rationale.

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.
