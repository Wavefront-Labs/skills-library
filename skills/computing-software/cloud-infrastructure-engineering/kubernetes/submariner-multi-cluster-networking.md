---
id: computing-software.cloud-infrastructure-engineering.kubernetes.submariner-multi-cluster-networking
name: submariner-multi-cluster-networking
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, submariner, multi-cluster-networking, broker, gateway, service-discovery, serviceexport, serviceimport, mcs-api, cidr-overlap, ipsec, vxlan, globalnet]
level: advanced
status: docs-checked
description: "Connect pod and service networks across separate Kubernetes clusters with Submariner (broker, gateway tunnels, Lighthouse, Globalnet) for direct cross-cluster traffic."
sources: ["https://submariner.io/getting-started/", "https://submariner.io/getting-started/architecture/gateway-engine/", "https://submariner.io/getting-started/architecture/globalnet/", "https://submariner.io/getting-started/architecture/service-discovery/", "https://submariner.io/operations/deployment/subctl/", "https://github.com/kubernetes/enhancements/tree/master/keps/sig-multicluster/1645-multi-cluster-services-api"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Submariner: pod/service networking across cluster boundaries

**Goal:** let a pod in cluster A call a Service in cluster B by (roughly) the same
Service DNS mechanics it would use in-cluster, without going through external
ingress/load balancers. Contrast with
`computing-software.cloud-infrastructure-engineering.kubernetes.multi-cluster-ingress-and-global-load-balancing`,
which solves north-south (external client) routing, not pod-to-pod.

## 1. Architecture
- The **Broker** is an API that every participating cluster can reach. Clusters exchange two
  CRD-backed objects through it: `Cluster` (a participating cluster and its CIDRs) and
  `Endpoint` (a connection endpoint and the cluster IPs reachable from it). It must be
  deployed on a single Kubernetes cluster whose API server all member clusters can reach; it
  can be a dedicated cluster or one of the connected ones. Tunnels run between the clusters'
  gateways, not through the broker (same nuance as in
  `computing-software.cloud-infrastructure-engineering.kubernetes.hub-and-spoke-vs-mesh-topology`).
- The **Gateway Engine** runs as a DaemonSet on nodes labelled `submariner.io/gateway=true`
  and builds secure tunnels to other clusters. Cable drivers: IPsec via Libreswan (the
  current default), WireGuard (installed on the gateway nodes) and unencrypted VXLAN
  (for networks that are already trusted or peered). Select it with
  `subctl join --cable-driver`.
- Gateway HA is **active/passive**: several gateway nodes can be labelled, they elect one
  active instance, and the others take over if it fails. Each additional cluster adds tunnels
  between gateways, so the number of pairwise connections grows with cluster count.
- **Service discovery (Lighthouse)** implements the Kubernetes Multi-Cluster Services API
  (KEP-1645). For each Service with a `ServiceExport`, the Lighthouse agent creates
  `ServiceImport` and `EndpointSlice` objects and shares them through the broker; the
  Lighthouse DNS server owns `clusterset.local`, so the Service resolves as
  `<svc>.<ns>.svc.clusterset.local`. If a Service exists in several clusters, the local
  cluster is preferred, then remote clusters in round-robin. Service discovery requires
  Kubernetes 1.21 or later.

## 2. CIDR overlap: the thing that breaks first
- By default Submariner requires **non-overlapping Pod and Service CIDRs** across clusters
  (worker node IPs must also be outside the Pod/Service ranges). Most clusters are created
  with default CIDRs, so a second cluster often collides. Submariner's docs note that
  changing CIDRs on existing clusters is very disruptive and needs a cluster restart.
- **Globalnet** supports overlapping CIDRs. It is enabled at broker deployment
  (`subctl deploy-broker --globalnet`, disabled by default), gives each cluster a slice of
  a virtual global CIDR (default supernet `242.0.0.0/8`, tunable with
  `--globalnet-cidr-range`), and uses global egress IPs (`ClusterGlobalEgressIP` per
  cluster, `GlobalEgressIP` per namespace or pods) and global ingress IPs for exported
  Services. The cost is another NAT layer to debug.
- Decide on Globalnet before you join clusters to the broker.

## 3. Operational notes
- `subctl diagnose all` runs diagnostics (including firewall checks); `subctl show
  connections|gateways|endpoints|networks|versions|all` summarize state.
- Gateway nodes need IP reachability to each other: default encapsulation port 4500/UDP
  (NAT-T discovery 4490/UDP, custom ports such as 4501/UDP are supported), 4800/UDP for
  pod traffic from nodes to the gateway (not needed with OVN-Kubernetes), and the ESP
  protocol when gateways are directly reachable without NAT.
- Tested CNIs listed in the docs: OpenShift-SDN, Weave, Flannel, Canal, Calico (with
  Calico-specific deployment steps) and OVN.
- Cross-cluster calls take real inter-cluster network latency; design for it.

## Gotchas
- A `ServiceExport` must be created per Service per cluster: nothing is cross-cluster
  visible by default, so a forgotten export looks like "the service doesn't exist".
- With Globalnet, remote clusters see global IPs rather than the real pod IPs, which breaks
  IP-based allow-lists and dashboards that assumed real cluster IPs.
- A cluster with a single gateway node loses all cross-cluster traffic if it fails; label
  more than one gateway where cross-cluster calls matter.
- A service mesh that provides its own cross-cluster routing (for example Istio
  multi-network, see
  `computing-software.cloud-infrastructure-engineering.kubernetes.multi-cluster-service-mesh-federation`)
  is a second cross-cluster layer: decide which layer owns routing and trust.

## Verify
- [ ] `subctl diagnose all` reports no CIDR overlap or connectivity errors across all
      joined clusters.
- [ ] A test pod in cluster A resolves and calls an exported Service in cluster B via
      `<svc>.<ns>.svc.clusterset.local`.
- [ ] Stopping the active gateway node (with several labelled gateways) fails over without
      dropping cross-cluster traffic longer than the expected failover window.
- [ ] CIDR planning (or Globalnet) was decided and documented before any production
      cluster was joined to the broker.

## Checked
2026-10-27. Documentation releases: Submariner website docs (main; latest release v0.24.2): getting started, gateway engine, Globalnet, service discovery, subctl and troubleshooting pages.
Confirmed: broker contents and placement, gateway DaemonSet label, cable drivers and default, active/passive HA, Lighthouse/MCS-API behaviour and local-first preference, prerequisites (CIDRs, ports, Kubernetes 1.21), Globalnet defaults and resources, `subctl` commands, tested CNI list.
Method: documentation only; no commands were run.
