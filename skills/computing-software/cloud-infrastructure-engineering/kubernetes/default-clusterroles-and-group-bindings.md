---
id: computing-software.cloud-infrastructure-engineering.kubernetes.default-clusterroles-and-group-bindings
name: default-clusterroles-and-group-bindings
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, rbac, default-clusterroles, user-facing-roles, group-binding, aggregated-clusterroles, admin-edit-view]
level: practitioner
status: docs-checked
description: "Use the built-in admin/edit/view ClusterRoles via RoleBindings to IdP groups, extend them with aggregation labels for CRDs, and avoid the cluster-admin shortcuts."
sources: ["https://kubernetes.io/docs/reference/access-authn-authz/rbac/#user-facing-roles", "https://kubernetes.io/docs/reference/access-authn-authz/rbac/#aggregated-clusterroles", "https://kubernetes.io/docs/reference/access-authn-authz/rbac/#auto-reconciliation", "https://github.com/kubernetes/kubernetes/blob/master/plugin/pkg/auth/authorizer/rbac/bootstrappolicy/policy.go"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Default user-facing roles and group bindings

## The built-ins
| ClusterRole | Use | Notable |
|---|---|---|
| `cluster-admin` | break-glass only | `*` on everything; bound to `system:masters` |
| `admin` | namespace owner | can create Roles/RoleBindings **in the namespace**; no quota/namespace edit |
| `edit` | developers | read/write most objects incl. Secrets; cannot view/modify Roles/RoleBindings |
| `view` | read-only | **excludes Secrets** by design; no `pods/exec`, but `pods/log` is readable |

At each apiserver start they are reconciled with the built-in definition (opt out by setting
annotation `rbac.authorization.kubernetes.io/autoupdate` to `false`); edit them and your changes are
overwritten — extend via aggregation instead.

## Bind to groups, scoped by namespace
```bash
kubectl create rolebinding team-a-edit --clusterrole=edit --group=oidc:team-a -n team-a
kubectl create rolebinding auditors-view --clusterrole=view --group=oidc:auditors -n team-a
```
A **RoleBinding** to a ClusterRole grants it only inside that namespace — the standard
multi-team pattern. A ClusterRoleBinding to `edit` grants it everywhere incl. kube-system.
Always bind **groups** from the IdP, not individual users, so joiners/leavers are handled
upstream. Group prefixes come from `--oidc-groups-prefix` / AuthenticationConfiguration
`claimMappings.groups.prefix`.

## Make CRDs visible to admin/edit/view
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: widgets-edit
  labels:
    rbac.authorization.k8s.io/aggregate-to-edit: "true"
    rbac.authorization.k8s.io/aggregate-to-admin: "true"
rules:
- apiGroups: [example.com]
  resources: [widgets]
  verbs: [get, list, watch, create, update, patch, delete]
```
Add a separate one with `aggregate-to-view: "true"` and read verbs only.

## Gotchas
- `edit` can read Secrets and create pods that mount any ServiceAccount in the namespace —
  effectively that SA's permissions. Treat `edit` as "can act as any SA in the ns".
- `view` users wanting `kubectl logs` have it (`pods/log` is included); `kubectl exec` is not.
- Groups `system:authenticated` / `system:unauthenticated` — never bind anything beyond
  discovery to them.

## Verify
- [ ] `kubectl get clusterrolebinding -o wide | grep -v system:` lists only intended subjects.
- [ ] `kubectl auth can-i --list -n team-a --as=x --as-group=oidc:team-a` matches the design.
- [ ] `kubectl auth can-i get widgets --as-group=oidc:auditors --as=x -n team-a` = yes.

## Checked

Checked 2026-10-27 against Kubernetes website content (main, v1.38 dev tree) and the v1.37 line (latest release at review time).

- admin/edit/view/cluster-admin descriptions, `view` excluding Secrets, `edit` able to run pods as any ServiceAccount, and the three `aggregate-to-*` labels confirmed in the RBAC page.
- Auto-reconciliation at start-up and its opt-out annotation `rbac.authorization.kubernetes.io/autoupdate` confirmed in the RBAC page.
- `pods/log` readable and `pods/exec` not readable for `view`, and `pods/exec` plus Secrets present in `edit`, confirmed in the bootstrap policy source (main branch).

Method: documentation only; no commands were run.
