---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.custom-anomaly-detection
name: custom-anomaly-detection
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, anomaly-management, custom-anomaly-detection, cost-anomaly-detection, seasonality, billing-export]
level: advanced
status: docs-checked
description: "Design custom cost anomaly detection over billing data: series by allocation dimension, thresholds, suppression of planned events, routing and outcome capture."
sources: ["https://www.finops.org/framework/capabilities/anomaly-management/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom anomaly detection over billing data

The FinOps Framework defines anomalies as spending different (usually higher) than normal historical or expected
spend, found by comparing current usage with past usage. Provider and third-party tools usually cover the basics;
build your own where you need dimensions or clouds they do not cover. Custom, tool-based or ML detection are all
acceptable per the Framework (Walk stage: provider, third-party or custom tooling).

## Design
1. **Series**: detect within subcategories, not only in aggregate. The Framework wants granularity by service,
   account or project and cost allocation tag, because allocation metadata is what identifies the owner who can
   resolve an anomaly.
2. **Baseline**: compare current spend with historical behaviour for the same series. Choose the window and seasonality
   handling from your own data and back-test them, as the Framework gives no numbers.
3. **Thresholds**: the Walk stage names context-relevant thresholds: percentage change in spend, a single-item
   spend ceiling, and forecast breach alerts. Use a percentage and an absolute amount together, set with finance and
   leadership (the Framework assigns them to set anomalous percentage thresholds), and move to thresholds tied to service
   components that are updated through the service lifecycle (Run).
4. **Known events**: new launches look like anomalies because detection compares with the past. The Framework expects
   engineering to warn other personas in advance of planned large spend and teams to document those alerts.
5. **Routing**: send alerts automatically to the responsible team, with severity-appropriate integration to
   ticketing or event management at Run. Different personas may have different thresholds.
6. **Outcome capture**: categorise each alert, manage false positives, investigate, and document cause and
   resolution. Use past resolutions to improve later alerting, and run a root cause review where warranted.

## Measures
The Framework lists: anomaly count per period, true versus missed versus false positives, cost associated with
anomaly alerts, mean time to detect, mean time to notify the owner, duration of unresolved anomalies, and time to
investigate.

## Gotchas
- Percentage-only thresholds flood small series and absolute-only thresholds miss large relative moves in big series.
- Detection on billing data can lag usage, so the Crawl stage's reaction of more than a week after the event is a
  warning sign; use the freshest billing data available.

## Verify
- [ ] Detection runs at the allocation granularity owners use, and every alert reaches a named owner.
- [ ] False positives and resolutions are recorded and reviewed.

## Checked
Confirmed on the FinOps Framework Anomaly Management page (read to the KPI list): definition, granularity and
allocation metadata, Crawl/Walk/Run behaviours, thresholds, planned-event alerts, routing, outcome capture and the
success measures. Removed: the SQL example, median and MAD baselines, 3-sigma, 1.3 ratio and dollar thresholds,
28-day and 4-8 week windows, BigQuery ML ARIMA_PLUS, FOCUS column names, the 6-month back-test, and the AWS and
Google Cloud sources (unreadable).
Method: docs-checked 2026-11-09 against finops.org Framework Anomaly Management capability page
