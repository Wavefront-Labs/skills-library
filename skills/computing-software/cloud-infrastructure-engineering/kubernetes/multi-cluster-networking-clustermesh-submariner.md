---
id: computing-software.cloud-infrastructure-engineering.kubernetes.multi-cluster-networking-clustermesh-submariner
name: multi-cluster-networking-clustermesh-submariner
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, multi-cluster, clustermesh, cilium, submariner, service-mirroring, cross-cluster, global-service, networking, vpn, wireguard, clusterset-local]
level: advanced
status: docs-checked
description: "Connect pod networks across clusters for service discovery: Cilium ClusterMesh's flat-network model vs Submariner's gateway tunnels and broker, and what breaks each."
sources: ["https://docs.cilium.io/en/stable/network/clustermesh/", "https://docs.cilium.io/en/stable/network/clustermesh/setup/", "https://docs.cilium.io/en/stable/network/clustermesh/global-services/", "https://submariner.io/getting-started/", "https://submariner.io/getting-started/architecture/gateway-engine/", "https://github.com/kubernetes/enhancements/tree/master/keps/sig-multicluster/1645-multi-cluster-services-api"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Multi-cluster networking: ClusterMesh, Submariner, and the CIDR problem underneath both

**Goal:** let pods/Services in one cluster reach another cluster's pods/Services directly,
and understand the one prerequisite every approach shares: non-overlapping pod CIDRs
(and, for Submariner, Service CIDRs).

## 1. The prerequisite nobody can skip: non-overlapping CIDRs
- Cilium ClusterMesh requires the PodCIDR ranges of all clusters and all nodes to be
  non-conflicting, unique IP addresses.
- Submariner requires non-overlapping Pod and Service CIDRs between clusters, unless you
  deploy its **Globalnet** component (section 3).
Two clusters both defaulted to `10.244.0.0/16` therefore cannot be joined without
re-addressing one of them (or Globalnet on Submariner). Check this before evaluating
tooling; it is usually the actual blocker on a "let's connect our clusters" project.

## 2. Cilium ClusterMesh: flat network, shared identity
- Requires Cilium as the CNI in every member cluster, the same datapath mode (overlay or
  native routing) in all of them, Cilium versions that differ by at most one minor
  release, and a unique cluster `name` and numeric `id` per cluster. The default limit is
  255 connected clusters (`maxConnectedClusters` can raise it to 511 at the cost of fewer
  cluster-local identities).
- Architecture: each cluster runs `clustermesh-apiserver` pods (an embedded etcd that
  exposes local cluster state to remote clusters over mTLS, an `apiserver` container that
  syncs local state into it, and `kvstoremesh`, which copies remote cluster state into
  the local cluster). Pod-to-pod traffic is then forwarded directly between nodes, with no
  proxy or gateway.
- ClusterMesh does the control-plane sync, **not** the L3 connectivity: nodes must reach each
  other on their InternalIPs (typically via peering or VPN), the firewall must allow the
  inter-cluster ports, and in native-routing mode the native routing CIDR must cover all
  clusters' PodCIDRs and pods must reach each other on all ports.
- **Global Services**: annotate a Service `service.cilium.io/global: "true"` in each
  cluster with the same name and namespace and its backends are load-balanced across
  clusters. This implicitly sets `service.cilium.io/shared: "true"`; set it to `"false"` to
  stop sharing a cluster's backends. `service.cilium.io/affinity: "local"`, `"remote"` or
  `"none"` states which backends are preferred: with `local`, remote backends are used only
  if no local backend is healthy; the docs' starting point is load-balancing across all
  clusters, which "might not be ideal in some cases". Cilium also supports the Multi-Cluster Services API
  (`ServiceExport`/`ServiceImport`) with `clustermesh.mcsapi.enabled=true`.
- Identities are shared across clusters, so `CiliumNetworkPolicy` can select endpoints by
  cluster using the `io.cilium.k8s.policy.cluster` label. Since Cilium 1.19 a policy selects
  endpoints of the local cluster only unless clusters are targeted explicitly, and policies
  are not distributed automatically: apply them in every cluster.
- All clusters in a mesh form a single trust domain; Cilium advises connecting only
  mutually trusted clusters with equivalent security posture.

## 3. Submariner: gateway tunnels and a broker
- Components: a **broker** (an API reachable by every cluster, holding `Cluster` and
  `Endpoint` objects; it can be a dedicated cluster or one of the members), a **Gateway
  Engine** on gateway nodes (DaemonSet on nodes labelled `submariner.io/gateway=true`) that
  builds tunnels to the other clusters, and Lighthouse for service discovery.
- Tunnel drivers: IPsec via Libreswan (the current default), WireGuard (installed on the
  gateway nodes), or unencrypted VXLAN (for example over an already-secured peering link);
  chosen with `subctl join --cable-driver`.
- Gateways need IP reachability to each other: default encapsulation UDP 4500, NAT-T
  discovery UDP 4490, UDP 4800 for pod traffic from nodes to the gateway (not needed with
  OVN-Kubernetes), and ESP when gateways are directly reachable without NAT.
- Supported CNIs listed in the docs: OpenShift-SDN, Weave, Flannel, Canal, Calico and OVN
  (Cilium is not in that list).
- **ServiceExport/ServiceImport** (the Multi-Cluster Services API, KEP-1645): a Service
  with a `ServiceExport` in cluster A resolves from other clusters as
  `<svc>.<ns>.svc.clusterset.local`. Nothing is exported by default. When a Service
  exists in several clusters Lighthouse DNS prefers the local cluster first, then remote
  clusters round-robin.
- **Globalnet** (enabled at broker deployment with `subctl deploy-broker --globalnet`, off
  by default) gives each cluster a slice of a global CIDR (default `242.0.0.0/8`) and NATs
  cross-cluster traffic, so clusters with overlapping Pod/Service CIDRs can connect.
  Remote clusters then see global IPs rather than real pod IPs.
- Gateway HA is active/passive: several gateway nodes elect one active instance, the rest
  stand by. A cluster with a single gateway node loses all cross-cluster traffic if it
  fails.
- Service discovery needs Kubernetes 1.21 or later.

## 4. Choosing between them
| Situation | Pick |
|---|---|
| All clusters already run Cilium, node and pod networks can be peered or routed | ClusterMesh (shared identity and policy, direct pod-to-pod, no gateway hop) |
| A supported non-Cilium CNI, or clusters you can only link through gateway nodes | Submariner |
| Overlapping Pod/Service CIDRs that cannot be changed | Submariner with Globalnet |
| Only a handful of specific Services exposed | Submariner's per-Service export (or MCS-API on ClusterMesh) |

## 5. Common failure modes
- **CIDR overlap discovered mid-rollout**: the #1 blocker; audit this first, always.
- **Firewall and reachability gaps**: wrong ports between gateways (Submariner) or no
  InternalIP/native-routing path between nodes (ClusterMesh) look like silent
  cross-cluster failures.
- **Expired inter-cluster certificates** (ClusterMesh uses mTLS between clusters): monitor
  certificate expiry as its own signal.
- **Policy assumptions**: a policy written for same-cluster selectors does not apply
  remotely; test cross-cluster identity selection (ClusterMesh) and remember Globalnet
  hides real pod IPs from IP-based allow-lists.

## Debug routine
```bash
# Cilium ClusterMesh
cilium clustermesh status
kubectl -n kube-system exec ds/cilium -- cilium-dbg service list   # look for cross-cluster backends
# Submariner
subctl show connections
subctl show gateways
subctl diagnose all
```

## Verify
- [ ] Pod CIDRs (and for Submariner, Service CIDRs) confirmed non-overlapping across every
  member cluster before any mesh/tunnel was configured, or Globalnet was chosen deliberately.
- [ ] A cross-cluster Service resolves and load-balances to the remote cluster's pods, tested
  with the local cluster's pods scaled to zero (forces the spillover path).
- [ ] Certificate expiry and gateway HA have their own alerts, independent of application
  error rates.
- [ ] Cross-cluster policy (if any) was tested with a deliberately denied case, not just the
  allowed case.

## Checked
2026-10-27. Documentation releases: Cilium v1.20.4 (ClusterMesh intro, setup, global services, affinity, policy, MCS-API pages), Submariner website docs (main; latest release v0.24.2).
Confirmed: ClusterMesh prerequisites, architecture, scaling limit, annotations and affinity semantics, policy default change; Submariner broker/gateway/cable-driver/port details, supported CNI list, Globalnet and Lighthouse behaviour, `subctl` commands.
Method: documentation only; no commands were run.
