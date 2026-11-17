---
id: computing-software.qa-testing-engineering.test-automation.automation-roi-and-payback
name: automation-roi-and-payback
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [automation-payback, automation-roi, test-automation-strategy, business-case, istqb-tae]
level: practitioner
status: draft
description: "Calculate test automation ROI and payback: build and maintenance costs, manual effort saved per run, faster feedback value, break-even runs and honest sensitivity ranges."
sources:
  - https://www.istqb.org/certifications/certified-tester-advanced-level-test-automation-engineering-ctal-tae
  - https://www.istqb.org/certifications/certified-tester-foundation-level
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Calculating automation ROI and payback

**Goal:** a business case for automating a test set that survives scrutiny, including maintenance, which most ROI slides omit.

## Costs
- **Build:** hours to automate each test (often 3-10x the manual execution time for UI tests), framework setup, CI integration.
- **Maintenance per run or per month:** fixing tests after product changes, flake triage, environment upkeep. Estimate from existing suites (typically 10-30% of build effort per year for stable UIs, more for volatile ones).
- **Infrastructure and licences:** CI minutes, device clouds, tools.
- **Run analysis:** time to review failures.

## Benefits
- **Manual effort saved** = manual execution hours per run x runs per period. Count only runs that would really have happened manually (automation runs 50 times a day, but you would never have run it manually 50 times).
- **Earlier defect detection:** defects caught at PR instead of system test (use team data on cost per escaped defect, conservatively).
- Faster release cycles, reduced regression phase duration.

## Payback

```python
build = 120          # hours
maint_per_month = 8
manual_per_run = 6   # hours of manual regression replaced
runs_per_month = 4   # realistic manual-equivalent runs
monthly_saving = manual_per_run * runs_per_month - maint_per_month   # 16 h
payback_months = build / monthly_saving                                  # 7.5 months
```
If monthly saving is zero or negative, the automation never pays back on effort alone; justify it on feedback speed or do not automate.

## Sensitivity
Show best/likely/worst for maintenance and runs; the decision should hold in the likely case. Re-measure actual maintenance after 3 months.

## Verify
The business case lists every cost category, uses realistic manual-equivalent run counts, states payback in months with a range, and is revisited with actuals.
