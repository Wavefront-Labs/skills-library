---
id: computing-software.cloud-infrastructure-engineering.prometheus-operator.prometheus-operator-operator-high-cpu-secret-watch
name: prometheus-operator-operator-high-cpu-secret-watch
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-operator
tags: [operator-cpu, reconcile-rate, secret-field-selector, watch-namespaces, prometheus-operator-metrics]
level: advanced
status: docs-checked
description: "Investigate high CPU in the Prometheus Operator using reconcile metrics and reduce it by limiting watched Secrets and namespaces."
sources: ["https://prometheus-operator.dev/docs/platform/troubleshooting/", "https://prometheus-operator.dev/docs/platform/operator/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
High operator CPU is typically a flood of reconciliations. Measure them with the operator own metrics:

```promql
sum by(controller,triggered_by) (rate(prometheus_operator_triggered_total[5m]))
sum by(controller) (rate(prometheus_operator_reconcile_operations_total[5m]))
```
(The docs show these two expressions to compare triggers against reconcile operations.)

## If `triggered_by="Secret"` dominates
Something is changing Secrets constantly (or there are very many watched). Limit what the operator watches:
- `--secret-field-selector` or `--secret-label-selector` to watch only matching Secrets (similar flags exist for ConfigMaps);
- namespace selectors (`--namespaces`, `--deny-namespaces`, and the per-kind instance namespace flags) to reduce the number of namespaces watched.

By default the operator only watches Secrets and ConfigMaps in the workload namespaces of Prometheus and PrometheusAgent, and in the configuration namespaces of Alertmanager, unless `--watch-referenced-objects-in-all-namespaces` is true.

Also useful: `--auto-gomemlimit-ratio` for memory pressure and `--disable-pprof` when profiling endpoints should not be exposed.

## Checked

2026-11-08. Read the troubleshooting page and the CLI reference in full. Added the CLI reference as a source for the secret, namespace, gomemlimit and pprof flags.

Method: documentation only; no commands were run.
