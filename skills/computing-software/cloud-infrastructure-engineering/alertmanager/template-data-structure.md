---
id: computing-software.cloud-infrastructure-engineering.alertmanager.template-data-structure
name: template-data-structure
category: computing-software
field: cloud-infrastructure-engineering
product: alertmanager
tags: [alertmanager, templating, data-structure, grouplabels, commonannotations]
level: practitioner
status: docs-checked
description: "The Data object passed to Alertmanager notification templates: Receiver, Status, Alerts, GroupLabels, CommonLabels, CommonAnnotations, RouteLabels, ExternalURL."
sources: ["https://prometheus.io/docs/alerting/latest/notifications/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# The Data structure in templates

Data is the structure passed to notification templates and webhook pushes.

| Name | Type | Notes |
|---|---|---|
| Receiver | string | Name of the receiver the notification goes to |
| Status | string | `firing` if at least one alert is firing, otherwise `resolved` |
| Alerts | Alert list | All alert objects in this group |
| GroupLabels | KV | The labels the alerts were grouped by |
| CommonLabels | KV | Labels common to all alerts |
| CommonAnnotations | KV | Annotations common to all alerts; used for longer strings |
| RouteLabels | KV | Route labels attached to this group; usually read via `routeLabels` |
| ExternalURL | string | Backlink to the Alertmanager that sent the notification |

The Alerts type exposes filtering helpers:
- `Alerts.Firing` returns currently firing alert objects.
- `Alerts.Resolved` returns resolved alert objects.

```
{{ range .Alerts.Firing }}{{ .Labels.instance }} {{ end }}
{{ .CommonAnnotations.summary }}
```

Alertmanager templates differ from Prometheus templating, which also covers alert rule labels and annotations. Alertmanager templates are based on the Go templating system, and some fields are evaluated as text and others as HTML, which affects escaping. Default templates ship with Alertmanager and can be customized.

## Checked

2026-11-08. Confirmed against the Notification template reference: the Data fields, Alerts.Firing and Alerts.Resolved, differences from Prometheus templating, Go templating and text versus HTML evaluation.

Method: documentation only; no commands were run.
