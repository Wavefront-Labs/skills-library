---
id: computing-software.cloud-infrastructure-engineering.linkerd.topology-aware-routing-zone-hints
name: topology-aware-routing-zone-hints
category: computing-software
field: cloud-infrastructure-engineering
product: linkerd
tags: [linkerd, topology-aware-routing, zones, endpointslices]
level: advanced
status: docs-checked
description: "Prefer same-zone endpoints by meeting the four requirements for Topology Aware Routing in Linkerd."
sources:
  - https://linkerd.io/2.19/features/topology-aware-routing/
  - https://linkerd.io/2.19/tasks/enabling-topology-aware-routing/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Topology aware routing makes Linkerd prefer endpoints in the client's own zone to cut cross-zone cost and latency. When it is enabled, the destination controller selects endpoints whose `hints.forZones` field matches the client's zone, taken from the node label `topology.kubernetes.io/zone`.

Four requirements:

1. The `TopologyAwareHints` feature gate is enabled on the cluster (default from Kubernetes 1.24).
2. Linkerd's `endpointSlice` feature is on (default since stable-2.12).
3. Every node carries the `topology.kubernetes.io/zone` label.
4. Each relevant Service has the annotation `service.kubernetes.io/topology-aware-hints=auto`.

```bash
kubectl annotate svc/my-service service.kubernetes.io/topology-aware-hints=auto
```

The annotation matters because only the Kubernetes endpoint slice controller sets `forZones`, and only after its own safeguards pass. Linkerd copies the hints from each endpoint slice and filters addresses so a client reaches only endpoints labeled for its zone.

Kubernetes constraints apply. Routing assumes traffic to a zone is roughly proportional to node capacity there, which horizontal pod autoscaling can upset by starting nodes in the wrong zone. Services with `internalTrafficPolicy` set to `Local` ignore topology aware routing, and it does not route to endpoints on Nodes labeled with the control-plane or master role. Review the Kubernetes constraints before enabling it.

## Checked

2026-11-08. Confirmed against: https://linkerd.io/2.19/features/topology-aware-routing/, https://linkerd.io/2.19/tasks/enabling-topology-aware-routing/. Purpose, hints.forZones and zone label matching, the four requirements with defaults, the annotation, endpoint slice controller behaviour, the constraints.

Removed or reworded: Nothing.

Method: documentation only; no commands were run.
