---
id: computing-software.it-support-helpdesk.servicenow.performance-analytics-indicators-and-dashboards
name: performance-analytics-indicators-and-dashboards
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, performance-analytics-dashboards, performance-analytics, indicators, breakdowns, kpi-dashboard]
level: practitioner
status: gated
description: "Build ServiceNow Performance Analytics indicators, breakdowns and dashboards for service desk KPIs: sources, data collection jobs, targets, thresholds and trend use."
sources:
  - "https://www.servicenow.com/docs/bundle/zurich-now-intelligence/page/use/performance-analytics/concept/c_PerformanceAnalytics.html"
  - "https://www.servicenow.com/docs/bundle/zurich-now-intelligence/page/use/performance-analytics/concept/c_Indicators.html"
  - "https://www.servicenow.com/docs/bundle/zurich-now-intelligence/page/use/performance-analytics/concept/c_Breakdowns.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# performance-analytics-indicators-and-dashboards

Reports show now; Performance Analytics (PA) stores daily snapshots so you can trend,
forecast and alert. Use PA for KPIs reviewed over time.

Claims in this skill were not verified against primary documentation (gated: unconfirmed, source is paywalled or blocked).

## Building blocks
| Object | What it is | Example |
|---|---|---|
| Indicator source | Table + conditions + frequency | Open incidents (state not resolved/closed), daily |
| Automated indicator | Aggregate over the source | Number of open incidents; average age |
| Formula indicator | Calculation from other indicators | % resolved at first contact |
| Breakdown | Dimension to slice by | Assignment group, priority, category |
| Data collection job | Scheduled job that scores indicators | Daily at 01:00 |

## Steps
1. Create the indicator source with the right **frequency** (daily for most desk KPIs).
2. Create indicators: set aggregate (COUNT, AVG, SUM), unit, direction (minimise /
   maximise), precision.
3. Add breakdowns via breakdown sources (e.g. Assignment group from `sys_user_group`
   active itil groups) and map them to the indicator field.
4. Add the indicator to the daily data collection job; run a **historic collection** for
   past months (bounded: 12-24 months, it is heavy).
5. Set **targets** and **thresholds** (alert when backlog rises 20% over 7 days).
6. Build the dashboard: scorecards for KPIs, time series with trend, breakdown widgets.

## Desk KPI set
New vs resolved per day, open backlog and age, FCR %, reopen %, SLA attainment, average
resolution time by priority, CSAT. Keep the dashboard to one screen per audience.

## Pitfalls
- Indicator source conditions changed later: past scores don't change; note the break or
  recollect.
- Daily snapshots of "open" counts need the job to run at the same time every day.
- Too many breakdown elements make collection slow; restrict to active groups.

## Verify
Indicator scores for a sample day match a list report filtered the same way, and the
collection job completes within its window.

## Checked

- Date: 2026-11-01. Reason: every cited source is paywalled, login-gated or blocked to automated readers (servicenow.com); no readable alternative was found.

Method: documentation only; no commands were run.
