---
id: computing-software.cloud-infrastructure-engineering.alertmanager.alert-and-silence-limits
name: alert-and-silence-limits
category: computing-software
field: cloud-infrastructure-engineering
product: alertmanager
tags: [alertmanager, alerts-per-alertname-limit, silences-max, rate-protection]
level: advanced
status: docs-checked
description: "Alertmanager silence limits: --silences.max-silences and --silences.max-silence-size-bytes, both disabled by default, plus the max_alerts receiver field."
sources: ["https://prometheus.io/docs/alerting/latest/configuration/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Silence limits

Alertmanager supports configurable limits through command-line flags:
- `--silences.max-silences` limits the maximum number of silences, including expired ones.
- `--silences.max-silence-size-bytes` limits the size in bytes of individual silences.
- Both limits are disabled by default.

Webhook and incident.io receivers have a separate `max_alerts` field limiting alerts per message; for webhooks, alerts above it are truncated and the JSON body reports `truncatedAlerts`.

## Checked

2026-11-03. Confirmed against the Alertmanager Configuration page (prometheus.io/docs/alerting/latest/configuration) (Limits section): silence limit flags and their defaults. Removed: the --alerts.per-alertname-limit section and the alertmanager_alerts_limited_total metric (not on any fetched page).

Method: documentation only; no commands were run.
