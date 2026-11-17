---
id: computing-software.qa-testing-engineering.test-case-design.test-work-breakdown-structure
name: test-work-breakdown-structure
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [test-work-breakdown, test-estimation, wbs, test-planning, task-decomposition]
level: practitioner
status: draft
description: "Build a test work breakdown structure: decompose test work by activity and test object into estimable tasks so nothing (data, environments, retests) is forgotten."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Test work breakdown structure

**Goal:** an estimate built from tasks small enough to estimate well (roughly 1-5 days each). Supports ISTQB CTFL v4.0 5.1.4 estimation.

## Decompose two ways
- **By test activity** (CTFL 1.4.1): planning, monitoring/control, analysis, design, implementation, execution, completion.
- **By test object**: features/components/risks, plus non-functional areas.

Grid them and fill in tasks:
```
1 Planning & management
  1.1 Test plan and risk analysis
  1.2 Weekly reporting (n weeks x 2h)
2 Feature: Checkout
  2.1 Analysis & design (decision tables for discounts)
  2.2 API automation
  2.3 Exploratory sessions (6 x 90 min)
3 Non-functional
  3.1 Load test scripting and 2 runs
  3.2 Accessibility audit
4 Support work (often forgotten)
  4.1 Test environment setup and fixes
  4.2 Test data preparation
  4.3 Defect retest and regression cycles (2 cycles)
  4.4 UAT support
  4.5 Tool/framework maintenance
```

## Then
Estimate each leaf (three-point or expert), sum, add contingency for project risks with explanation.

## Gotchas
- Leaving out retest/regression cycles and environment work is the most common underestimate.
- Too fine a WBS (hour-level tasks) wastes time and gives false precision.

## Verify
Review the WBS with a developer and a product owner; ask "what is missing?" before estimating.
