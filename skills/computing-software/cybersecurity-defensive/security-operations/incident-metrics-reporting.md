---
id: computing-software.cybersecurity-defensive.security-operations.incident-metrics-reporting
name: incident-metrics-reporting
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [incident-metrics, incident-reporting, mttd, mttr, dwell-time, soc-metrics, kpis]
level: practitioner
status: draft
description: "Report incident metrics: MTTD, MTTA, MTTC, MTTR definitions, incident counts by category and severity, dwell time, and presenting trends without gaming."
sources: ["https://csrc.nist.gov/pubs/sp/800/61/r3/final", "https://csrc.nist.gov/pubs/sp/800/55/v1/final", "https://www.verizon.com/business/resources/reports/dbir/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Incident metrics reporting

## Definitions (write them down)
- **Dwell time / time to detect (MTTD)**: first malicious activity (from investigation) to detection.
- **Time to acknowledge (MTTA)**: detection/alert creation to analyst assignment.
- **Time to contain (MTTC)**: detection to containment complete (threat cannot spread/act).
- **Time to recover/resolve (MTTR)**: detection to service restored and incident closed (state which).
- Counts by category (phishing, malware, account compromise, data loss, DoS, insider), severity,
  source of detection (internal detection vs user report vs third party).

## Data capture
Incident records must have timestamps for each milestone as fields, not buried in notes; response
plans/SOAR tasks can stamp them automatically. Detection time vs first activity requires the
investigation to record the earliest evidence.

## Presenting
- Medians and p90 rather than means (one long incident skews averages).
- Trend over 12 months by severity; small numbers of severe incidents: show individually.
- % detected internally vs externally notified: a strong maturity indicator.
- Recurrence: incidents with the same root cause as a previous incident.

## Interpretation
- Rising incident counts after new detections or awareness campaigns can be good.
- Fast MTTR with high recurrence means fixes are shallow.

## Gotchas
- Gaming: closing incidents early to improve MTTR; use reopened rate as a check.
- Mixing alerts and incidents inflates counts; define what an incident is.

## Verify
Recalculate a quarter's metrics from raw incident records and match the published numbers;
definitions appendix accompanies every report.
