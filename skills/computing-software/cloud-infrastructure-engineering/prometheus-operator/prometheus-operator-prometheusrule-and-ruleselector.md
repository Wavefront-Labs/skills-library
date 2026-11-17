---
id: computing-software.cloud-infrastructure-engineering.prometheus-operator.prometheus-operator-prometheusrule-and-ruleselector
name: prometheus-operator-prometheusrule-and-ruleselector
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-operator
tags: [prometheusrule, alerting-rules, recording-rules, rulenamespaceselector, ruleselector-nil]
level: practitioner
status: docs-checked
description: "Deploy alerting and recording rules with PrometheusRule and make Prometheus pick them up via ruleSelector and ruleNamespaceSelector."
sources:
  - https://prometheus-operator.dev/docs/developer/alerting/
  - https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/main/Documentation/platform/webhook.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`PrometheusRule` defines alerting and recording rules. The operator loads them into Prometheus (or Thanos Ruler) dynamically, with no restart.

## Selection
`spec.ruleSelector` on the `Prometheus` object chooses rules by label. By default it is nil, which means the operator picks up no rules at all. By default only rules in the Prometheus object's namespace are discovered; refine with `ruleNamespaceSelector`:
- `ruleNamespaceSelector: {}` discovers from all namespaces;
- `matchLabels` limits to namespaces carrying a label; to pick a single namespace by name use the `kubernetes.io/metadata.name` label.

Example: rules labelled `role=alert-rules` and `prometheus=example` from namespaces labelled `team=frontend`.

## Verify
Create a `PrometheusRule` whose labels match `ruleSelector`. The documentation example always fires an `ExampleAlert`; confirm it on the Prometheus Alerts page and then as an active alert in the Alertmanager UI.

## Validation
The admission webhook (if deployed) validates that `PrometheusRule` objects are semantically valid through `/admission-prometheusrules/validate`. Prometheus sends each firing alert to all Alertmanager instances on every evaluation interval.

## Checked

2026-11-08. Read the developer alerting guide and the webhook guide in full. Selector defaults, namespace selector options and the example rule match. Replaced an unsourced events claim with the webhook validation endpoint.

Method: documentation only; no commands were run.
