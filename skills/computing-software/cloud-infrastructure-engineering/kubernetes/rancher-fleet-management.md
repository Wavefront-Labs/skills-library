---
id: computing-software.cloud-infrastructure-engineering.kubernetes.rancher-fleet-management
name: rancher-fleet-management
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, rancher, fleet, gitrepo, bundle, gitops, multi-cluster, fleet-agent, cluster-group, targeting, helm, kustomize, fleet-summary]
level: advanced
status: docs-checked
description: "Manage GitOps delivery to a large cluster fleet with Rancher Fleet: GitRepo, Bundle, and targeting by cluster labels."
sources: ["https://fleet.rancher.io/architecture", "https://fleet.rancher.io/gitrepo-targets", "https://fleet.rancher.io/ref-fleet-yaml", "https://fleet.rancher.io/rollout"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rancher Fleet — GitOps to thousands of clusters without per-cluster Argo CD agents

**Goal:** deploy manifests from Git to a large, heterogeneous fleet (bare-metal, edge,
cloud) where running a full Argo CD instance per cluster or a huge pull-based agent
footprint isn't practical. Fleet is built for scale-to-thousands with a lightweight
per-cluster agent; compare against `computing-software.cloud-infrastructure-engineering.kubernetes.fleet-gitops-argocd-applicationsets`
when choosing a GitOps engine — don't run both against the same fleet.

## 1. Architecture
- **Fleet manager** runs on one cluster (often the Rancher management cluster) and
  watches `GitRepo` resources.
- Each **downstream cluster** runs one cluster agent. Fleet uses a two-stage pull model: the controller
  pulls from Git and the agents pull from the controller. All communication goes from the managed
  cluster to the Fleet controller, so the controller never initiates a connection to a cluster.
- A `GitRepo` points at a repo/path/branch and fans out into one `Bundle` per matching
  target; the agent on each targeted cluster pulls and applies its Bundle.

## 2. Targeting
```yaml
apiVersion: fleet.cattle.io/v1alpha1
kind: GitRepo
metadata: {name: platform-base, namespace: fleet-default}
spec:
  repo: https://git.example.com/platform.git
  branch: main
  paths: ["base"]
  targets:
  - name: prod
    clusterSelector: {matchLabels: {env: prod}}
  - name: staging
    clusterSelector: {matchLabels: {env: staging}}
```
- Clusters and cluster groups in the same namespace as the `GitRepo` are evaluated against its targets.
  `clusterSelector`, `clusterGroupSelector` and `clusterGroup` are combined with AND; a criterion
  left at its default (null or empty string) is dropped.
- `fleet.yaml` in the repo path configures how the content is deployed: raw manifests, a Kustomize
  overlay (`kustomize.dir`) or a Helm chart (`helm` options such as `valuesFiles`); `targetCustomizations`
  override the root-level `helm`/`kustomize` options for matched targets.

## 3. Status and drift
- `kubectl get gitrepo -n fleet-default` and the Rancher UI show Bundle and BundleDeployment state; the
  `Ready` condition is true only if all BundleDeployments are ready, and status messages list states
  such as `WaitApplied` per cluster.
- Drift correction is **not** on by default: `correctDrift.enabled` defaults to `false` in `fleet.yaml`.
  Enable it (optionally with `force`, which can recreate resources) if you want manual changes reverted.

## Gotchas
- `clusterSelector: {}` matches **all** clusters (the docs say `{}` means "match everything"; `null` is
  ignored), a common accidental-blast-radius mistake when copying a target block.
- Fleet has its own rollout control: `rolloutStrategy` in `fleet.yaml` (`maxUnavailable` default 100%,
  `maxUnavailablePartitions`, manual or automatic partitions). Fleet deploys in batches of up to 50
  clusters per partition and checks `maxUnavailable` between batches. Partitions only group and gate
  the rollout; they do not change deployment options.

## Verify
- [ ] `kubectl get gitrepo,bundle -n fleet-default` shows `Ready` for every cluster the
      target selector should match, and correctly excludes clusters it shouldn't.
- [ ] A `targetCustomizations` override (different Helm value per cluster group) is
      confirmed applied via the actual resource on two different clusters.
- [ ] If `correctDrift` is enabled, a manually edited resource on a downstream cluster is reverted.

## Checked

2026-10-26, against Fleet docs in rancher/fleet-docs (archived 2026-03-24; its README says documentation moved to rancher/fleet-product-docs; docs cover Fleet up to 0.14). Confirmed: pull architecture, `fleet.cattle.io/v1alpha1` GitRepo, target matching rules and `{}` semantics, `fleet.yaml` keys (`kustomize`, `helm`, `targetCustomizations`, `correctDrift`, `rolloutStrategy`), rollout batch size and `maxUnavailable` default, Ready condition. Wrong: drift correction was described as default (it defaults to off) and Fleet was said to lack progressive rollout (it has `rolloutStrategy` partitions). Removed unconfirmed manager sizing, empty-bundle on path typo and Argo CD comparison claims. The docs read are an archived snapshot; verify against the current Fleet product docs for versions after 0.14.

Method: documentation only; no commands were run.
