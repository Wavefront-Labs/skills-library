---
id: computing-software.cloud-infrastructure-engineering.kubernetes.operator-rbac-and-multi-tenancy-scoping
name: operator-rbac-and-multi-tenancy-scoping
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, operator, rbac, kubebuilder-rbac-markers, clusterrole, namespaced-operator, cluster-scoped-operator, confused-deputy, aggregated-clusterrole, multi-tenant-operator, watchnamespace, least-privilege, privilege-escalation, serviceaccount]
level: advanced
status: docs-checked
description: "Scope an operator's own ServiceAccount permissions correctly: namespaced vs cluster-scoped install, kubebuilder RBAC markers, aggregation, and the confused-deputy trap in multi-tenant clusters."
sources: ["https://book.kubebuilder.io/reference/manager-scope", "https://book.kubebuilder.io/reference/markers/rbac", "https://kubernetes.io/docs/reference/access-authn-authz/rbac/", "https://kubernetes.io/docs/reference/access-authn-authz/admission-controllers/#ownerreferencespermissionenforcement", "https://kubernetes.io/docs/reference/access-authn-authz/authorization/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Operator RBAC and multi-tenancy scoping — the operator's own permissions, not the CRD's consumers'

**Goal:** the operator's ServiceAccount holds exactly the permissions its
controllers and webhooks use — no more — and a multi-tenant cluster can't be
tricked into using the operator as a privilege-escalation path for a tenant who
couldn't otherwise touch those resources. This complements, but is distinct from,
general cluster RBAC hygiene in
`computing-software.cloud-infrastructure-engineering.kubernetes.k8s-rbac-and-security`
— this skill is specifically about the permissions an operator's own identity needs.

## 1. Markers generate the ClusterRole, but check what they actually produced
```go
// +kubebuilder:rbac:groups=apps.example.com,resources=widgets,verbs=get;list;watch;create;update;patch;delete
// +kubebuilder:rbac:groups=apps.example.com,resources=widgets/status,verbs=get;update;patch
// +kubebuilder:rbac:groups=apps.example.com,resources=widgets/finalizers,verbs=update
// +kubebuilder:rbac:groups="",resources=secrets,verbs=get;list;watch
```
The RBAC markers cause an RBAC `ClusterRole` to be generated (`make manifests` writes
`config/rbac/role.yaml`); adding `namespace=<ns>` to a marker makes controller-gen generate a `Role`
instead. Kubebuilder scaffolds cluster-scoped managers by default (`ClusterRole` and `ClusterRoleBinding`,
watching all namespaces), and `kubebuilder init --namespaced` (or `kubebuilder edit --namespaced=true`)
scaffolds the namespace-scoped layout. Audit every marker: does this controller actually need
`delete` on Secrets, or only `get`? The scaffold is a starting point, not the production-ready role.

## 2. Namespaced vs cluster-scoped install — a real architectural choice
- **Cluster-scoped** (`ClusterRole` + `ClusterRoleBinding`, watches all
  namespaces): simplest to operate, one instance serves the whole cluster.
  Correct when the CRD itself is conceptually cluster-wide (cluster policies,
  cluster-wide infra resources) or when there's exactly one tenant.
- **Namespaced** (`Role` + `RoleBinding` per namespace, operator watches only its
  own or a configured set): required in real multi-tenant clusters where tenant A
  must not be able to see or influence tenant B's custom resources or the
  Secrets/ConfigMaps the operator reads on their behalf. controller-runtime
  supports this via `cache.Options{DefaultNamespaces: map[string]cache.Config{...}}`
  (watch only specified namespaces); the Kubebuilder `--namespaced` scaffold reads the `WATCH_NAMESPACE`
  environment variable (comma-separated for several namespaces) to build it, and needs a `Role` and
  `RoleBinding` in each watched namespace. With webhooks, requests from all namespaces still arrive, so set a
  `namespaceSelector` or `objectSelector` on the webhooks to match the cache.
- A common production pattern: one cluster-scoped **controller manager** that
  owns the CRD and reconciliation logic, but whose *effect* (what it creates on a
  tenant's behalf) is itself scoped per-namespace by the CR's own namespace — the
  operator's RBAC is cluster-wide, but its generated children are namespace-local.
  This still needs careful review: cluster-wide read on Secrets, even if writes
  are namespace-scoped by convention in code, is a cluster-wide read grant in RBAC
  terms — code-level scoping is not a substitute for an actual RBAC boundary when
  the threat model includes a compromised controller process.

## 3. The confused-deputy trap
An operator's ServiceAccount typically holds far broader permissions (create
Deployments, read Secrets, manage cloud credentials) than any individual tenant
using the CRD. If the CRD's spec lets a tenant influence *what the operator acts
on* without validation (e.g. a field naming an arbitrary Secret to mount, an
arbitrary namespace to write into, an arbitrary image to run), a tenant who can
only create the CRD — and nothing else — can use the operator as a proxy to read
or write things their own RBAC would never allow directly. This is the single most
underrated risk in self-service operator CRDs.
- Validate (webhook or CEL) that spec fields referencing other resources
  (Secrets, ServiceAccounts, namespaces) are constrained to the CR's own
  namespace, or to an explicit admin-controlled allowlist, before the controller
  acts on them.
- Never let a CRD spec field directly become a cluster-scoped RBAC grant or a
  cross-namespace reference without an explicit admission check — "the operator
  can do it, so letting the user ask it to is fine" is exactly the confused-deputy
  pattern.
- If different tenants need genuinely different operator privilege levels,
  consider separate operator installs per tenant namespace rather than one
  shared cluster-scoped identity mediating everyone's requests.

## 4. Aggregated ClusterRoles for extending built-ins
If the operator's CRD should be editable by anyone who already holds the
cluster's standard `admin`/`edit`/`view` roles (common for "this is just another
kind of workload" CRDs), use **aggregation** instead of telling every tenant to
also bind your operator's specific role:
```yaml
metadata:
  labels: {rbac.authorization.k8s.io/aggregate-to-edit: "true"}
rules:
- apiGroups: [apps.example.com]
  resources: [widgets]
  verbs: [get, list, watch, create, update, patch, delete]
```
This auto-merges into the cluster's built-in aggregated `edit`/`view` ClusterRoles
— no binding management on your part, and it means a later cluster-wide RBAC
audit tool correctly understands who can touch your CRD.

## Gotchas
- Kubebuilder scaffolds a `widgets/finalizers` `update` rule. Kubernetes needs it when the
  `OwnerReferencesPermissionEnforcement` admission controller is enabled: only users with `update` on the
  owner's `finalizers` subresource can set `blockOwnerDeletion` on an owner reference.
- Leader election needs RBAC on `coordination.k8s.io` `leases` (and the scaffold also grants configmaps and
  `events` create/patch) in the operator's namespace; Kubebuilder scaffolds this as `leader-election-role`.
- Testing RBAC with `kubectl auth can-i ... --as system:serviceaccount:<ns>:<sa>` must
  use the operator's actual ServiceAccount name, not your own user.

## Verify
- [ ] `kubectl auth can-i <verb> <resource> --as system:serviceaccount:<ns>:<operator-sa>`
      returns `yes` only for verbs the controllers/webhooks actually call — no leftover
      scaffold permissions for resources never touched in code.
- [ ] A tenant who can create the CRD but holds no other permissions cannot, via
      any CRD spec field, cause the operator to read or write a resource outside
      their own namespace.
- [ ] If namespaced: the operator's cache/watch is explicitly scoped (not
      cluster-wide watch paired with namespaced-only RBAC, which just produces
      watch errors).
- [ ] `widgets/status` and `widgets/finalizers` subresource RBAC rules are present
      and distinct from the base `widgets` rule.

## Checked

Checked on 2026-10-26 against the Kubebuilder book (`reference/manager-scope`, `reference/markers/rbac`, cronjob tutorial `leader_election_role.yaml`) on `kubernetes-sigs/kubebuilder` (pushed 2026-10-25), and the Kubernetes website docs `access-authn-authz/rbac.md`, `authorization.md`, `admission-controllers.md`.
Confirmed: markers generate a `ClusterRole` and `namespace=` generates a `Role`; default cluster-scoped scaffold and `--namespaced`; `WATCH_NAMESPACE` with `cache.Options{DefaultNamespaces}`; webhooks need selectors in namespaced mode; aggregation labels `aggregate-to-admin`, `aggregate-to-edit`, `aggregate-to-view`; the leader-election Role contents; `OwnerReferencesPermissionEnforcement` and `finalizers` `update`; `kubectl auth can-i --as system:serviceaccount:...`.
Wrong in the draft: the finalizer-RBAC failure mode (it is tied to `blockOwnerDeletion` under that admission plugin). Removed as unconfirmed: the silent leader-election hang and the RBAC-caching remark.

Method: documentation only; no commands were run.
