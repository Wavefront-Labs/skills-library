---
id: computing-software.cloud-infrastructure-engineering.external-dns.service-type-filter-informer-scope
name: service-type-filter-informer-scope
category: computing-software
field: cloud-infrastructure-engineering
product: external-dns
tags: [external-dns, service-type-filter, informer-scope, memory-usage, watchlist, label-filter]
level: advanced
status: docs-checked
description: "Cut ExternalDNS memory on large clusters: the service source watches Pods, EndpointSlices and Nodes unless --service-type-filter narrows it; WatchList and startup bursts."
sources:
  - https://raw.githubusercontent.com/kubernetes-sigs/external-dns/master/docs/advanced/operational-best-practices.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Informer scope and memory

The `service` source registers informers for Services, Pods, EndpointSlices and Nodes depending on service types in scope:

| Informers | Active when |
|---|---|
| Services | always |
| Pods + EndpointSlices | `NodePort` or `ClusterIP` in scope |
| Nodes | `NodePort` in scope |

With no `--service-type-filter` (the default) every service type is in scope, so ExternalDNS caches every Pod, EndpointSlice and Node in the cluster.

**Fix:** list only the types you publish.
```sh
--service-type-filter=LoadBalancer
```
Filter values and the informers they remove: `LoadBalancer` or `LoadBalancer,ExternalName` removes Pods, EndpointSlices and Nodes; `ClusterIP` removes Nodes; `NodePort` removes none.

Narrow further:
```sh
--label-filter=external-dns/enabled=true
--annotation-filter=external-dns.kubernetes.io/hostname
```

The memory saving is a side effect; choose filters by the records you actually need.

**Startup burst:** the classic LIST path loads all objects of a type at once. The `WatchListClient` feature gate streams them instead and defaults to `true` in recent client-go, so the burst is effectively eliminated on the latest release. On older releases `--service-type-filter` is the main mitigation. Transformers and indexers are still needed for steady-state memory.

## Checked

2026-11-04. Confirmed against the ExternalDNS Operational Best Practices page (Resource Scope and Memory): informer table, default behaviour, filter table, label and annotation filters, WatchList note. Removed an unsourced verification line.
Method: documentation only; no commands were run.
