---
id: computing-software.cloud-infrastructure-engineering.kubernetes.hierarchical-namespace-controller
name: hierarchical-namespace-controller
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, hnc, hierarchical-namespace-controller, hierarchical-namespaces, subnamespace, multi-tenancy, self-service, rbac-propagation, policy-inheritance, delegated-admin]
level: advanced
status: docs-checked
description: "Manage nested, self-service namespace hierarchies with HNC: subnamespace anchors, propagated RBAC, tree labels, cascading deletion guard and project status."
sources: ["https://github.com/kubernetes-sigs/hierarchical-namespaces", "https://github.com/kubernetes-sigs/hierarchical-namespaces/blob/master/docs/user-guide/concepts.md", "https://github.com/kubernetes-sigs/hierarchical-namespaces/blob/master/docs/user-guide/how-to.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hierarchical Namespace Controller — self-service namespaces without handing out cluster-admin

**Goal:** let a team lead create sub-namespaces for their own sub-teams/projects
without a platform-admin ticket, while RBAC, NetworkPolicy, ResourceQuota and labels
set on the parent automatically propagate down — a middle ground between "every
namespace is hand-provisioned by platform" and "give teams a ClusterRole that can
create cluster-scoped Namespaces" (the latter is a blast-radius problem: Namespace is
cluster-scoped, so that permission isn't containable to one team's area without HNC).

## 1. Core objects
- **SubnamespaceAnchor**: created *inside* a parent namespace to request a
  child; the child `Namespace` is created by the HNC controller, not directly by the
  user — this is the trick that lets a namespaced RBAC role (create anchors in namespace X)
  stand in for a cluster-scoped "create Namespace" permission.
```yaml
apiVersion: hnc.x-k8s.io/v1alpha2
kind: SubnamespaceAnchor
metadata: {name: team-a-dev, namespace: team-a}
```
creates child namespace `team-a-dev` under parent `team-a`.
- **HNCConfiguration**: cluster-scoped object declaring which resource types
  **propagate** down the tree (RBAC `Role`/`RoleBinding` only by default, enforced in
  `Propagate` mode; any other kind, including custom resources, can be added) and in which
  synchronization mode: `Propagate`, `AllowPropagate`, `Remove` or `Ignore`.
- Tree labels of the form `<ancestor>.tree.hnc.x-k8s.io/depth` are applied to every namespace
  in a subtree — useful as `NetworkPolicy` selectors that should apply to
  "this team and everything under it."

## 2. What propagates and what doesn't
- RBAC objects set on a parent namespace propagate to every descendant automatically —
  grant a team lead `edit` on the parent, every sub-namespace they create inherits it,
  no re-granting per child.
- Only RBAC objects propagate by default; a `ResourceQuota` propagated to every child gives each
  child its own full quota. HNC has a separate **HierarchicalResourceQuota** (HRQ) so the sum of
  a subtree's usage is capped by the parent's quota (beta in HNC v1.1; not included by default,
  install `hrq.yaml` from the release assets).
- Deleting a namespace whose deletion would also delete subnamespaces is **blocked** by an HNC
  webhook unless `allowCascadingDeletion` is set on the parent or on all the subnamespaces. The
  HNC guide compares that field to `rm -rf`; set it at the lowest possible level.

## 3. Delegating safely
- Grant `create`/`delete` on `subnamespaceanchors` (not `namespaces`) to team leads via
  a namespaced RBAC Role — this is the actual delegation mechanism; no cluster-scoped
  permission is granted.

## Gotchas
- HNC changes the mental model of "a namespace is a flat, independent unit" — anyone
  debugging RBAC with `kubectl get rolebinding -n X` needs to know bindings may be
  inherited from an ancestor, not defined locally; `kubectl hns tree <ns>` and `kubectl
  hns describe <ns>` are essential, not optional, debugging tools once HNC is in use.
- Setting `allowCascadingDeletion` (for example from a cleanup script) removes the guard that
  protects subtrees from accidental deletion; do not set it broadly.
- Mixing HNC-managed subtrees with policy tools that assume flat namespaces (some
  Gatekeeper/Kyverno `namespaceSelector` patterns, or external cost-allocation tooling
  keyed on namespace name alone) can double-count or miss resources unless those tools
  are taught about the `*.tree.hnc.x-k8s.io/depth` labels.
- HNC is a smaller project than Kyverno/Gatekeeper: its latest GitHub release is v1.1.0 (June 2023)
  and its README roadmap still lists v1.2 with an ETA of late 2023. Confirm it fits your
  Kubernetes version and your support needs before committing a platform design to it.

## Verify
- [ ] A team-lead RBAC role that can only create `SubnamespaceAnchor` (not `Namespace`)
      successfully self-serves a new sub-namespace with inherited RBAC.
- [ ] `kubectl hns tree <parent>` matches the expected hierarchy after a self-service
      creation.
- [ ] Deleting a namespace that has subnamespaces is refused until `allowCascadingDeletion` is
      set, and deleting only the intended child (for example `kubectl hns delete`) works.
- [ ] If HRQ is installed, quota sharing across a subtree behaves as expected — a team cannot
      bypass its quota ceiling by creating additional sub-namespaces.

## Checked

Date: 2026-10-27. Documentation release: Kubernetes v1.37.1 (latest release; website main is the v1.38 development tree).

- Object names and API: `SubnamespaceAnchor` in `hnc.x-k8s.io/v1alpha2`, RBAC `Role`/`RoleBinding` propagated by default,
  modes `Propagate`, `AllowPropagate`, `Remove`, `Ignore`, tree labels `<ancestor>.tree.hnc.x-k8s.io/depth`, HRQ beta in v1.1
  and installed from `hrq.yaml`, `allowCascadingDeletion` webhook, `kubectl hns tree` and `describe`: HNC README, concepts and
  how-to guides (repository default branch).
- Project status: latest release v1.1.0, 2023-06-23 (GitHub releases API on 2026-10-27); README roadmap ETA for v1.2.
- Removed: a nonexistent `HierarchicalNamespace` kind, the `Select` mode, the claim that deleting a parent cascades by default,
  and the unconfirmed depth/count guard rails.

Method: documentation only; no commands were run.
