---
id: computing-software.cloud-infrastructure-engineering.opentelemetry-operator.opentelemetry-operator-opamp-bridge-standalone-mode
name: opentelemetry-operator-opamp-bridge-standalone-mode
category: computing-software
field: cloud-infrastructure-engineering
product: opentelemetry-operator
tags: [opentelemetry-operator, opamp-standalone, configmap-backed-config, workloadref, kustomize-standalone, restartedat]
level: advanced
status: docs-checked
description: "Run the OpAMP Bridge without the operator CRDs to manage Collector config stored in ConfigMaps, restarting workloads with the restartedAt annotation after updates."
sources: ["https://github.com/open-telemetry/opentelemetry-operator/blob/main/cmd/operator-opamp-bridge/README.md", "https://github.com/open-telemetry/opentelemetry-operator/blob/main/cmd/operator-opamp-bridge/manifests/standalone/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# OpAMP Bridge standalone mode

Standalone mode lets the bridge manage Collector configuration stored in Kubernetes `ConfigMap` resources without creating `OpenTelemetryCollector` CRDs, useful when the Collector workload is managed outside the operator. Start with `mode: standalone` in the config file or `--mode=standalone`:

```yaml
endpoint: "<OPAMP_SERVER_ENDPOINT>"
mode: standalone
capabilities:
  AcceptsRemoteConfig: true
  ReportsEffectiveConfig: true
  ReportsRemoteConfig: true
standalone:
  agents:
    - namespace: default
      type: otel-collector
      workloadRef: {apiVersion: apps/v1, kind: Deployment, name: my-collector}
      config:
        collector: {kind: configmap, name: collector-config, key: collector.yaml}
```

Behaviour:
- To let the bridge restart deployment pods you must enable the `AcceptsRestartCommand` capability, which needs patch permission on deployments. Standalone mode also needs RBAC for ConfigMaps and the configured workload types (starter manifest `manifests/standalone/rbac.yaml`).
- One OpAMP client connection per entry in `standalone.agents`.
- `description.non_identifying_attributes` can be set bridge-wide as defaults and overridden per agent. The bridge always reports `opentelemetry.io/opamp.bridge.mode` as `operator` or `standalone`.
- Each key under an agent's `config` is the OpAMP config file name seen by the server (`collector` here), mapped locally to a resource in the workload namespace (`ConfigMap/default/collector-config`, key `collector.yaml`).
- After applying an update the bridge restarts the workload by updating the pod template annotation `kubectl.kubernetes.io/restartedAt`. Supported refs: `apps/v1` Deployment, DaemonSet and StatefulSet.
- The bridge never creates or deletes ConfigMaps.

Without the operator: a Kustomize base in `manifests/standalone` needs no operator, CRDs or cert-manager, deploys into `opentelemetry-opamp-bridge` with `make deploy-standalone-bridge`, and fits the OpenShift restricted SCC profile (non-root, no privilege escalation, all capabilities dropped, read-only root filesystem).

## Checked

2026-11-04. Confirmed against cmd/operator-opamp-bridge/README.md: standalone purpose, `mode: standalone` or `--mode=standalone`, one client per `standalone.agents` entry, bridge-level and per-agent `non_identifying_attributes`, `opentelemetry.io/opamp.bridge.mode`, config key mapping in the workload namespace, the `kubectl.kubernetes.io/restartedAt` restart with Deployment, DaemonSet and StatefulSet refs, and no ConfigMap creation or deletion. Confirmed against manifests/standalone/README.md: Kustomize base without operator, CRDs or cert-manager, namespace `opentelemetry-opamp-bridge`, `make deploy-standalone-bridge`, and the OpenShift restricted SCC compatibility. Added the AcceptsRestartCommand and RBAC requirements the README marks as important.

Method: documentation only; no commands were run.
