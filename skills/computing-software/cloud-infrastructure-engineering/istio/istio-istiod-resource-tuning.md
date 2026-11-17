---
id: computing-software.cloud-infrastructure-engineering.istio.istio-istiod-resource-tuning
name: istio-istiod-resource-tuning
category: computing-software
field: cloud-infrastructure-engineering
product: istio
tags: [istio, istiod-tuning, istiod, discovery-selectors, pilot]
level: practitioner
status: docs-checked
description: "Set istiod requests, replicas and autoscaling, watch push latency, and reduce config churn with discovery selectors."
sources: ["https://istio.io/latest/docs/ops/configuration/mesh/configuration-scoping/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
By default the control plane reads all configuration in all namespaces and each proxy receives configuration for all namespaces; each configuration costs CPU and memory to maintain, so at large scale limit the scope.

```yaml
meshConfig:
  discoverySelectors:
  - matchLabels: {istio-discovery: enabled}
```

Gotchas: the page lists three scoping tools that can be combined: the `Sidecar` resource (a workload imports only the configuration listed in `egress.hosts`), `exportTo` (the service owner controls visibility) and `discoverySelectors` (Istio ignores configuration outside the selected namespaces). A namespace that does not match the selectors is ignored by Istio entirely, so label every namespace that must stay in the mesh.

Verify: after labelling namespaces, `istioctl proxy-status` still lists all expected proxies.

## Checked

2026-11-03. Confirmed in the Istio configuration scoping page (default read-everything behaviour and its CPU/memory cost, `Sidecar` `egress.hosts`, `exportTo`, `discoverySelectors`) and the mesh config reference (`discoverySelectors`) and proxy-cmd page (`proxy-status`). Removed: the `kubectl top` and `pilot_xds_push_time` commands, the HPA/PDB replica advice, the istiod-outage claim and the staging advice (not on the pages read).

Method: documentation only; no commands were run.
