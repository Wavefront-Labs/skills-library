---
id: computing-software.qa-testing-engineering.test-case-design.test-point-analysis-estimation
name: test-point-analysis-estimation
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [test-point-analysis, test-estimation, tpa, function-points, istqb-tm]
level: advanced
status: draft
description: "Estimate test effort with Test Point Analysis: dynamic and static test points from function points, quality characteristics, productivity and environment factors."
sources:
  - https://www.tmap.net/
  - https://www.istqb.org/certifications/certified-tester-advanced-level-test-management-ctal-tm
  - https://www.istqb.org/certifications/certified-tester-foundation-level
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Test Point Analysis (TPA)

**Goal:** a size-based estimate of system/acceptance test effort that is defensible to stakeholders, from the TMap method that extends function point analysis.

## Inputs
- Function points (FP) per function from a function point count (IFPUG), or an approximation.
- Per-function factors: user importance, usage intensity, interfacing (how many logical data sets it touches), complexity (conditions), uniformity (repeated logic counts less).
- Quality characteristics tested dynamically (functionality, security, usability, efficiency) and statically (checklist-based).
- Productivity factor: hours per test point for this team (TMap suggests roughly 0.7-2.0; calibrate from history).
- Environment factor: test tools, prior test experience, test basis quality, development testing quality, testware reuse, environment readiness.

## Calculation outline
1. **Dynamic test points per function:** `FP x Df x Qd`, where Df is the product/sum of the weighted function-dependent factors and Qd the weight for dynamically tested quality characteristics.
2. **Static test points:** `total FP x Qi / 500` for characteristics checked statically.
3. **Total test points** = sum of dynamic points + static points.
4. **Primary test hours** = total test points x productivity factor x environment factor.
5. **Total test hours** = primary hours plus a management allowance (planning and control, typically 10-20% depending on team size and tools).

## Use it well
- Keep a spreadsheet template with the TMap weight tables so counts are consistent.
- Calibrate the productivity factor from completed projects' actuals; uncalibrated TPA is false precision.
- Cross-check with a second method (three-point, analogy) and present a range.

## Verify
The estimate sheet shows FP source, every factor value with rationale, productivity calibration data, and a cross-check estimate within an agreed tolerance.
