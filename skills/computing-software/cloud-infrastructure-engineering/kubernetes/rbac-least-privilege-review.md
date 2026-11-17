---
id: computing-software.cloud-infrastructure-engineering.kubernetes.rbac-least-privilege-review
name: rbac-least-privilege-review
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, rbac, rbac-least-privilege, rbac-wildcards, rbac-escalation, secret-exposure]
level: practitioner
status: docs-checked
description: "Review RBAC for least privilege: find wildcards, secret list/watch, pods/exec, escalate/bind/impersonate, node proxy, and cluster-admin sprawl, then tighten."
sources: ["https://kubernetes.io/docs/concepts/security/rbac-good-practices/", "https://kubernetes.io/docs/reference/access-authn-authz/rbac/", "https://github.com/alcideio/rbac-tool"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RBAC least-privilege review

## High-risk permissions (from the Kubernetes RBAC good-practices page)
| Permission | Why it is dangerous |
|---|---|
| `*` verbs or resources | grants future resources too |
| `list`/`watch` on secrets | returns full Secret contents, not just names |
| `create` pods (or any workload) | can mount any Secret/SA in the namespace and run as it |
| `pods/exec`, `pods/attach` | shell inside running workloads |
| `nodes/proxy` | direct kubelet API access, bypasses audit and admission |
| `escalate`, `bind` | grant yourself more |
| `impersonate` | become another user or group |
| `create` on `serviceaccounts/token` | mint tokens for any SA |
| `update` on validating/mutating webhook configs | disable policy |
| `patch` on namespaces | change PSA labels |
| PersistentVolume create | hostPath PVs to read node files |

## Find them
```bash
# who has cluster-admin
kubectl get clusterrolebindings -o json | jq -r '.items[] | select(.roleRef.name=="cluster-admin") | .metadata.name + ": " + ([.subjects[]? | .kind+"/"+.name] | join(","))'
# roles with wildcards
kubectl get clusterroles,roles -A -o json | jq -r '.items[] | select(any(.rules[]?; (.verbs|index("*")) or (.resources|index("*")))) | .kind+"/"+(.metadata.namespace//"")+"/"+.metadata.name' | grep -v system:
# who can read secrets
kubectl who-can list secrets -A           # krew: who-can
```
Tools: `kubectl rbac-tool analysis`, `kubectl rbac-tool who-can`.

## Tighten
- Replace wildcards with explicit verbs/resources; ignore `system:` roles (managed).
- Replace `list secrets` with `get` plus `resourceNames` where the app knows the names (if you
  restrict `list` or `watch` by name, clients must send a matching `metadata.name` field selector).
- Move human access to groups via OIDC and default `view`/`edit`; keep cluster-admin to a
  break-glass group.
- Remove bindings to `system:authenticated` or `system:unauthenticated` other than defaults.

## Verify
Re-run the queries; diff `kubectl auth can-i --list --as=<subject>` before and after for each
changed subject and confirm the workload still works in staging.

## Checked

Checked 2026-10-27 against Kubernetes website content (main, v1.38 dev tree) and the v1.37 line (latest release at review time) and the rbac-tool README.

- The high-risk permission table matches the RBAC good-practices page (wildcards, secrets list/watch, workload creation, nodes/proxy, escalate/bind, impersonate, serviceaccounts/token, webhook configurations, namespace patch, PersistentVolume create); `pods/exec` and `pods/attach` grant shell access to running workloads.
- `resourceNames` behaviour for list/watch (needs a `metadata.name` field selector) confirmed in the RBAC page.
- Removed the unconfirmed kubescape and KubiScan references.

Method: documentation only; no commands were run.
