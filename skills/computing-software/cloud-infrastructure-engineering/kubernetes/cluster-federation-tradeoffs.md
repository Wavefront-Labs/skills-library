---
id: computing-software.cloud-infrastructure-engineering.kubernetes.cluster-federation-tradeoffs
name: cluster-federation-tradeoffs
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, kubefed, federation-v2, admiralty, multi-cluster, cluster-federation, gitops, applicationset, fleet, deprecated, history]
level: sme
status: docs-checked
description: "Weigh Kubernetes cluster federation (KubeFed, Karmada, Admiralty) against GitOps fleet patterns, and why KubeFed (federation v2) was archived."
sources: ["https://github.com/kubernetes-retired/kubefed", "https://github.com/kubernetes-retired/kubefed/blob/master/docs/userguide.md", "https://github.com/karmada-io/karmada", "https://github.com/admiraltyio/admiralty/blob/master/docs/introduction.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cluster federation — why KubeFed lost to GitOps fleets

**Goal:** know what "federation" meant in Kubernetes (a single API that fans
resource-creation out to member clusters) and why almost no one runs it today in favor
of `computing-software.cloud-infrastructure-engineering.kubernetes.fleet-gitops-argocd-applicationsets`
or `computing-software.cloud-infrastructure-engineering.kubernetes.rancher-fleet-management`
— so you don't propose reviving it without knowing why it was abandoned.

## 1. What KubeFed (Federation v2) tried to do
- A `FederatedDeployment`/`FederatedConfigMap` etc. resource (API group `types.kubefed.io`,
  version `v1beta1`), applied once to a **host cluster**, that KubeFed's controller propagated
  to registered **member clusters**, optionally with per-cluster `overrides` (JSON-patch style
  `clusterOverrides` such as replica counts or image tags) in the federated resource's spec.
  Each federated type had to be enabled first (`kubefedctl enable <type>`), which created its
  `FederatedTypeConfig`.
- This is architecturally a hub-and-spoke push model, same shape as what Fleet/
  ApplicationSets do today — the idea was sound, the specific implementation wasn't.

## 2. Why it stalled
- **Federation v1** was retired (its repository now lives under `kubernetes-retired`).
- **Federation v2 / KubeFed** (SIG Multicluster) required wrapping every resource type
  you wanted federated in its own `Federated<Kind>` CRD and a `FederatedTypeConfig` —
  this meant it only worked well for types someone had explicitly wired up, and each
  new CRD you wanted to federate (common once Operators got popular) needed its own
  federation plumbing.
- Its API stayed at `v1beta1`, and the KubeFed repository is archived and moved to
  `kubernetes-retired/kubefed`
  ("no longer active development"; SIG Multicluster points to its current subprojects).
  Meanwhile GitOps tooling (Argo CD, Flux, Fleet) solved the same "same config, many
  clusters" problem using **plain
  Kubernetes manifests plus a generator/templating layer**, with no new CRD type needed
  per resource kind, and with Git as the audit trail KubeFed never had built in.
- GitOps fleet tools also compose better with existing tooling: an ApplicationSet or
  Fleet Bundle deploys literally anything renderable as YAML/Helm/Kustomize; KubeFed
  could only propagate types it had a `Federated` wrapper for.

## 3. What's left standing in this space
- **Admiralty** — a narrower project for multi-cluster **pod scheduling**: pods labelled
  for election become proxy pods on virtual-kubelet nodes that represent target clusters,
  and delegate pods run the containers remotely. Use cases it lists include cloud bursting.
  Its latest release is v0.17.0 (November 2024); check activity before adopting.
- **Karmada** — a CNCF graduated project that describes itself as a continuation of
  Federation v1 and v2. It speaks Kubernetes-native APIs (no `Federated<Kind>` wrappers) and
  adds multi-cluster scheduling policies (cluster affinity, splitting and rebalancing,
  failover), which plain GitOps fleets don't do.
- For "same config everywhere," GitOps fleet tooling is the common answer today.

## When federation-style thinking still applies
- If the actual need is **workload placement/scheduling across clusters** (not just
  config propagation), that's a different problem than any tool in this list solves
  well — most fleets instead run independent schedulers per cluster and route traffic
  with `computing-software.cloud-infrastructure-engineering.kubernetes.multi-cluster-ingress-and-global-load-balancing`
  rather than scheduling pods across cluster boundaries.
- If someone proposes "let's federate," ask whether they mean config propagation
  (GitOps fleet solves it, already built, already battle-tested) or cross-cluster
  scheduling (Karmada or Admiralty; confirm it's really needed).

## Gotchas
- Don't inherit legacy `FederatedDeployment` CRDs/controllers from an old cluster
  without a plan — they're unmaintained; migrate the same config to an ApplicationSet
  or Fleet Bundle instead of patching a dead project.
- "Federation" as a word is used loosely in multi-cluster marketing material for
  anything from KubeFed-style propagation to Istio's mesh federation
  (`computing-software.cloud-infrastructure-engineering.kubernetes.multi-cluster-service-mesh-federation`,
  a networking/identity concept, not a config-propagation one) — confirm which meaning
  is meant before reusing the word in a design doc.

## Verify
- [ ] No `kubefed`/`FederatedTypeConfig` resources remain in any cluster inherited from
      a legacy setup (`kubectl get crd | grep federation` across the fleet).
- [ ] The actual requirement ("same config everywhere" vs "schedule workload anywhere")
      is named explicitly before picking a tool, so GitOps fleet tooling isn't ruled
      out for a problem it already solves.

## Checked
2026-10-27 against the KubeFed README and user guide (repository archived and now at
kubernetes-retired/kubefed, last
push March 2023), the karmada-io/karmada README and the admiraltyio/admiralty introduction and
release list. Confirmed: the archive notice, the `types.kubefed.io/v1beta1` federated types,
`kubefedctl enable`, where `overrides` live, Karmada's CNCF graduated status and lineage, and how
Admiralty's proxy and delegate pods work. Fixed: overrides were attributed to
`FederatedTypeConfig`; "Karmar" was Karmada and was described as immature; Admiralty was called
still maintained; prose source titles replaced with URLs.
Method: documentation only; no commands were run.
