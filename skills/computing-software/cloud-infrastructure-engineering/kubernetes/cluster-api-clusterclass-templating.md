---
id: computing-software.cloud-infrastructure-engineering.kubernetes.cluster-api-clusterclass-templating
name: cluster-api-clusterclass-templating
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, cluster-api, capi, clusterclass, templating, patches, variables, multi-cluster, fleet, topology, managed-topology, clusterctl, mutation-webhook]
level: advanced
status: docs-checked
description: "Template a fleet of Cluster API clusters from one ClusterClass with typed variables and JSON patches, instead of copy-pasting per-cluster YAML."
sources: ["https://github.com/kubernetes-sigs/cluster-api/blob/main/docs/book/src/user/guide/configuration/cluster-class/index.md", "https://github.com/kubernetes-sigs/cluster-api/blob/main/docs/book/src/user/guide/configuration/cluster-class/write-clusterclass.md", "https://github.com/kubernetes-sigs/cluster-api/blob/main/docs/book/src/user/guide/configuration/cluster-class/change-clusterclass.md", "https://github.com/kubernetes-sigs/cluster-api/blob/main/docs/book/src/user/guide/configuration/cluster-class/operate-cluster.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ClusterClass: one template, many clusters

**Goal:** define a cluster's shape once (control plane, worker pools, infrastructure templates) and create many clusters from it with small per-cluster variable overrides. Builds on `computing-software.cloud-infrastructure-engineering.kubernetes.cluster-api-fundamentals`.

ClusterClass needs the `ClusterTopology` feature gate (`CLUSTER_TOPOLOGY` variable). The examples use the `v1beta2` API, which is the supported version in the current Cluster API book; `v1beta1` is deprecated (since v1.11, to stop being served in v1.16).

## 1. What ClusterClass replaces
Without it every cluster is a hand-authored tree of `Cluster`, infrastructure cluster, control plane and `MachineDeployment` objects. With a ClusterClass the `Cluster` shrinks to a topology:
```yaml
apiVersion: cluster.x-k8s.io/v1beta2
kind: Cluster
metadata: {name: team-a-prod}
spec:
  topology:
    classRef: {name: generic-cluster-class}
    version: v1.35.0
    controlPlane: {replicas: 3}
    workers:
      machineDeployments:
      - class: default-worker
        name: md-0
        replicas: 5
    variables:
    - name: imageRepository
      value: registry.k8s.io
```

## 2. Variables and patches
- `ClusterClass.spec.variables` declares each variable with `name`, `required` and a `schema.openAPIV3Schema` (a subset of CRD schema: defaults and validation; basic types string, integer, number, boolean plus complex types). A `Cluster` sets values in `spec.topology.variables`.
```yaml
spec:
  variables:
  - name: imageRepository
    required: true
    schema:
      openAPIV3Schema:
        type: string
        default: registry.k8s.io
```
- `ClusterClass.spec.patches` hold named patches. Each definition has a `selector` (apiVersion, kind, `matchResources`) naming the template to patch and `jsonPatches` (JSON patch `op`, `path`, and a `value` or `valueFrom` with `variable` or a Go `template`).
```yaml
  patches:
  - name: imageRepository
    definitions:
    - selector:
        apiVersion: controlplane.cluster.x-k8s.io/v1beta2
        kind: KubeadmControlPlaneTemplate
        matchResources: {controlPlane: true}
      jsonPatches:
      - op: add
        path: /spec/template/spec/kubeadmConfigSpec/clusterConfiguration/imageRepository
        valueFrom: {variable: imageRepository}
```
- Builtin variables such as `builtin.cluster.name`, `builtin.controlPlane.version` and `builtin.machineDeployment.class` can be used in patches; in Go templates paths start with a dot (`.builtin.machineDeployment.version`).
- A patch can be conditional with `enabledIf`, which is a Go template that must evaluate to `true` (for example `"{{ if .httpProxy }}true{{end}}"`), so one class can serve differently shaped clusters.
- Logic beyond templates and JSON patches can be implemented with a Runtime Extension topology mutation hook (see the Cluster API Runtime Extensions docs).

## 3. Rollout and change propagation
- There are two strategies. The recommended one for beginners is to create a new ClusterClass with the change and rebase clusters one at a time by changing `spec.topology.classRef.name` (a canary-like rollout). The alternative is changing the ClusterClass in place, which propagates immediately to every Cluster using it and can trigger machine rollouts across the whole fleet.
- For templates the recommended way is rotation: create a new template, update the reference in the ClusterClass, delete the old one. In-place template mutations are only picked up at the next full reconciliation (up to the controller sync period, 10 minutes by default).
- Do not reuse a template across ClusterClasses; prefix templates with the ClusterClass name.
- Plan changes before applying them and understand the compatibility checks, which block changes that would produce non-functional Clusters.
- Make changes through `Cluster.spec.topology` (for example `kubectl patch cluster <name> --type json --patch '[{"op":"replace","path":"/spec/topology/version","value":"v1.36.0"}]'`). The topology controller reconciles the underlying objects to the desired state immediately, so avoid concurrent changes (a version change plus other worker changes can cause a double rollout).
- A Kubernetes version upgrade in a topology cannot skip a minor version (+2 minor is not allowed).
- When upgrading Cluster API itself, upgrade Cluster API first and then bump apiVersions referenced in the ClusterClass.

## Gotchas
- JSON patch paths depend on the template's structure; check with the planning step after provider upgrades.
- A forgotten `enabledIf` applies the patch to every cluster.
- If a MachineHealthCheck is defined by the ClusterClass, direct edits to the generated MachineHealthCheck are overridden; override it through `healthCheck` in `Cluster.spec.topology`.

## Verify
- [ ] `clusterctl describe cluster <name>` shows the expected resolved control plane and worker setup for a small and a large instance of the same class.
- [ ] A variable override changes the generated infrastructure machine template as expected.
- [ ] A patch gated by `enabledIf` is absent when the condition is false.
- [ ] After rebasing one cluster to a new class, the others are unchanged.

## Checked

Checked 2026-10-26 against Cluster API book (main branch, latest commit 2026-10-22; latest release v1.14.3). Confirmed: v1beta2 Cluster topology and ClusterClass variable and patch syntax, enabledIf as a Go template, change strategies (new class plus rebase versus in-place), template rotation, +2 minor upgrade rule.

Method: documentation only; no commands were run.
