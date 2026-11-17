---
id: computing-software.cloud-infrastructure-engineering.prometheus-operator.prometheus-operator-operator-flags-and-scoping
name: prometheus-operator-operator-flags-and-scoping
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-operator
tags: [operator-flags, namespaces, deny-namespaces, controller-id, feature-gates, config-reloader, instance-selector, tls]
level: advanced
status: docs-checked
description: "Configure the Prometheus Operator process: namespace scoping, instance selectors, controller-id, feature gates, config-reloader resources, kubelet endpoint options and web TLS."
sources: ["https://prometheus-operator.dev/docs/platform/operator/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The operator binary takes commands `start` (default), `crds` and `full-crds` (print CRDs as YAML), plus these notable arguments.

## Scoping
- `--namespaces` (allow list) and `--deny-namespaces` are mutually exclusive.
- `--prometheus-instance-namespaces`, `--alertmanager-instance-namespaces`, `--thanos-ruler-instance-namespaces` and `--alertmanager-config-namespaces` override the generic list for that kind.
- `--prometheus-instance-selector`, `--alertmanager-instance-selector` and `--thanos-ruler-instance-selector` filter which custom resources to watch by label.
- `--controller-id`: reconcile only resources annotated `operator.prometheus.io/controller-id` with the same value.
- `--secret-label-selector`, `--secret-field-selector`, `--configmap-label-selector`, `--configmap-field-selector` limit watched Secrets and ConfigMaps.

## Behaviour
- `--feature-gates`: `PrometheusAgentDaemonSet` (off), `PrometheusShardRetentionPolicy` (on), `PrometheusTopologySharding` (on), `RemoteWriteCustomResourceDefinition` (off), `StatusForConfigurationResources` (off).
- `--config-reloader-cpu-limit`, `-cpu-request`, `-memory-limit`, `-memory-request` default to 10m and 50Mi; `0` removes the setting.
- `--disable-unmanaged-prometheus-configuration` turns off the deprecated unmanaged-config mode.
- `--repair-policy-for-statefulsets` is `none`, `evict` or `delete`.
- `--kubelet-endpoints`, `--kubelet-endpointslice`, `--kubelet-http-metrics` (port 10255; set false where the read-only port is disabled), `--kubelet-sync-period` (3m).

## Web server
`--web.listen-address` (`:8080`), `--web.enable-tls`, `--web.cert-file`, `--web.key-file`, `--web.client-ca-file`, `--web.tls-min-version` (default TLS 1.3), `--web.tls-reload-interval` (1m). `--log-format` is logfmt or json.

## Checked

2026-11-08. Read the operator CLI reference page in full. Flags, defaults and feature gate states match; no changes needed.

Method: documentation only; no commands were run.
