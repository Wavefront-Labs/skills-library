---
id: computing-software.cloud-infrastructure-engineering.cert-manager.best-practice-installation
name: best-practice-installation
category: computing-software
field: cloud-infrastructure-engineering
product: cert-manager
tags: [best-practice, network-policy, replicacount, poddisruptionbudget, priorityclass, hardening]
level: advanced
status: docs-checked
description: "Harden and scale a production cert-manager install with Helm values for network policy, node isolation, HA replicas, PDBs, priority and token mounting."
sources:
  - https://cert-manager.io/docs/installation/best-practice/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Helm values from the best-practice page:

- Network policy: set `networkPolicy.enabled`, `webhook.networkPolicy.enabled`, `cainjector.networkPolicy.enabled` to true. Defaults are over-permissive; default egress is TCP 443, TCP 6443 (OpenShift), TCP/UDP 53 and TCP 80 (HTTP01 self-checks). Metrics listen on TCP 9402.
- Node isolation: the controller and cainjector cache TLS Secrets in memory. Label and taint dedicated nodes (`node-restriction.kubernetes.io/reserved-for=platform`, `NoExecute`) and set `nodeSelector` plus a toleration at top level and under `webhook`, `cainjector`, `startupapicheck`. Keep `kubernetes.io/os: linux`.
- HA: `replicaCount: 2`, `webhook.replicaCount: 3`, `cainjector.replicaCount: 2`. Controller and cainjector use leader election, so extra replicas are standby, not scale. A webhook outage blocks all cert-manager API operations.
- PDBs: `podDisruptionBudget.enabled: true`, `minAvailable: 1` for each component. `replicaCount` must exceed `minAvailable` or drains block.
- `global.priorityClassName: system-cluster-critical`; on GKE-style clusters add a ResourceQuota with a PriorityClass `scopeSelector`.
- No default resource requests or limits; supply them, with more controller memory for many CertificateRequests.
- `automountServiceAccountToken: false` with an explicit projected token volume (`expirationSeconds: 3607`).
- `values.best-practice.yaml` bundles these.

## Checked

2026-11-03: Confirmed against the Best Practice page: `networkPolicy.enabled` for controller, webhook and cainjector, default egress ports (443, 6443, 53 TCP/UDP, 80) and metrics port 9402, node label/taint example (`node-restriction.kubernetes.io/reserved-for=platform`, `NoExecute`) with nodeSelector and tolerations for each component, replicaCount 2/3/2 and leader-election note, webhook outage effect, PodDisruptionBudget with `minAvailable: 1` and the replicaCount warning, `global.priorityClassName: system-cluster-critical` and the GKE ResourceQuota note, no default resources, `automountServiceAccountToken: false` with projected token `expirationSeconds: 3607`, and `values.best-practice.yaml`. Nothing removed.

Method: documentation only; no commands were run.
