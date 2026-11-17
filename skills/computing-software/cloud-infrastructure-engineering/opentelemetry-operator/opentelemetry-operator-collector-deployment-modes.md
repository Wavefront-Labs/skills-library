---
id: computing-software.cloud-infrastructure-engineering.opentelemetry-operator.opentelemetry-operator-collector-deployment-modes
name: opentelemetry-operator-collector-deployment-modes
category: computing-software
field: cloud-infrastructure-engineering
product: opentelemetry-operator
tags: [opentelemetry-operator, deployment-modes, daemonset, statefulset, sidecar, deployment, mode-field]
level: intro
status: docs-checked
description: "Choose the OpenTelemetryCollector spec.mode (deployment, daemonset, statefulset or sidecar) and know which spec fields only apply to certain modes."
sources: ["https://github.com/open-telemetry/opentelemetry-operator/blob/main/docs/collector/deployment-modes.md", "https://github.com/open-telemetry/opentelemetry-operator/blob/main/docs/api/opentelemetrycollectors.md", "https://github.com/open-telemetry/opentelemetry-operator/blob/main/docs/target-allocator/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Collector deployment modes

`spec.mode` on an `OpenTelemetryCollector` selects how the Collector runs. The enum values in the API reference are `deployment`, `daemonset`, `statefulset` and `sidecar`. The deployment-modes page lists an example for each mode and says Deployment is the default.

Mode-dependent fields from the v1beta1 API reference:
- `volumeClaimTemplates` and `persistentVolumeClaimRetentionPolicy` only work in `statefulset` mode.
- `deploymentUpdateStrategy` applies only to `deployment` mode, and `daemonSetUpdateStrategy` only to `daemonset` mode.
- `nodeSelector` works for daemonset, statefulset and deployment modes.
- `ingress` is available only for deployment, daemonset and statefulset.
- `podSecurityContext` is ignored in sidecar mode, where the operator injects a container into your own pod instead of creating a workload.
- The Target Allocator README says it currently supports the `statefulset` and `daemonset` modes.

`spec.replicas` (default 1) is for non-autoscaled instances, and the operator also records `managementState` (`managed` or `unmanaged`).

## Checked

2026-11-04. Confirmed against docs/collector/deployment-modes.md (Deployment is the default; examples for Deployment, DaemonSet, StatefulSet, Sidecar) and the generated OpenTelemetryCollector API reference (docs/api/opentelemetrycollectors.md, read as raw Markdown because the GitHub page view is a stub): the `mode` enum, `volumeClaimTemplates` and `persistentVolumeClaimRetentionPolicy` statefulset only, `deploymentUpdateStrategy` and `daemonSetUpdateStrategy` mode limits, `nodeSelector` and `ingress` modes, `podSecurityContext` ignored in sidecar mode, `replicas` default 1 and `managementState` managed or unmanaged. Confirmed in docs/target-allocator/README.md: statefulset and daemonset support. Removed the unverified claim about an e2e tests directory.

Method: documentation only; no commands were run.
