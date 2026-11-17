---
id: computing-software.cloud-infrastructure-engineering.prometheus-operator.prometheus-operator-resource-selectors
name: prometheus-operator-resource-selectors
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-operator
tags: [resource-selectors, servicemonitorselector, namespace-selector, label-selector, scrapeconfigselector, ruleselector, alertmanagerconfigselector]
level: practitioner
status: docs-checked
description: "Wire Prometheus, PrometheusAgent, ThanosRuler and Alertmanager to monitors, probes, scrape configs and rules with selectors, and null versus empty."
sources:
  - https://github.com/prometheus-operator/prometheus-operator/blob/main/Documentation/getting-started/design.md
  - https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/main/Documentation/developer/alerting.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Instance resources find config resources through selector fields. A monitor or rule whose labels do not satisfy the selector is not picked up.

## Selector fields per resource
- `Prometheus` and `PrometheusAgent`: `serviceMonitorSelector`, `podMonitorSelector`, `probeSelector`, `scrapeConfigSelector`, each with a matching `...NamespaceSelector`.
- `Prometheus` and `ThanosRuler`: `ruleSelector` and `ruleNamespaceSelector`.
- `Alertmanager`: `alertmanagerConfigSelector` and `alertmanagerConfigNamespaceSelector`.

## Semantics
The fields follow standard Kubernetes label selector rules, with one operator-specific twist:
- An empty selector (`{}`) matches all objects.
- A null selector (field not specified) matches no objects for a resource selector, and only the current namespace for a namespace selector.
- Anything else matches objects carrying the listed labels.

So `serviceMonitorSelector: {}` selects every ServiceMonitor in the allowed namespaces, while omitting it selects none. Likewise `ruleNamespaceSelector: {}` opens rule discovery to all namespaces, and leaving it out confines discovery to the Prometheus object's own namespace.

## Typical pairing
A `Prometheus` with `serviceMonitorSelector.matchLabels: {team: frontend}` picks up only ServiceMonitors labelled `team: frontend`. Put that label on the monitor, not on the Service. To select a namespace by name use the automatically populated `kubernetes.io/metadata.name` label in `...NamespaceSelector.matchLabels`.

## Checked

2026-11-08. Read the design page and the developer alerting guide in full. Selector fields and the empty versus null semantics match; the kubernetes.io/metadata.name label comes from the alerting guide. Softened an unsourced frequency claim.

Method: documentation only; no commands were run.
