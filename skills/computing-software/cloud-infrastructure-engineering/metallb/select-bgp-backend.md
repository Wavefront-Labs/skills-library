---
id: computing-software.cloud-infrastructure-engineering.metallb.select-bgp-backend
name: select-bgp-backend
category: computing-software
field: cloud-infrastructure-engineering
product: metallb
tags: [metallb, backend-selection, frr-logging, frr-k8s, native-bgp, helm-values, frr-logging-level]
level: advanced
status: docs-checked
description: "Pick the MetalLB BGP backend (FRR-K8s, native, FRR) via manifests or Helm values, and map speaker --log-level to FRR log levels with FRR_LOGGING_LEVEL override."
sources:
  - https://raw.githubusercontent.com/metallb/metallb/main/website/content/installation/_index.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Select the BGP backend

Helm default is FRR-K8s. Set values explicitly for the others.

Deprecated FRR mode:
```yaml
speaker:
  frr:
    enabled: true
frrk8s:
  enabled: false
```
Native BGP (no FRR):
```yaml
speaker:
  frr:
    enabled: false
frrk8s:
  enabled: false
```
Manifests/Kustomize: pick `metallb-frr-k8s`, `metallb-native` or `metallb-frr` (`computing-software.cloud-infrastructure-engineering.metallb.install-by-manifest-or-kustomize`). Operator: `computing-software.cloud-infrastructure-engineering.metallb.install-with-operator`.

FRR daemon log level follows the speaker `--log-level`:

| Speaker | FRR |
|---|---|
| all, debug | debugging |
| info | informational |
| warn | warnings |
| error | error |
| none | emergencies |

Override with the speaker env var `FRR_LOGGING_LEVEL` set to any value FRR supports (`log stdout LEVEL`).

Topology: FRR-K8s runs as a separate DaemonSet, FRR mode as a sidecar, and the metric prefix differs (`frrk8s_` versus `metallb_`). The chart default changed from FRR to FRR-K8s, so pin the FRR values above if you must keep FRR mode on upgrade.

## Checked
2026-11-04. Confirmed against the MetalLB "Installation" page: Helm default and the FRR and native values, manifest names, log-level table, FRR_LOGGING_LEVEL, and the default-mode-change warning. Removed a generic kubectl check line.
Method: documentation only; no commands were run.
