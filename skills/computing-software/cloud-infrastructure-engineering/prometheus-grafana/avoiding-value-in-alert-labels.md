---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.avoiding-value-in-alert-labels
name: avoiding-value-in-alert-labels
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [value-in-labels, alert-identity, alerting-rules, alert-annotation-templating, alertmanager]
level: practitioner
status: docs-checked
description: "Never template $value or other changing data into alert labels: it changes alert identity, so alerts restart or resolve and re-fire; put it in annotations instead."
sources: ["https://prometheus.io/docs/prometheus/latest/configuration/alerting_rules/#templating", "https://prometheus.io/docs/alerting/latest/alertmanager/#grouping", "https://prometheus.io/docs/prometheus/latest/configuration/template_reference/", "https://raw.githubusercontent.com/prometheus/prometheus/main/rules/alerting.go", "https://github.com/prometheus/alertmanager#example"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Avoiding $value in alert labels

Label and annotation values of an alerting rule can both be templated, and `$value` holds the evaluated value of the alert instance (alerting rules page). But an alert instance is keyed by its label set: in the Prometheus source (`rules/alerting.go`) the labels are templated on every evaluation, hashed, and the hash looks up the existing active alert. A changed label value therefore means a different alert, not an update of the old one.

## Bad
```yaml
- alert: HighErrorRate
  expr: job:errors:ratio_rate5m > 0.05
  for: 10m
  labels:
    severity: page
    value: "{{ $value }}"          # a different label set whenever the value changes
```
In the source, an active alert whose label hash no longer appears in the evaluation result goes inactive (a pending one is deleted, so its `for` timer restarts), and the new label set starts as a new pending alert. Expect alerts that never leave pending, or that resolve and fire again.

## Good
```yaml
  labels:
    severity: page
  annotations:
    summary: "Error ratio {{ $value | humanizePercentage }} on {{ $labels.job }}"
```
For an alert that already exists, the source updates the stored value and annotations on each evaluation without creating a new alert. `humanizePercentage` converts a ratio to a fraction of 100 (template reference).

## Other identity-changing mistakes
- Labels carried from the expression that change over time, for example `pod` in a deployment-level alert: aggregate it away in the expression (`sum by (namespace, deployment)`).
- A severity label templated from the value (`{{ if gt $value 10.0 }}page{{ else }}ticket{{ end }}`) changes the label set when the value crosses the threshold; write two rules with different thresholds instead, and use an Alertmanager inhibition rule so the `page` alert mutes the `ticket` one (the Alertmanager README shows a critical-inhibits-warning rule).
- The group in Alertmanager is built from labels too (`group_by`), so changing labels also moves alerts between groups.

## Verify
- [ ] The label sets of the alert in the Prometheus Alerts tab (or in the `ALERTS` series) stay the same across evaluations while the annotation text updates.

## Checked
Date: 2026-11-07. Read in full: the Prometheus alerting rules page (labels and annotations templatable; `$labels`, `$externalLabels`, `$value`), the Prometheus template reference (`humanizePercentage`, alert field template variables), the Alertmanager concepts page (Grouping section), and the Alertmanager README (Example section, the inhibit_rules example). Alert identity and the pending-deletion behaviour are taken from `rules/alerting.go` in the Prometheus repository (the template expansion, `lbs.Hash()` lookup in the active map, update of value and annotations, and the removal/inactivation branch); I read lines about 420-525 of that raw file, not the whole thing. Removed: the Alertmanager "groups break" claim and the Grafana-managed alerts gotcha (not on the cited pages), and the `changes()`-based verify step.
Method: documentation only; no commands were run.
