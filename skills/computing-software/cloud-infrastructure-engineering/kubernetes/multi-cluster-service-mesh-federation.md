---
id: computing-software.cloud-infrastructure-engineering.kubernetes.multi-cluster-service-mesh-federation
name: multi-cluster-service-mesh-federation
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, istio, service-mesh, multi-cluster, multi-primary, multi-network, east-west-gateway, mtls, spiffe, trust-domain, locality-load-balancing, failover, mesh-federation]
level: sme
status: docs-checked
description: "Federate a service mesh (Istio multi-primary/multi-network) across clusters for cross-cluster mTLS, failover, and traffic splitting."
sources: ["https://istio.io/latest/docs/ops/deployment/deployment-models/", "https://istio.io/latest/docs/setup/install/multicluster/", "https://istio.io/latest/docs/setup/install/multicluster/before-you-begin/", "https://istio.io/latest/docs/tasks/traffic-management/locality-load-balancing/", "https://istio.io/latest/docs/releases/supported-releases/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multi-cluster service mesh: shared identity and traffic policy, not just connectivity

**Goal:** go beyond raw cross-cluster IP reachability
(`computing-software.cloud-infrastructure-engineering.kubernetes.submariner-multi-cluster-networking`)
to get mesh-level mTLS identity, locality-aware load balancing, and traffic
splitting/failover that treats services across clusters as one logical mesh. This is a
different layer than Submariner: a mesh can federate across clusters using only
gateway-routed traffic (no flat pod network needed) or can be combined with a flat pod
network for direct pod routing: know which you actually have.

## 1. Istio's multi-cluster deployment models
Istio's install guides cover four combinations of control plane model and network model:
multi-primary or primary-remote, each on one network or on different networks.
- **Multi-primary, single network**: every cluster runs its own `istiod`; all clusters
  share one routable pod network. Istio requires non-overlapping pod and service CIDRs and
  working cross-cluster routing for this, and needs no east-west gateway.
- **Multi-primary, different networks**: separate pod networks per cluster; cross-network
  traffic goes through an **east-west gateway** in each cluster. Clusters are labelled with
  `topology.istio.io/network`, and Istio's samples generate the gateway
  (`gen-eastwest-gateway.sh`) and expose services through it (`expose-services.yaml`).
- **Primary-remote**: a primary cluster runs `istiod`; remote clusters have no control
  plane of their own and reach it (through an Istio gateway when they are on different
  networks). That gives a hub-and-spoke control dependency
  (`computing-software.cloud-infrastructure-engineering.kubernetes.hub-and-spoke-vs-mesh-topology`
  applies here too). An **external control plane** (for example a cloud vendor's managed
  control plane) is a related option where every cluster is remote.
- In multi-primary meshes each primary reads configuration from its own cluster's API
  server, so config must be rolled out to each cluster (Istio suggests CI/CD tooling).
- Every cluster's API server must be reachable by the other clusters' `istiod`.

## 2. What federation actually buys you
- **Shared trust**: a multicluster mesh requires trust between all clusters; Istio's guide
  uses a common root CA with an intermediate CA per cluster. mTLS and `AuthorizationPolicy`
  can then treat a service in cluster B calling a service in cluster A like an in-cluster
  call.
- **Locality-aware load balancing**: Istio's default mesh config enables locality load
  balancing and uses the node labels `topology.kubernetes.io/region` and
  `topology.kubernetes.io/zone` (plus the Istio-specific `topology.istio.io/subzone`).
  Locality-aware **failover** is activated by configuring `OutlierDetection` in a
  `DestinationRule`, because Envoy relies on outlier detection to find unhealthy endpoints.
  Without it, traffic is not failed over automatically.
- **Traffic splitting/canary across clusters**: a `VirtualService`/`DestinationRule` pair
  can send a share of traffic to a version deployed in only one cluster.
- Across networks Istio supports only workloads that have an Istio proxy: the gateway passes
  TLS through so mTLS terminates at the workload, and endpoints without a proxy are
  filtered out.

## 3. Setup essentials
- Establish trust before installing: the multicluster guide's flow creates a root CA and
  intermediate CA certificates per cluster and installs them as a secret in each cluster.
  Skipping this means cross-cluster calls fail at the TLS handshake, not at an obviously
  mesh-related layer.
- East-west gateways need their own Service (usually a cloud load balancer) reachable
  from the other clusters.
- Register clusters with each other using `istioctl create-remote-secret`, which creates a
  secret holding a kubeconfig for that cluster so each `istiod` can discover the other's
  endpoints.

## Gotchas
- A root CA mismatch between clusters is a classic federation failure: "service
  unreachable cross-cluster" that is really a TLS trust failure, visible in sidecar and
  `istiod` logs rather than in the calling application. `istioctl proxy-config
  rootca-compare <pod-1> <pod-2>` compares the root CAs two workloads trust.
- Locality load balancing needs correct region/zone labels on nodes (and `OutlierDetection`
  for failover); wrong or missing labels give suboptimal routing with no error.
- Version skew: Istio's support policy says the control plane can be one version ahead of
  the data plane, never behind. Plan per-cluster upgrades with revisions so there is no
  skew (see the service mesh upgrade skill).
- Combining a mesh with a separate flat-network tool (for example Submariner): decide which
  network model Istio sees and label networks accordingly; do not leave two layers
  providing overlapping cross-cluster routing.

## Verify
- [ ] Cross-cluster mTLS: a call from a cluster-B workload to a cluster-A service
      authenticates with a valid SPIFFE identity under the shared trust domain
      (checked via `istioctl proxy-config` or mesh logs, not just "it worked").
- [ ] Killing all endpoints of a service in its local cluster causes locality-aware
      failover to the other cluster's endpoints within the expected time (with
      `OutlierDetection` configured).
- [ ] A traffic-split rule routes the configured percentage to a cross-cluster
      destination, confirmed by request tracing, not estimated from aggregate metrics.
- [ ] Root CA chain and cluster registration are documented and reproducible (not a
      one-off manual `istioctl` run with no record of the exact commands used).

## Checked
2026-10-27. Documentation releases: istio.io docs (main) and Istio 1.31.3 release tree (istioctl source, supported releases page).
Confirmed: the four install combinations and their prerequisites (CIDRs, east-west gateway, network label, sample scripts), primary-remote and external control plane definitions, per-primary configuration source, trust setup, `istioctl create-remote-secret`, locality labels and the OutlierDetection requirement for failover, cross-network proxy-only support, control plane/data plane skew rule.
Method: documentation only; no commands were run.
