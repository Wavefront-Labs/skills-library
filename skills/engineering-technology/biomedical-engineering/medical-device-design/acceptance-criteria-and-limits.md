---
id: engineering-technology.biomedical-engineering.medical-device-design.acceptance-criteria-and-limits
name: acceptance-criteria-and-limits
category: engineering-technology
field: biomedical-engineering
product: medical-device-design
tags: [acceptance-criteria, performance-specification, design-input-limits, tolerance, pass-fail]
level: practitioner
status: draft
description: "Define performance specifications and pass-fail acceptance criteria with limits, tolerances and statistical confidence, justified by risk and clinical need before tests run."
sources: ["ISO 14971 Medical devices - Application of risk management to medical devices", "ISO 13485 design verification and validation clauses (confirm edition)", "https://www.iso.org"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Performance specifications and acceptance criteria

**Goal:** a spec limit that is clinically meaningful, measurable and fixed before testing begins.

## Method
1. Derive each limit from a source: clinical need, a recognised standard, predicate or competitor data, risk analysis, or bench evidence. Record which.
2. State the condition (temperature, fluid, load rate, sample state, sterilised or not) with the number.
3. Include measurement uncertainty: if the test method has uncertainty U, set the limit so a passing result is credible after accounting for U.
4. Set the sample size and confidence-reliability (a reliability target at a stated confidence) from the risk of failure; higher severity demands higher reliability.
5. Write the acceptance criterion in the protocol before the test (pass if all units meet X; allowed number of failures and what happens on one).
6. Separate **specification** (design limit) from **manufacturing tolerance** (process variation); process capability must support the tolerance.

## Traps
- Limits set to what the prototype achieved (post-hoc criteria).
- Specs with no tolerance on the test method.
- Mean-only criteria for failure-type characteristics; use tolerance or reliability bounds.

## Verify
- [ ] Each limit has a documented source and clinical or risk rationale.
- [ ] Criteria predate the test and are in the approved protocol.
- [ ] Sample size is justified.

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.
