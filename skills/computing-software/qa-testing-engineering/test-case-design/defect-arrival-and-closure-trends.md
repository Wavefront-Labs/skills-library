---
id: computing-software.qa-testing-engineering.test-case-design.defect-arrival-and-closure-trends
name: defect-arrival-and-closure-trends
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [defect-trend-analysis, defect-arrival-rate, defect-metrics, test-monitoring, release-readiness]
level: practitioner
status: draft
description: "Analyse defect arrival and closure trends: cumulative open/closed curves, arrival rate by severity and component, convergence as a release signal."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
  - https://www.istqb.org/certifications/certified-tester-advanced-level-test-management-ctal-tm
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Defect arrival and closure trend analysis

**Goal:** use defect trends to judge product stability and whether the team is converging on a releasable build.

## Charts
- **Daily arrivals and closures** (bars) and **cumulative found vs cumulative fixed/closed** (lines). The gap between the lines is the open backlog.
- **Open defects by severity** over time.
- **Arrivals by component** (heat map): clusters show risky areas for extra testing.
- **Fix and retest age:** time in each status.

Jira: created vs resolved gadget, or JQL exports (`created >= -30d` grouped by day) into a sheet.

## Reading the trends
- **Convergence:** arrival rate falling while test effort stays constant, closure rate above arrival, cumulative curves approaching each other. A good release signal.
- **Falling arrivals with falling test effort** means nothing; normalise by hours tested or tests executed.
- **Spike after a build:** regression from a change; look at that build's commits.
- **Closure far below arrival:** dev capacity problem; escalate before the deadline.
- **Reopen rate high:** weak fixes or weak retests.
- **Late severe arrivals:** risk areas tested too late; revise the test order next time.

## Using for release decisions
Combine with exit criteria: e.g. no new critical defects in the last 5 test days and open highs at zero.

## Verify
Trend charts are in each status report, normalised by test effort, with a written interpretation of convergence and any clusters.
