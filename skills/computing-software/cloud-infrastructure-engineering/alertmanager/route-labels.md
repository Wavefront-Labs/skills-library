---
id: computing-software.cloud-infrastructure-engineering.alertmanager.route-labels
name: route-labels
category: computing-software
field: cloud-infrastructure-engineering
product: alertmanager
tags: [alertmanager, route-labels, routelabels-function, templating]
level: advanced
status: docs-checked
description: "Route labels: labels attached to a route, merged parent to child, templated per alert group and read with routeLabels; they do not affect grouping."
sources: ["https://prometheus.io/docs/alerting/latest/configuration/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Route labels

The route `labels` field attaches a set of labels to a route and makes them available to notification templates through the `routeLabels` template function, and through the `routeLabels` field of the `/api/v2/alerts/groups` API response.

Behaviour:
- Labels merge from parent to child. A child inherits its parent's route labels and may override individual labels by redefining them.
- Unlike `group_by`, route labels do not affect how alerts are grouped.
- Values may themselves be templates, rendered against the notification data of each alert group, so they can reference group labels and other route labels.
- They are rendered per alert group, independently of any notification. Fields only meaningful for a specific notification are unavailable; `.NotificationReason` is always `unknown` in route label templates.

Example from the reference:

```yaml
route:
  labels:
    reason: '{{ .GroupLabels.alertname }}'
    description: '{{ .GroupLabels.alertname }} firing ({{ routeLabels "reason" }})'
  routes:
    - matchers: [ service="database" ]
      group_by: [ alertname, database ]
      labels:
        reason: 'database {{ .GroupLabels.database }}'
```

The sub-route overrides only `reason`; the inherited `description` picks it up automatically.

## Checked

2026-11-08. Confirmed against the Alertmanager configuration reference source (prometheus/alertmanager, docs/configuration.md, main branch, read in full), the published form of the cited prometheus.io page: route label merging, templating, the unknown NotificationReason and the example. Removed: the closing line on the return value of routeLabels (not stated).

Method: documentation only; no commands were run.
