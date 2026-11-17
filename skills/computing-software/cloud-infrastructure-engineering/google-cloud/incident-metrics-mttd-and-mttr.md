---
id: computing-software.cloud-infrastructure-engineering.google-cloud.incident-metrics-mttd-and-mttr
name: incident-metrics-mttd-and-mttr
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, incident-management, mttr-metrics, mttd, time-to-mitigate, incident-timeline, bigquery]
level: practitioner
status: docs-checked
description: "Measure incident response consistently: time to detect, acknowledge, mitigate and resolve from alerts and postmortems, reported as percentiles."
sources: ["https://sre.google/workbook/incident-response/", "https://cloud.google.com/blog/products/devops-sre/using-the-four-keys-to-measure-your-devops-performance", "https://cloud.google.com/monitoring/alerts/incidents-events"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Incident metrics: MTTD and MTTR

## Define timestamps first
| Timestamp | Source |
|---|---|
| impact start | SLI graph / logs (retrospective) |
| detected | alert opened (Cloud Monitoring alert open time) or first human report |
| acknowledged | paging tool ack (Cloud Monitoring alerts can be marked Acknowledged) |
| mitigated | user impact ends (SLI recovered) |
| resolved | root cause fixed / incident closed |

- **TTD** = detected - impact start; **TTA** = ack - detected; **TTM** = mitigated - impact start;
  **TTR** = resolved - impact start. Report TTM separately: it is what users feel.

## Collect
- Store each incident as a row (postmortem template fields) in BigQuery or a sheet:
  ```sql
  CREATE TABLE ops.incidents (id STRING, sev STRING, service STRING,
    impact_start TIMESTAMP, detected TIMESTAMP, acked TIMESTAMP, mitigated TIMESTAMP, resolved TIMESTAMP,
    detection_source STRING, error_budget_consumed FLOAT64);
  SELECT sev, APPROX_QUANTILES(TIMESTAMP_DIFF(mitigated, impact_start, MINUTE), 100)[OFFSET(50)] p50_ttm,
         APPROX_QUANTILES(TIMESTAMP_DIFF(mitigated, impact_start, MINUTE), 100)[OFFSET(90)] p90_ttm,
         COUNTIF(detection_source != 'alert') / COUNT(*) AS pct_not_alert_detected
  FROM ops.incidents WHERE resolved > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 180 DAY) GROUP BY sev;
  ```
- The Cloud Monitoring Alert details page records when an alert was opened or closed; copy those times into the incident row. An alert closes when the condition stops being met, when someone closes it, or after 7 days without an observation that the condition continued, so do not treat alert close time as the resolved time.

## Interpreting
- Use medians/percentiles, not means: one long outage dominates averages; small samples mislead.
- `% incidents detected by customers` is often more actionable than MTTD.
- Do not set MTTR targets for individuals; use trends to drive investments (alerting, runbooks, rollbacks).

## Gotchas
- Inconsistent definitions across teams make numbers meaningless; write the definitions into the postmortem template.
- Severity re-classification after the fact skews per-severity stats; record original and final.

## Verify
- [ ] Quarterly report shows p50/p90 TTM per severity from complete incident records.

## Checked
2026-11-09. Confirmed in the Cloud Monitoring alerts page (alert states Open, Acknowledged, Closed; opened/closed times; 7-day auto-close), the Four Keys post (time to restore service needs incident created and resolved times) and the BigQuery reference (APPROX_QUANTILES, COUNTIF, TIMESTAMP_DIFF, TIMESTAMP_SUB). Removed: the claim that alert times arrive via a Pub/Sub channel and the Cloud Monitoring `started` field name (not on the page).
Method: documentation only; no commands were run.
