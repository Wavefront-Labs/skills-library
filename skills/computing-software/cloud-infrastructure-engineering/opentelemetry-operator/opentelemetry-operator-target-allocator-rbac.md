---
id: computing-software.cloud-infrastructure-engineering.opentelemetry-operator.opentelemetry-operator-target-allocator-rbac
name: opentelemetry-operator-target-allocator-rbac
category: computing-software
field: cloud-infrastructure-engineering
product: opentelemetry-operator
tags: [opentelemetry-operator, targetallocator-rbac, clusterrole, namespace-scoped-rbac, serviceaccount-targetallocator, endpointslices]
level: advanced
status: docs-checked
description: "Grant the Target Allocator the ClusterRole or namespaced Role it needs for service discovery and Prometheus CRs, and know which ServiceAccount the field sets."
sources: ["https://github.com/open-telemetry/opentelemetry-operator/blob/main/docs/target-allocator/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Target Allocator RBAC

The TA needs a ServiceAccount plus roles before it can scrape. Reference your own with `spec.targetAllocator.serviceAccount`. Note that the Collector part of the same CR also has a `serviceAccount` key, which only affects the Collector and not the TA. If you omit it, the operator creates `<collector-name>-targetallocator`, which has no permissions until you bind roles.

Cluster-scoped minimum for target discovery (ClusterRole):
- core `nodes`, `nodes/metrics`, `services`, `endpoints`, `pods`: get, list, watch
- core `configmaps`: get
- `discovery.k8s.io` `endpointslices`: get, list, watch
- `networking.k8s.io` `ingresses`: get, list, watch
- non-resource URL `/metrics`: get

With `prometheusCR.enabled`, add a ClusterRole for `monitoring.coreos.com` `servicemonitors` and `podmonitors` (all verbs in the docs example) and `namespaces` get/list/watch. The two can be combined into one ClusterRole.

Namespace-scoped: set `prometheusCR.allowNamespaces: [foo]` and create a `Role` and `RoleBinding` in that namespace instead. The documented Role covers pods, services, endpoints, configmaps, secrets, namespaces (get, watch, list), `apps` statefulsets, `endpointslices`, `ingresses`, and `monitoring.coreos.com` servicemonitors, podmonitors, scrapeconfigs and probes.

Remember the TA must also be allowed to get Secrets referenced by monitors if endpoints use credentials; see the mTLS note.

## Checked

Method: docs-checked 2026-11-09 against the Target Allocator README, RBAC section (read in full).
