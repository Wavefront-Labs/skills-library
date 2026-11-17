---
id: computing-software.cybersecurity-defensive.splunk.soc-metrics-dashboard
name: soc-metrics-dashboard
category: computing-software
field: cybersecurity-defensive
product: splunk
tags: [splunk, siem-dashboards, soc-metrics-dashboard, mttd, mttr, alert-volume, true-positive-rate, analyst-workload, incident-review, kpi]
level: practitioner
status: draft
description: "Build a SOC metrics dashboard from notable/case data: alert volume, true-positive rate by rule, time to triage and resolve, backlog age and analyst load."
sources: ["Splunk Docs - Enterprise Security (Incident Review audit dashboard, notable event statuses)", "SANS SOC Survey (metrics used by SOCs)", "CySA+ CS0-003 objective 4.2 (incident response metrics)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SOC metrics dashboard

**Goal:** measure whether the SOC detects and resolves real threats quickly, and which
detections waste analyst time, using data the SIEM already holds.

## Data you need
- Alert/notable creation time and source rule (`notable` macro in ES, `SecurityAlert` in Sentinel).
- Status changes with timestamps and owner (`incident_review_lookup` / `` `incident_review` `` in ES).
- Final disposition (true positive, benign true positive, false positive) as a required close field.
  Without a mandatory disposition there are no quality metrics.

## Core panels (ES example)
Time to triage (first status change):
```
`notable` | eval created=_time
| join type=left rule_id [| `incident_review` | stats min(_time) as first_touch by rule_id]
| eval ttt_min=round((first_touch-created)/60,1)
| stats median(ttt_min) as median_ttt perc90(ttt_min) as p90_ttt by urgency
```
True-positive rate by detection:
```
`notable` | `get_disposition`
| stats count as total count(eval(disposition="True Positive")) as tp by search_name
| eval tp_rate=round(100*tp/total,1) | sort tp_rate
```
(Define `get_disposition` for your environment; ES 7+ has a disposition field on notables.)
Backlog by age: open notables bucketed as <4h, 4-24h, 1-3d, >3d.
Load: closed per analyst per shift (use for capacity, never for individual ranking).

## Which metrics to show
| Metric | Why |
|---|---|
| Median and p90 time to triage, by urgency | Is the queue served within SLA? Use medians: means are distorted by one forgotten alert. |
| Time to contain for confirmed incidents | Business impact. |
| TP rate and volume per rule | Top tuning targets: high volume, low TP rate. |
| Backlog age | Early warning of staffing problems. |
| Detection coverage (ATT&CK techniques with tested detections) | Programme progress, monthly. |

## Gotchas
- Counting alerts as success rewards noise. Show TP volume and coverage alongside.
- Auto-closed alerts (SOAR) must be separated or they flatten time-to-triage.
- Time zones: compute durations from epoch fields, never from formatted strings.
- MTTD needs the time the activity started, which only exists after investigation: record it in the case.

## Verify
- [ ] Every closed notable has a disposition (count of null dispositions is zero).
- [ ] Numbers reconcile with a manual count for one sample week.
- [ ] The dashboard has led to at least one tuning or staffing decision; otherwise trim it.
