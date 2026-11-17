---
id: computing-software.cloud-infrastructure-engineering.metallb.metrics-relabeling
name: metrics-relabeling
category: computing-software
field: cloud-infrastructure-engineering
product: metallb
tags: [metallb, metric-relabeling, metricrelabelings, frrk8s, servicemonitor, backward-compatible, dashboards]
level: advanced
status: docs-checked
description: "Keep old metallb_bgp_ and metallb_bfd_ dashboards working after moving to FRR-K8s by relabeling frrk8s_ metrics in the ServiceMonitor; the peer label cannot be fixed."
sources:
  - https://raw.githubusercontent.com/metallb/metallb/main/website/content/prometheus-metrics/_index.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Backward-compatible metric relabeling

Before, FRR-based BGP/BFD metrics used the `metallb_` prefix and a `peer` label including the port (`peer="172.23.0.5:179"`). FRR-K8s mode uses `frrk8s_` and the IP only.

To keep `metallb_` names, add metric relabeling to the FRR-K8s ServiceMonitor:
```yaml
metricRelabelings:
- sourceLabels: [__name__]
  regex: "frrk8s_bgp_(.*)"
  targetLabel: "__name__"
  replacement: "metallb_bgp_$1"
- sourceLabels: [__name__]
  regex: "frrk8s_bfd_(.*)"
  targetLabel: "__name__"
  replacement: "metallb_bfd_$1"
```
Where to put it:
- Helm: on the FRR-K8s subchart's ServiceMonitor (see the commented example in `values.yaml`).
- Kustomize: the `config/prometheus-frr-k8s` overlay already includes these rules.

Limit: the `peer` label format change (IP vs IP:port) cannot be fixed by relabeling. Queries that filter on `peer` with a port suffix must be updated.

Context: `computing-software.cloud-infrastructure-engineering.metallb.upgrading-metallb`, `computing-software.cloud-infrastructure-engineering.metallb.metrics-reference`.

## Checked

2026-11-04. The relabeling block, Helm and kustomize placement, and the peer-label limitation match the "Backward-compatible metric relabeling" section of the MetalLB Prometheus Metrics page. Removed the unsupported Verify line.

Method: documentation only; no commands were run.
