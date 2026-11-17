---
id: computing-software.cloud-infrastructure-engineering.opentelemetry-operator.opentelemetry-operator-manager-configuration-sources
name: opentelemetry-operator-manager-configuration-sources
category: computing-software
field: cloud-infrastructure-engineering
product: opentelemetry-operator
tags: [opentelemetry-operator, manager-configuration, config-file, watch-namespace, leader-election, webhook-port]
level: advanced
status: docs-checked
description: "Configure the operator manager through defaults, a --config-file YAML, environment variables and flags, in that override order, including namespaces, webhooks and leader election."
sources: ["https://github.com/open-telemetry/opentelemetry-operator/blob/main/docs/reference/configuration.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Operator manager configuration sources

The manager accepts configuration through four mechanisms, applied in this order with later sources overriding earlier ones: built-in defaults, the `--config-file` YAML, environment variables, then command-line flags. The `operator` and `webhook-server` subcommands share the model. Extra `--zap-*` logging flags are registered separately.

```yaml
watch-namespace: observability
enable-leader-election: true
metrics-addr: ":8443"
tls:
  minversion: VersionTLS13
  configureoperands: true
zap:
  level-format: lowercase
```

General settings (YAML key, flag, env var, default):
- `watch-namespace` / `WATCH_NAMESPACE`: comma-separated namespaces; empty watches all.
- `enable-leader-election` / `ENABLE_LEADER_ELECTION`: false.
- `enable-webhooks` / `ENABLE_WEBHOOKS`: true. `webhook-port`: 9443.
- `ignore-missing-collector-crds`: false.
- `openshift-webhook-replicas` / `OPENSHIFT_WEBHOOK_REPLICAS`: 2 for the standalone webhook on OpenShift OLM; 0 disables.
- `feature-gates` / `FEATURE_GATES`: comma list, prefix `-` to disable (for example `gate1,-gate2`).

File-only keys (no flag or env): `enable-instrumentation-crds`, `instrumentations`, `collector-configmap-entry` (default `collector.yaml`), `target-allocator-configmap-entry`, `operator-op-amp-bridge-configmap-entry`, and the autodetected `create-rbac-permissions`.

`HTTP_PROXY`, `HTTPS_PROXY` and `NO_PROXY` from the operator pod environment are propagated to managed workloads and are not part of the YAML schema.

## Checked

2026-11-04. Confirmed against docs/reference/configuration.md: the four mechanisms and their override order, the shared `operator` and `webhook-server` model, separately registered `--zap-*` flags, the YAML example, the general table (watch-namespace, enable-leader-election false, enable-webhooks true, webhook-port 9443, ignore-missing-collector-crds false, openshift-webhook-replicas 2 with 0 disabling), feature-gates format, the file-only keys (including `collector-configmap-entry` default `collector.yaml`) and proxy variable propagation. Nothing removed.

Method: documentation only; no commands were run.
