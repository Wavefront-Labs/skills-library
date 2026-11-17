---
id: computing-software.cloud-infrastructure-engineering.opentelemetry-operator.opentelemetry-operator-crd-v1beta1-config-and-selectors
name: opentelemetry-operator-crd-v1beta1-config-and-selectors
category: computing-software
field: cloud-infrastructure-engineering
product: opentelemetry-operator
tags: [opentelemetry-operator, structured-config, label-selectors, matchlabels, empty-map, nil-selector]
level: practitioner
status: docs-checked
description: "Convert v1alpha1 string configs to v1beta1 structured YAML, write empty maps as {}, and use standard matchLabels selectors where nil selects nothing."
sources: ["https://github.com/open-telemetry/opentelemetry-operator/blob/main/docs/reference/crd-changelog.md", "https://github.com/open-telemetry/opentelemetry-operator/blob/main/docs/target-allocator/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# v1beta1 structured config and label selectors

Two schema changes in `OpenTelemetryCollector` v1beta1 trip people during migration.

Structured config. In `v1alpha1`, `spec.config` was a YAML string (`config: |`). In `v1beta1` it is a structure aligned with the Collector configuration format. The string form was error-prone (YAML formatting mistakes), gave poor diffs and made it harder for the operator to reject invalid config at admission. Convert by removing the pipe and indenting the YAML as real fields. Empty maps must be explicit:

```yaml
# v1alpha1
exporters:
  debug:
# v1beta1
exporters:
  debug: {}
```

The same applies to `grpc: {}` and `http: {}` under OTLP protocols.

Standard label selectors. Target Allocator Prometheus CR selectors used to be plain maps (`serviceMonitorSelector: {key: value}`). In `v1beta1` they are standard Kubernetes selectors:

```yaml
serviceMonitorSelector:
  matchLabels:
    key: value
```

Semantics changed: a `nil` selector now selects no resources, while an empty selector selects all. To keep the old default of watching everything, set `serviceMonitorSelector: {}` (and `podMonitorSelector: {}`) explicitly; the Target Allocator doc says both must be present in v1beta1 even if unused.

## Checked

2026-11-04. Confirmed against docs/reference/crd-changelog.md: `spec.config` a string in v1alpha1 and a structure in v1beta1, the three listed downsides, empty maps written as `{}` (`debug: {}`, `grpc: {}`, `http: {}`), and the standard label selector change with the nil-selects-nothing and empty-selects-all note. Confirmed against docs/target-allocator/README.md: `serviceMonitorSelector` and `podMonitorSelector` must both be present in v1beta1, and `{}` selects all monitors in every namespace (the README warns about trusting monitor creators before using `{}`). Nothing removed.

Method: documentation only; no commands were run.
