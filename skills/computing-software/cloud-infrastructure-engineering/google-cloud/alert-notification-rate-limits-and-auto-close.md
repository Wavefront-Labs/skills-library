---
id: computing-software.cloud-infrastructure-engineering.google-cloud.alert-notification-rate-limits-and-auto-close
name: alert-notification-rate-limits-and-auto-close
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, alerting, alert-notification-rate-limit, auto-close, log-based-alerts, alert-fatigue]
level: practitioner
status: docs-checked
description: "Tune Cloud Monitoring alert noise: auto-close duration, notification rate limits on log-based alerts, renotification, close prompts and missing-data handling."
sources: ["https://cloud.google.com/monitoring/alerts/concepts-indepth", "https://cloud.google.com/logging/docs/alerting/log-based-alerts", "https://cloud.google.com/monitoring/api/ref_v3/rest/v3/projects.alertPolicies"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Alert notification rate limits and auto-close

## 1. Auto-close
Incidents for metric alerts close when the condition stops being met; if data stops arriving, the
incident auto-closes after `alertStrategy.autoClose` (default 7 days; minimum 30 min).
```yaml
alertStrategy:
  autoClose: 1800s
  notificationPrompts: [OPENED, CLOSED]     # notify on close too
  notificationChannelStrategy:
  - notificationChannelNames: [projects/<P>/notificationChannels/<PAGER>]
    renotifyInterval: 3600s                 # re-send while still open
```

## 2. Log-based alert rate limit (required)
```yaml
conditions:
- displayName: payment failures
  conditionMatchedLog:
    filter: resource.type="cloud_run_revision" AND jsonPayload.event="payment_failed"
    labelExtractors: {customer: EXTRACT(jsonPayload.customer_id)}
alertStrategy:
  notificationRateLimit: {period: 300s}     # at most one notification per 5 min
  autoClose: 1800s
```
`notificationRateLimit` is required for log-based policies; `period` means not more than one notification per period. A log-based policy has one `conditionMatchedLog` condition and `OR` combiner.
For frequency-based alerting ("more than 10 per minute"), use a log-based **metric** with a threshold instead.

## 3. Missing data
Threshold conditions: `evaluationMissingData` is `EVALUATION_MISSING_DATA_INACTIVE` (evaluate as false), `EVALUATION_MISSING_DATA_ACTIVE` (evaluate as true) or `EVALUATION_MISSING_DATA_NO_OP` (no value; unspecified means NO_OP). It is ignored when `duration` is zero. For "service
stopped reporting" use `conditionAbsent` explicitly instead of hoping a threshold fires.

## Gotchas
- `duration` (retest window) too short = flapping.
- One policy can have at most 1,000 open alerts at once; extra met conditions are ignored until some close. Group by fewer labels so one outage does not open hundreds.
- Snooze for planned work: `gcloud alpha monitoring snoozes create --criteria-policies=<POLICY> --start-time=... --end-time=...`.

## Verify
- [ ] Policy JSON (`gcloud alpha monitoring policies describe`) shows the strategy; a test burst of logs produces one notification per rate-limit period.

## Checked

2026-10-28. Confirmed against: Cloud Monitoring API v3 discovery document (AlertStrategy fields, notificationPrompts values, NotificationRateLimit period, renotifyInterval range of 30 minutes upward, evaluationMissingData enum), the log-based alerts page (7 day default auto-close, 1,800 s / 30 min minimum, single condition with `OR`) and the alert-conditions page (1,000 open alerts per policy, missing-data field ignored at zero duration).

Removed: the one-incident-per-entry claim, the 5-minute duration advice and the 200-pages figure.

Method: documentation only; no commands were run.
