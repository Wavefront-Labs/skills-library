---
id: computing-software.qa-testing-engineering.test-case-design.test-execution-burndown-and-s-curves
name: test-execution-burndown-and-s-curves
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [test-burndown, s-curve, test-monitoring, test-progress, test-metrics]
level: practitioner
status: draft
description: "Track test execution progress with burndown charts and S-curves: planned vs actual executed and passed tests, reading the shape and forecasting completion."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
  - https://www.istqb.org/certifications/certified-tester-advanced-level-test-management-ctal-tm
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Test execution burndown and S-curves

**Goal:** see early whether test execution will finish by the deadline, and why not.

## Data
Per day: planned cumulative tests executed, actual executed, actual passed, blocked, failed. Export from TestRail/Xray/Zephyr or count CI results.

## Charts
- **Burndown:** remaining tests to execute (or remaining story points of testing) vs an ideal line to zero at the deadline.
- **S-curve:** cumulative executed and cumulative passed vs plan. Typical shape: slow start (environment setup, blockers), steep middle, flattening end (hard tests, retests).
- **Stacked status bar** per day: passed, failed, blocked, not run.

## Reading it
- Executed tracking plan but passed lagging far behind: quality problem, many defects; check defect arrival.
- Both lagging with many blocked: environment, data or build problem; escalate the blocker, not the testers.
- Flat line for days: test team diverted or build rejected.
- Executed curve hitting 100% early with low pass rate: tests run, but the product is not ready.

## Forecast
Recent daily execution rate (e.g. last 5 days average) projects the finish date: remaining / rate. Include expected retests (failed tests x retest ratio).

```python
remaining = planned_total - executed
days_left = remaining / mean(daily_executed[-5:])
```

## Verify
The status report shows burndown or S-curve with plan line, a forecast completion date and an explanation for any gap over 10% from plan.
