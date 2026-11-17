---
id: computing-software.cloud-infrastructure-engineering.metallb.upgrading-metallb
name: upgrading-metallb
category: computing-software
field: cloud-infrastructure-engineering
product: metallb
tags: [metallb, upgrade, release-notes, helm-default-change, frr-k8s, metric-prefix, crds]
level: practitioner
status: docs-checked
description: "Upgrade MetalLB safely: read release notes, reuse your install method, and avoid the Helm default switch from FRR to FRR-K8s that changes pods and metric prefixes."
sources:
  - https://raw.githubusercontent.com/metallb/metallb/main/website/content/installation/_index.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Upgrading MetalLB

1. Read the release notes (https://metallb.io/release-notes/) for changes and required actions, especially for new major/minor releases.
2. Upgrade with the same method you installed with: plain manifests, Kustomize or Helm.
3. Helm upgrades CRDs automatically; do not upgrade them by hand.
4. Take the known limitations of layer 2 and BGP into account when upgrading. See `computing-software.cloud-infrastructure-engineering.metallb.l2-mode-and-failover` and `computing-software.cloud-infrastructure-engineering.metallb.bgp-connection-reset-mitigation`.

Warning, default BGP mode change: the Helm chart default moved from FRR to FRR-K8s. If you relied on defaults (no explicit `speaker.frr.enabled: true`), upgrading switches backend. This changes:
- pod topology (FRR-K8s runs as a separate DaemonSet instead of a sidecar), and
- the Prometheus metric prefix from `metallb_` to `frrk8s_`.

To stay on FRR during upgrade, pin:
```yaml
speaker:
  frr:
    enabled: true
frrk8s:
  enabled: false
```
For dashboards and alerts use relabeling: `computing-software.cloud-infrastructure-engineering.metallb.metrics-relabeling`.

## Checked

2026-11-04. Confirmed against the MetalLB Installation page (Upgrade section: release notes, same install methods, Helm upgrades CRDs automatically, layer 2 and BGP limitations, default BGP mode change warning, pod topology and metric prefix changes, pinning values). Removed the invented failover-blip and connection-reset predictions and the afterwards Check line.

Method: documentation only; no commands were run.
