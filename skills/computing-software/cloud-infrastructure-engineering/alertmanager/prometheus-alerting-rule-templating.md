---
id: computing-software.cloud-infrastructure-engineering.alertmanager.prometheus-alerting-rule-templating
name: prometheus-alerting-rule-templating
category: computing-software
field: cloud-infrastructure-engineering
product: alertmanager
tags: [alertmanager, alerting-rules, rule-templating, alerts-series]
level: practitioner
status: docs-checked
description: "Templating in Prometheus alert labels and annotations: labels, externalLabels and value variables, plus the synthetic ALERTS series."
sources: ["https://prometheus.io/docs/prometheus/latest/configuration/alerting_rules/", "https://prometheus.io/docs/alerting/latest/notification_examples/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Templating in alert rules

Label and annotation values in a rule can be templated with console templates. Variables:

- `$labels`: label key/value pairs of the alert instance.
- `$externalLabels`: the configured external labels.
- `$value`: the evaluated value of the alert instance.

```
{{ $labels.<labelname> }}
{{ $value }}
```

Example:

```yaml
- alert: InstanceDown
  expr: up == 0
  for: 5m
  labels:
    severity: page
  annotations:
    summary: "Instance {{ $labels.instance }} down"
    description: "{{ $labels.instance }} of job {{ $labels.job }} has been down for more than 5 minutes."
```

The Alertmanager notification examples distinguish the two layers: Prometheus templates apply in the rule's annotation and label fields, while Alertmanager templates (`.GroupLabels`, `.CommonAnnotations`, `.Alerts`) apply in the receiver.

Inspection: the Alerts tab of the Prometheus UI shows pending and firing label sets. For these, Prometheus stores a synthetic series `ALERTS{alertname="<alert name>", alertstate="<pending or firing>", ...}` with value 1 while in that state, marked stale afterwards.

## Checked

2026-11-08. Confirmed against the Alerting rules page (templating variables, example rule, Alerts tab, ALERTS synthetic series) and the Notification template examples page (Prometheus templates in rule fields, Alertmanager templates in the receiver).

Method: documentation only; no commands were run.
