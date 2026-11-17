---
id: computing-software.cloud-infrastructure-engineering.kubernetes.rbac-escalation-paths-and-auditing
name: rbac-escalation-paths-and-auditing
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, rbac, rbac-escalation, impersonate, kubectl-who-can, rbac-audit-tools, privilege-escalation, cks]
level: advanced
status: docs-checked
description: "Find RBAC privilege-escalation paths (escalate, bind, impersonate, pod create, secrets, nodes/proxy) and audit who can do what with kubectl auth can-i, who-can and rbac-tool."
sources: ["https://kubernetes.io/docs/concepts/security/rbac-good-practices/", "https://kubernetes.io/docs/reference/access-authn-authz/rbac/#privilege-escalation-prevention-and-bootstrapping", "https://kubernetes.io/docs/reference/access-authn-authz/user-impersonation/", "https://github.com/aquasecurity/kubectl-who-can", "https://github.com/alcideio/rbac-tool"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RBAC escalation paths and auditing

RBAC prevents creating a Role with permissions you do not hold — **unless** you have one of
the escalation verbs. Audit for these first.

## Permissions that equal (near) cluster-admin
| Grant | Why it escalates |
|---|---|
| `escalate` on roles/clusterroles | edit a role to add any permission |
| `bind` on roles/clusterroles | bind yourself to `cluster-admin` |
| `impersonate` on users/groups/serviceaccounts | `--as=admin --as-group=system:masters` |
| `create` pods (or deployments, jobs...) | mount any SA token in the namespace, hostPath, privileged (if PSA allows) |
| `get/list/watch` secrets | read SA tokens and credentials (`list` returns contents!) |
| `nodes/proxy` | kubelet API exec, attach and logs on every pod on the node; bypasses audit logging and admission, and `get` alone is enough |
| `create` serviceaccounts/token | mint tokens for any SA |
| `update/patch` on validating/mutating webhook configs | intercept or rewrite every request |
| `create` certificatesigningrequests + `update` on `certificatesigningrequests/approval` (signer `kubernetes.io/kube-apiserver-client`) | issue client certificates with arbitrary names, including system component identities |
| `patch` on namespaces | change Pod Security Admission or NetworkPolicy-relevant labels |
| create PersistentVolumes | `hostPath` volumes expose node files |

Also: `*` verbs or `*` resources anywhere; wildcards silently include future resources.

## Auditing
```bash
kubectl auth can-i --list --as=system:serviceaccount:ci:deployer          # one subject
kubectl auth can-i create clusterrolebindings --as=jane
kubectl who-can create pods -n prod            # krew: who-can
kubectl who-can impersonate users
kubectl rbac-tool lookup -e '^system:serviceaccount:'   # subjects -> roles
kubectl rbac-tool policy-rules -e jane
kubectl rbac-tool viz --outformat dot          # graph
```
For CI, run `kubectl rbac-tool analysis` in a pipeline and fail on new escalation grants.

## Safe impersonation
Give operators impersonation only of specific names:
```yaml
rules:
- apiGroups: [""]
  resources: [users]
  verbs: [impersonate]
  resourceNames: [readonly-debug]
```
Impersonated requests appear in audit logs with `impersonatedUser`; alert on any
impersonation of `system:masters`.

On clusters with the `ConstrainedImpersonation` feature gate (alpha in v1.35, beta and on by
default from v1.36) an impersonator can be limited to specific actions with the verbs
`impersonate:user-info` / `impersonate:serviceaccount` plus `impersonate-on:<mode>:<verb>`
(API group `authentication.k8s.io`); prefer it over plain `impersonate`.

## Gotchas
- Aggregated ClusterRoles grow automatically when someone adds a labelled role — review
  `aggregate-to-*` labels as carefully as bindings.
- Default `system:` bindings are not the place to look for drift; diff non-`system:` bindings
  against git.

## Verify
- [ ] No non-admin subject has escalate/bind/impersonate/nodes-proxy/secrets-list cluster-wide.
- [ ] CI check fails on new wildcard rules.

## Checked

Checked 2026-10-27 against Kubernetes website content (main, v1.38 dev tree) and the v1.37 line (latest release at review time), the kubectl-who-can and rbac-tool READMEs, and kubectl source.

- Escalation list confirmed in the RBAC good-practices page: escalate, bind, impersonate, workload creation, secrets list/watch, nodes/proxy (get is enough, bypasses audit and admission), serviceaccounts/token, webhook configuration control, namespace patch, PersistentVolume create, CSR approval for the kube-apiserver-client signer.
- Constrained impersonation verbs and feature-gate stages (alpha v1.35, beta v1.36 default on) confirmed in the impersonation page and feature-gate page.
- `kubectl auth can-i --list` confirmed in kubectl source; who-can flags and rbac-tool `lookup`, `policy-rules`, `viz`, `analysis` confirmed in their READMEs.
- Removed unconfirmed claims: node relabelling row, rakkess line, kubescape control IDs.

Method: documentation only; no commands were run.
