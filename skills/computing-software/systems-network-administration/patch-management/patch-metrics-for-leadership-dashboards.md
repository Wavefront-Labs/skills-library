---
id: computing-software.systems-network-administration.patch-management.patch-metrics-for-leadership-dashboards
name: patch-metrics-for-leadership-dashboards
category: computing-software
field: systems-network-administration
product: patch-management
tags: [vulnerability-dashboard, patch-metrics, executive-reporting, kev-exposure, sla-compliance, mttr, patch-management]
level: practitioner
status: draft
description: "Report patch and vulnerability metrics to leadership: a few of outcome measures (KEV exposure, SLA compliance by tier, MTTR trend, coverage, exceptions) with clear thresholds."
sources:
  - https://csrc.nist.gov/pubs/sp/800/40/r4/final
  - https://www.cisa.gov/known-exploited-vulnerabilities-catalog
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reporting patch metrics to leadership

**Goal:** leaders understand risk and trend in one page and know what decision is asked of them.

## Pick 5-7 outcome metrics
| Metric | Definition | Why it matters |
|---|---|---|
| KEV exposure | Open instances of CISA KEV vulnerabilities, by tier | Known-exploited = highest real risk |
| SLA compliance | % of critical/high findings remediated within tier SLA | Shows process health |
| Median time to remediate (critical) | Release or detection to verified fix | Speed trend |
| Coverage | % of in-scope assets reporting to patch and scan tools | Unknown assets are unpatched assets |
| Exceptions | Count and age of accepted risks; % past expiry | Hidden risk |
| Internet-facing critical findings | Count, oldest age | Direct attack surface |

Avoid raw "total vulnerabilities": it rises with coverage and scanner changes and drives the wrong behaviour.

## Presentation
- Trend over 6-12 months, one sparkline per metric, with a target line.
- Traffic-light thresholds agreed in advance (e.g. SLA compliance green >= 95%, amber 85-95%, red < 85%).
- Top three risks in words, each with owner and asked-for decision (budget, downtime window, decommission approval).
- Per business unit or service when accountability sits there.

## Data plumbing
Scanner and patch tool exports into a warehouse or Log Analytics; dashboards in Power BI or Grafana; definitions documented next to the dashboard so numbers are reproducible.

## Gotchas
- Changing definitions mid-year breaks trends; version the definitions and annotate the chart.
- Excluding "unknown" assets inflates compliance; show coverage beside compliance.

## Verify
Recompute one month's figures from raw exports and get the same numbers as the dashboard.
