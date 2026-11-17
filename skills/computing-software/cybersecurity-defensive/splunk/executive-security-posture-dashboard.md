---
id: computing-software.cybersecurity-defensive.splunk.executive-security-posture-dashboard
name: executive-security-posture-dashboard
category: computing-software
field: cybersecurity-defensive
product: splunk
tags: [executive-security-dashboard, security-metrics, kpis, siem-dashboards, dashboard-studio, risk-reporting, board-reporting]
level: advanced
status: draft
description: "Design an executive security posture dashboard: choosing 6-10 outcome metrics, targets and trends, data sources per metric, and avoiding vanity counts."
sources: ["https://www.cisecurity.org/insights/white-papers/cis-controls-v8-measures-and-metrics", "https://csrc.nist.gov/pubs/sp/800/55/v1/final", "https://docs.splunk.com/Documentation/Splunk/latest/DashStudio/IntroFrame"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Executive security posture dashboard

Executives need to see whether risk is going up or down against agreed targets, not alert counts.

## Pick outcome metrics (6-10)
Each metric: definition, data source, target, owner, trend window (13 months shows seasonality).
- Critical/KEV vulnerabilities past SLA (count and % of total) - scanner data.
- Mean time to remediate critical vulns (days) - scanner/ticketing.
- Endpoint protection coverage: % of inventory with healthy EDR - EDR vs CMDB.
- MFA coverage of workforce and privileged accounts - IdP.
- Mean time to detect / respond for true-positive incidents - case management.
- Phishing report rate vs click rate from simulations - awareness platform.
- Backup restore test success for tier-1 systems - backup tooling.
- Log source coverage of crown-jewel systems - SIEM health.

Avoid: total alerts, blocked attacks, events per second. They rise with tooling, not risk.

## Layout
- Top row: single-value tiles with trend arrows and target colouring (green at or better than target).
- Middle: 13-month trend lines per metric with target line.
- Bottom: top 5 risks with owner and due date (from the risk register, not the SIEM).
- One page, no drilldown needed to understand it; drilldowns exist for the security team.

## Build (Splunk Dashboard Studio)
- Summary-index each metric daily (`| collect index=sec_metrics`) so the dashboard queries
  small, stable data and history survives data retention.
- Single value with `trendDisplay` comparing to 30 days ago; threshold colours from targets.
- Schedule PDF monthly to the exec distribution; freeze the numbers in a monthly snapshot.

## Gotchas
- Changing a metric's definition breaks the trend; annotate and restate history.
- Coverage metrics need a trusted denominator (asset inventory); fix the inventory first.
- Never show metrics you cannot explain in one sentence.

## Verify
Walk the dashboard with one executive: they should state, unaided, which areas improved, which
missed target, and what decision is asked of them.
