---
id: computing-software.rpa-and-low-code.n8n.track-usage-with-insights
name: track-usage-with-insights
category: computing-software
field: rpa-and-low-code
product: n8n
tags: [n8n, insights, time-saved, workflow-roi, metrics, retention]
level: practitioner
status: docs-checked
description: "Use n8n Insights: summary banner and dashboard metrics, time periods by plan, fixed or dynamic Time Saved, and retention via N8N_INSIGHTS_MAX_AGE_DAYS or disabling the module."
sources:
  - https://docs.n8n.io/administer/observe-and-log/track-usage-with-insights
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: see how workflows perform and how much time they save. Visible to instance owners and admins.

## Parts and availability
- Summary banner (last 7 days, top of **Overview**): Cloud all plans, self-hosted all editions.
- Dashboard (per-workflow table, comparisons): Cloud Pro and Enterprise, self-hosted Business and Enterprise.
- Metrics: production executions (excluding sub-workflow and manual), failed production executions, failure rate, time saved (when set on at least one active workflow), average run time (includes Wait node time).
- Periods: default rolling 7 days vs previous period. Cloud Pro 7 and 14 days; self-hosted Business 24 hours, 7, 14, 30 days; Enterprise adds 90 days, 6 months, 1 year.

## Time saved
Workflow three-dot menu, **Settings**, **Estimated time saved**:
- **Fixed**: minutes saved per production execution on any path.
- **Dynamic**: save, then add **Time Saved** nodes where time is saved. Each sets **Time saved** (minutes) and **Calculation mode** (once for all items, or per item multiplying by input item count). Times from all executed Time Saved nodes add up for the run.
Limits: only parent workflows count (not sub-workflows); error workflow executions are in other metrics but not time saved.

## Self-hosted retention
Compacted data is kept 365 days by default via `N8N_INSIGHTS_MAX_AGE_DAYS`, capped at 730. Older versions pruned by licence defaults (commonly 180); set `N8N_INSIGHTS_MAX_AGE_DAYS=180` to match. Turn collection off with `N8N_DISABLED_MODULES=insights`.

## Checked
Method: docs-checked 2026-11-09 against the n8n "Track usage with Insights" page (docs.n8n.io, read in full).
Nothing removed; availability, metrics, time periods, time saved setup, limits and retention variables match the page.
