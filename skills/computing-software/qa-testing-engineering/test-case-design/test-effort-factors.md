---
id: computing-software.qa-testing-engineering.test-case-design.test-effort-factors
name: test-effort-factors
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [test-effort-factors, test-estimation, estimation-assumptions, istqb, ctfl]
level: practitioner
status: draft
description: "Identify and quantify factors affecting test effort: product, development process, people and test results factors, and record them as estimate assumptions."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
  - https://www.istqb.org/certifications/certified-tester-advanced-level-test-management-ctal-tm
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Factors affecting test effort

**Goal:** make the drivers of a test estimate explicit (ISTQB CTFL 5.1.4 groups them as product, development process, people and test results characteristics), so the estimate can be challenged and adjusted when a factor changes.

## Factor checklist

| Group | Factor | Pushes effort up when... |
|---|---|---|
| Product | Risks | high-risk areas need deeper techniques |
| Product | Test basis quality | requirements vague, missing acceptance criteria |
| Product | Size and complexity | many integrations, rules, configurations |
| Product | Quality requirements | security, performance, accessibility, regulatory evidence |
| Product | Documentation level required | audit trails, formal reports |
| Process | Stability and maturity | new process, frequent priority changes |
| Process | Lifecycle model | late test involvement, big-bang integration |
| Process | Tools | no automation, manual environments |
| Process | Time pressure | compressed schedule increases rework |
| People | Skills and experience | new team or domain |
| People | Team cohesion, distribution | many time zones, handoffs |
| Results | Defect count and severity | more defects = more retest and regression |
| Results | Rework needed | unstable builds, failed smoke tests |

## Use in an estimate
1. Start from a base estimate (analogy, three-point, test points).
2. Rate each factor low/normal/high with evidence, and apply an adjustment (e.g. +10-30% for poor test basis) agreed with stakeholders.
3. Write each assumption into the test plan ("assumes stable builds daily from sprint 3"; "assumes test environment available by date X").
4. Track assumptions; when one breaks, re-estimate and say which factor changed.

## Verify
The test plan lists factors with ratings and the adjustment each caused, and later re-estimates cite the factor that changed.
