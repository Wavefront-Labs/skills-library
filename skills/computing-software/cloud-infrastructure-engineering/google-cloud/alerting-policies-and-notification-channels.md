---
id: computing-software.cloud-infrastructure-engineering.google-cloud.alerting-policies-and-notification-channels
name: alerting-policies-and-notification-channels
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, alerting-policies, alerting, notification-channels, alert-routing, pagerduty-gcp, slack-alerts, pubsub-notification-channel, webhook-channel, mql-alerts, promql-alerts, log-based-alerts, alert-documentation, severity-labels, snooze, alert-deduplication, multi-condition-alerts, absence-alerts, alerting-as-code]
level: practitioner
status: docs-checked
description: "Cloud Monitoring alerting that pages correctly: metric, PromQL and log-based conditions, absence rules, severity and routing labels, notification channels, runbook docs, snoozes."
sources: ["https://cloud.google.com/monitoring/alerts", "https://cloud.google.com/monitoring/alerts/using-alerting-ui", "https://cloud.google.com/monitoring/alerts/policies-in-json", "https://cloud.google.com/monitoring/support/notification-options", "https://cloud.google.com/logging/docs/alerting/log-based-alerts", "https://cloud.google.com/monitoring/alerts/snooze", "https://cloud.google.com/monitoring/alerts/doc-variables"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Alerting policies and notification channels

**Goal:** an alert fires only when a human must act, reaches the right rota with a runbook
link, and is defined in git so nobody edits it in the console at 3 a.m. and forgets.

## 1. Channels
Create channels in the console, or with the API (`notificationChannels.create`) or `gcloud beta monitoring channels create` (beta only; GA gcloud has no such command). List the channel types and their required labels with the `notificationChannelDescriptors` API rather than guessing label keys.

Types: email, SMS, mobile app, PagerDuty, Slack, webhooks, Pub/Sub. Google documents that SMS is not fully reliable and may be unavailable in some regions, so pair it with another type. Mobile app, PagerDuty, webhook and Slack share one internal service and one failure point: add email or Pub/Sub as the redundant channel. For automation that reads or reroutes notifications use webhook or Pub/Sub; other types' formats can change. A Pub/Sub channel needs `roles/pubsub.publisher` on the topic for the Monitoring service account. Channel per **rota/team**, not per person.

## 2. Policy anatomy (JSON/Terraform)
```json
{
  "displayName": "[P1] Cloud Run 5xx ratio > 2% (payments-api)",
  "combiner": "AND",
  "conditions": [{
    "displayName": "5xx ratio",
    "conditionPrometheusQueryLanguage": {
      "query": "sum(rate(run_googleapis_com:request_count{service_name=\"payments-api\",response_code_class=\"5xx\"}[5m])) / sum(rate(run_googleapis_com:request_count{service_name=\"payments-api\"}[5m])) > 0.02",
      "duration": "300s", "evaluationInterval": "60s", "labels": {"severity": "critical"}
    }
  }],
  "severity": "CRITICAL",
  "alertStrategy": {"autoClose": "1800s", "notificationRateLimit": {"period": "300s"}, "notificationChannelStrategy": [{"notificationChannelNames": ["projects/P/notificationChannels/123"], "renotifyInterval": "3600s"}]},
  "notificationChannels": ["projects/P/notificationChannels/123", "projects/P/notificationChannels/456"],
  "documentation": {"mimeType": "text/markdown", "content": "## Runbook\nhttps://runbooks.example.com/payments-5xx\nService: ${metric.label.service_name}  Project: ${resource.project}\n", "subject": "[P1] payments-api 5xx ${metric.label.service_name}"},
  "userLabels": {"team": "payments", "tier": "1"}
}
```
`gcloud alpha monitoring policies create --policy-from-file=policy.json`; Terraform `google_monitoring_alert_policy`. Condition types: `conditionThreshold` (metric + aggregation + comparison + duration), `conditionAbsent` (no data for N — heartbeat alerts), `conditionMonitoringQueryLanguage`, `conditionPrometheusQueryLanguage`, `conditionMatchedLog` (log-based). `combiner: AND/OR/AND_WITH_MATCHING_RESOURCE` for multi-condition.

## 3. Make it page-worthy
- **Ratio, not count**: errors / requests; latency `histogram_quantile(0.99, …)`; saturation as % of limit.
- **Duration**: set `duration` (the retest window) long enough to ride out single bad samples, on PromQL and threshold conditions alike.
- Use **metric-absence** alerts for anything that should always report (backup jobs, exporters, GMP targets): `conditionAbsent` with `duration: 900s`.
- `severity` field (CRITICAL/ERROR/WARNING; default SEVERITY_UNSPECIFIED) + `userLabels.team` drive routing: Pub/Sub channel → router function → PagerDuty service by label, or separate policies per severity with different channels.
- **Documentation variables**: `${resource.label.instance_id}`, `${metric.label.*}`, `${policy.user_label.team}`, `${log.extracted_label.*}`; include the dashboard link and the exact runbook step.
- `autoClose` so stale incidents disappear; `notificationRateLimit` on log-based alerts so a log storm sends one page.

## 4. Log-based alerts
Save as `log-policy.json`, then `gcloud alpha monitoring policies create --policy-from-file=log-policy.json`:
```json
{"displayName":"[P2] KMS key version destroyed","conditions":[{"displayName":"destroy","conditionMatchedLog":{"filter":"protoPayload.methodName=\"DestroyCryptoKeyVersion\"","labelExtractors":{"key":"EXTRACT(protoPayload.resourceName)"}}}],"combiner":"OR","alertStrategy":{"notificationRateLimit":{"period":"300s"},"autoClose":"1800s"},"notificationChannels":["projects/P/notificationChannels/123"],"documentation":{"content":"Key: ${log.extracted_label.key}"}}
```
`notificationRateLimit` is required for log-based policies, and a log-based policy takes one `conditionMatchedLog` condition with combiner `OR`. For "more than N in 5 min" use a log-based *metric* + threshold condition instead.

## 5. Operate
- **Snooze** during maintenance: `gcloud monitoring snoozes create --criteria-policies=projects/P/alertPolicies/<ID> --start-time=… --end-time=…` — never disable the policy.
- Incidents: console → Alerting → Incidents; acknowledge/close. For downstream automation consume the webhook or Pub/Sub channel payload (fields such as `policy_name` and `condition_name`) rather than scraping the console.
- Review periodically: policies that never open incidents (delete or demote), policies that fire without action (tune), channels with failed deliveries.

## Gotchas
- `evaluationInterval` on a PromQL condition must be a positive multiple of 30 seconds (or omitted).
- Multi-condition `AND` only fires when all conditions are violating *at the same time*; for "A then B" patterns use a single query with `and` in PromQL.

## Verify
- [ ] Test channel delivery with a throwaway policy on a test metric; every channel receives the notification.
- [ ] Forcing errors in staging fires the policy after the duration and the page shows the runbook URL and service name substituted.
- [ ] Stopping the exporter triggers the absence alert at the configured duration.
- [ ] `terraform plan` on the alerting module is clean (no console drift) and every policy has `severity`, `userLabels.team`, and documentation.

## Checked

2026-10-28. Confirmed against: Cloud Monitoring API v3 discovery document (AlertPolicy combiner and severity enums, AlertStrategy, NotificationRateLimit, NotificationChannelStrategy, PrometheusQueryLanguageCondition, Condition types), the alert documentation-variables page (`resource.project`, `resource.label.KEY`, `policy.user_label.KEY`, `log.extracted_label.KEY`), the notification-options page (channel reliability notes, `roles/pubsub.publisher`, payload fields), the log-based alerts page (required rate limit, single condition with `OR`) and gcloud reference (channels create is beta only).

Removed or rewritten: channel-create commands with guessed `--channel-labels` keys, the `gcloud monitoring channels verify` command (no such command), the stdin heredoc form, the 90-day and 20x review thresholds, the scoping-project, Slack private-channel and PromQL `for` gotchas, the PromQL default interval, and timing and percentage test figures.

Method: documentation only; no commands were run.
