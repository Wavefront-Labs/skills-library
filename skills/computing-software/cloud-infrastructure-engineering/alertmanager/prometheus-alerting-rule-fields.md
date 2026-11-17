---
id: computing-software.cloud-infrastructure-engineering.alertmanager.prometheus-alerting-rule-fields
name: prometheus-alerting-rule-fields
category: computing-software
field: cloud-infrastructure-engineering
product: alertmanager
tags: [alertmanager, alerting-rules, for-clause, keep-firing-for]
level: practitioner
status: docs-checked
description: "Prometheus alerting rule fields that feed Alertmanager: alert, expr, for, keep_firing_for, labels, annotations and the pending state."
sources: ["https://prometheus.io/docs/prometheus/latest/configuration/alerting_rules/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Alerting rule fields

Alerting rules live in Prometheus rule files and are written like recording rules. Whenever the expression yields one or more vector elements, the alert is active for those label sets.

```yaml
groups:
- name: example
  labels:
    team: myteam
  rules:
  - alert: HighRequestLatency
    expr: job:request_latency_seconds:mean5m{job="myjob"} > 0.5
    for: 10m
    keep_firing_for: 5m
    labels:
      severity: page
    annotations:
      summary: High request latency
```

- `for`: optional. Prometheus waits this long between first seeing a new element and counting the alert as firing, checking it stays active at each evaluation. Active but not firing elements are `pending`. Without `for`, an alert fires on first evaluation.
- `keep_firing_for`: optional. Keeps the alert firing for this duration after the condition was last met, which helps with flapping and false resolutions from data loss. Without it, an alert deactivates at the first evaluation where the condition is not met.
- `labels`: extra labels attached to the alert; conflicting existing labels are overwritten; values can be templated.
- `annotations`: informational labels for longer text such as descriptions or runbook links; templatable.
- The example also sets group-level `labels` (`team: myteam`) beside `name` and `rules`.

Prometheus then periodically sends alert states to Alertmanager.

## Checked

2026-11-08. Confirmed against the Alerting rules page: the example rule file, for, keep_firing_for, labels, annotations and the pending state. Reworded the group-level labels line to what the example shows.

Method: documentation only; no commands were run.
