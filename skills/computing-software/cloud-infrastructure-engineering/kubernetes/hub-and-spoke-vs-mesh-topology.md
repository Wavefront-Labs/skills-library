---
id: computing-software.cloud-infrastructure-engineering.kubernetes.hub-and-spoke-vs-mesh-topology
name: hub-and-spoke-vs-mesh-topology
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, multi-cluster, topology, hub-and-spoke, mesh-topology, management-cluster, fleet-design, blast-radius, network-topology, failure-domain, control-plane-architecture]
level: sme
status: docs-checked
description: "Choose between hub-and-spoke and full-mesh multi-cluster topology for control, networking, and failure isolation tradeoffs."
sources: ["https://cluster-api.sigs.k8s.io/user/concepts", "https://istio.io/latest/docs/ops/deployment/deployment-models/", "https://submariner.io/getting-started/", "https://github.com/rancher/fleet"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hub-and-spoke vs mesh: picking a fleet's shape before you build it

**Goal:** decide, before standing up a multi-cluster fleet, whether control and
networking radiate from one hub or connect every cluster to every other cluster. The
choice determines blast radius, operational complexity, and which failures are survivable.
This is a design decision that several other skills implement:
`computing-software.cloud-infrastructure-engineering.kubernetes.cluster-api-fundamentals`
and `computing-software.cloud-infrastructure-engineering.kubernetes.rancher-fleet-management`
are typically hub-and-spoke by construction; `computing-software.cloud-infrastructure-engineering.kubernetes.submariner-multi-cluster-networking`
and `computing-software.cloud-infrastructure-engineering.kubernetes.multi-cluster-service-mesh-federation`
can be wired either way.

## 1. Hub-and-spoke
- One **hub** (management cluster, GitOps control plane, mesh control plane) holds
  state and pushes or pulls config to N **spoke** clusters. Spokes typically do not talk
  directly to each other.
- Examples: a Cluster API management cluster (the Cluster API book defines the management
  cluster as the one that manages workload clusters); a single Fleet or Argo CD instance
  fanning out to many clusters (Fleet describes itself as designed to manage multiple
  clusters); Istio primary-remote or an external control plane, where the control plane
  runs outside the remote clusters that depend on it.
- **Pros:** one place to operate, upgrade, and audit; adding a spoke is cheap; natural
  fit for centralized policy and cost reporting.
- **Cons:** the hub is a single point of control-plane failure. Losing it does not
  necessarily take down spoke workloads (they keep running), but it blocks fleet-wide
  operations (deploys, scaling, healing) until restored. The hub also concentrates blast
  radius: a bad hub config push can touch every spoke simultaneously unless staged rollout
  (canary cluster groups) is deliberately built in.

## 2. Mesh (every cluster talks to every other cluster)
- Each cluster runs its own control plane and establishes direct connectivity and trust
  with every peer it needs, for example Istio multi-primary (every primary cluster has its
  own `istiod` and reads config from its own API server) or Submariner connecting cluster
  pairs through gateway tunnels.
- **Pros:** no single cluster's outage blocks cross-cluster traffic between the
  surviving pair; no central control-plane dependency for data-plane traffic. Istio's
  deployment-models page also lists availability, configuration isolation, controlled
  rollout and selective service visibility as benefits of several control planes.
- **Cons:** pairwise connections grow as n(n-1)/2, so gateway/tunnel config and firewall
  rules multiply quickly as clusters are added; debugging "cluster A can't reach cluster B"
  means checking a specific pairwise link, not one hub; Istio notes that config is
  duplicated across primary clusters, which needs extra steps (often CI/CD automation) to
  roll out changes consistently.

## 3. Deciding factors
- **Fleet size**: a hub scales operationally with the number of spokes by automation
  (Cluster API, Fleet, ApplicationSets); a full mesh multiplies pairwise links, so
  count them for your real fleet size and automate their creation.
- **Blast radius tolerance**: if a tenant's cluster must never be affected by another
  tenant's or the platform's own mistake, avoid a shared hub pushing to both: use separate
  hubs per trust boundary, or apply the reasoning in
  `computing-software.cloud-infrastructure-engineering.kubernetes.cluster-per-tenant-vs-shared-cluster`.
- **Hybrid is common**: a GitOps hub for config delivery (hub-and-spoke) combined with
  mesh-style data-plane connectivity (Submariner or Istio multi-primary) for workloads that
  must call each other directly. These are independent axes, not one choice.
- Submariner uses a **broker** only to exchange connection metadata: the broker is an API
  holding `Cluster` and `Endpoint` objects that member clusters push to and pull from, and
  its docs say it can be a dedicated cluster or one of the connected clusters. Cross-cluster
  traffic runs between the clusters' gateways, not through the broker. Do not confuse "has
  a hub for discovery" with "hub-and-spoke for the data plane."

## Gotchas
- Treating the GitOps hub as if it were HA by default: a single-instance hub is a single
  failure domain, and a region outage that takes it out removes the ability to roll back a
  bad deploy across the whole fleet exactly when you need it most. Deploy and test the hub
  for the availability you need.
- Assuming "mesh" implies no coordination point at all: Istio multi-primary clusters still
  need a shared root of trust and remote-cluster secrets, and Submariner needs its broker.

## Verify
- [ ] The chosen topology's single points of failure are written down and each one's
      blast radius (control vs data plane) is explicit.
- [ ] A simulated hub outage (or, for mesh, a simulated single-cluster outage) is tested
      and its actual blast radius matches what was assumed on paper.
- [ ] Connection and trust count for a mesh topology is sized against the real fleet count,
      not just a pilot of 2-3 clusters.

## Checked
2026-10-27. Documentation: Cluster API book (management cluster concept), Istio docs (deployment models, multicluster before-you-begin; istio.io main, release 1.31.3), Submariner website docs (getting started, architecture; release v0.24.2), Fleet README.
Confirmed: management/workload cluster definition; Istio primary, remote and external control plane definitions and the "each primary reads config from its own API server" text; Istio multicluster trust requirement; Submariner broker contents and role, tunnels between gateways. Scale thresholds were not found in documentation and are not stated.
Method: documentation only; no commands were run.
