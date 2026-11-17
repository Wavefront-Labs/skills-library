---
id: computing-software.cloud-infrastructure-engineering.cilium.clustermesh-service-affinity
name: clustermesh-service-affinity
category: computing-software
field: cloud-infrastructure-engineering
product: cilium
tags: [cilium, clustermesh, service-affinity, service-cilium-io-affinity, local, remote]
level: practitioner
status: docs-checked
description: "Prefer local or remote backends for a global service with the service.cilium.io/affinity annotation and verify with cilium-dbg service list --clustermesh-affinity."
sources:
  - https://docs.cilium.io/en/stable/network/clustermesh/affinity/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# ClusterMesh service affinity

Annotation `service.cilium.io/affinity` on a global service takes `none` (default), `local` or `remote`. With MCS-API, set it through the ServiceExport `exportedAnnotations` field.

- `local`: load-balance across healthy local backends only, using remote backends only if all local ones are unavailable or unhealthy.
- `remote`: prefer remote cluster backends if available.

Change at runtime: `kubectl annotate service rebel-base service.cilium.io/affinity=local --overwrite`; remove with `kubectl annotate service rebel-base service.cilium.io/affinity- --overwrite`.

Verify which backends are preferred: `kubectl exec -n kube-system -ti ds/cilium -- cilium-dbg service list --clustermesh-affinity` marks backends `(preferred)`. Affinity is per cluster: the cluster without the annotation still sees replies from both clusters.

## Checked

2026-11-03. Claims were read against: https://docs.cilium.io/en/stable/network/clustermesh/affinity/. 

Method: documentation only; no commands were run.
