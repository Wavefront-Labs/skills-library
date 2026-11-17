---
id: computing-software.cloud-infrastructure-engineering.opentelemetry-operator.opentelemetry-operator-target-allocator-overview-config
name: opentelemetry-operator-target-allocator-overview-config
category: computing-software
field: cloud-infrastructure-engineering
product: opentelemetry-operator
tags: [opentelemetry-operator, target-allocator, targetallocator-config, http-sd-config, prometheus-receiver, collector-namespace]
level: practitioner
status: docs-checked
description: "Understand what the Target Allocator does, its supported collector modes, and the main configuration file keys such as allocation_strategy, filter_strategy and prometheus_cr."
sources: ["https://github.com/open-telemetry/opentelemetry-operator/blob/main/docs/target-allocator/README.md", "https://github.com/open-telemetry/opentelemetry-operator/blob/main/cmd/otel-allocator/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Target Allocator overview and configuration file

The Target Allocator (TA) is an optional component of the Collector custom resource. It decouples Prometheus service discovery from metric collection so each can scale independently: Collectors collect Prometheus metrics with the Prometheus receiver without installing Prometheus, and the TA manages that receiver's configuration. It has two jobs: evenly distribute Prometheus targets among a pool of Collectors, and discover Prometheus Operator custom resources. Currently TA supports Collectors in `statefulset` and `daemonset` mode. Its release version matches the operator's.

Flow: the TA discovers metrics targets and available Collectors, assigns targets, Collectors query the TA for their endpoints, then scrape.

With `targetAllocator.enabled: true` the operator creates a TA deployment and service, and rewrites the Collector's Prometheus receiver so it uses `target_allocator` (endpoint `http://<name>-targetallocator.<namespace>.svc:80`, interval 30s, `collector_id: $POD_NAME`).

Config file (default `/conf/targetallocator.yaml`) keys:
- `collector_namespace` (required, env `OTELCOL_NAMESPACE`) and `collector_selector`
- `listen_addr` (`:8080`, or `:8443` with https), `https`
- `config`: the Prometheus configuration block
- `allocation_strategy` (default `consistent-hashing`), `allocation_strategy_config`
- `filter_strategy`: `relabel-config` (default) or `none`
- `prometheus_cr`: watch Prometheus custom resources
- `allow_insecure_auth_secrets` (default false), `collector_not_ready_grace_period` (30s)
- `kube_config_file_path` (`KUBECONFIG`)

The README also points to `internal/config/config.go` under the repository `cmd/otel-allocator` directory for further options; user docs are under `docs/target-allocator`.

## Checked

Method: docs-checked 2026-11-09 against the Target Allocator README (docs/target-allocator, read in full). The cmd/otel-allocator README was not used.
