---
id: computing-software.cloud-infrastructure-engineering.kubernetes.user-impersonation-testing
name: user-impersonation-testing
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, authentication, kubectl-as, impersonation-headers, impersonate, rbac]
level: practitioner
status: docs-checked
description: "Use impersonation (--as, --as-group, --as-uid) to test what users and ServiceAccounts can do, grant impersonate safely, and read impersonated audit events."
sources: ["https://kubernetes.io/docs/reference/access-authn-authz/user-impersonation/", "https://kubernetes.io/docs/reference/access-authn-authz/authentication/", "https://kubernetes.io/docs/tasks/debug/debug-cluster/audit/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# User impersonation

## Use it
```bash
kubectl get pods -n prod --as=alice --as-group=dev-team
kubectl auth can-i delete pods -n prod --as=system:serviceaccount:prod:web
kubectl auth whoami --as=alice --as-group=dev-team
```
Headers on raw API calls: `Impersonate-User`, `Impersonate-Group` (repeatable),
`Impersonate-Uid`, `Impersonate-Extra-<key>`.

The impersonated identity consists only of the headers you send; groups are NOT looked up from
your IdP. If permissions come via a group, add `--as-group` or the test gives false "no" answers.
Flags: `--as-uid` (v1.23) sets `Impersonate-Uid`; `--as-user-extra` (v1.35) sets extra fields.

## Granting impersonation
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata: {name: impersonate-dev}
rules:
- apiGroups: [""]
  resources: ["users", "groups"]
  verbs: ["impersonate"]
  resourceNames: ["alice", "dev-team"]
- apiGroups: [""]
  resources: ["serviceaccounts"]
  verbs: ["impersonate"]
  resourceNames: ["web"]
```
Unscoped `impersonate` on users/groups means "can become cluster-admin" via
`--as-group=system:masters`. Always use resourceNames. Impersonation is not namespace scoped, so
grant it with a ClusterRole and ClusterRoleBinding (ServiceAccount impersonation is namespaced,
but the ServiceAccount may act outside its namespace).

On clusters with `ConstrainedImpersonation` (beta, on by default from v1.36) you can instead limit
an impersonator to specific actions with `impersonate:user-info` and `impersonate-on:user-info:<verb>`
(API group `authentication.k8s.io`).

## Audit trail
Impersonated requests record both identities:
```bash
jq 'select(.impersonatedUser) | {by: .user.username, as: .impersonatedUser.username, verb, uri: .requestURI}' audit.log
```

## Uses
- Validate a new Role before giving it to the team.
- Support engineers reproducing "I get Forbidden".
- CI checks: `kubectl auth can-i --list --as=...` diffed against an expected file.

## Checked

Checked 2026-10-27 against Kubernetes website content (main, v1.38 dev tree) and the v1.37 line (latest release at review time).

- Impersonation headers (`Impersonate-User`, `-Group`, `-Uid`, `-Extra-*`), the kubectl flags `--as`, `--as-group`, `--as-uid` (1.23) and `--as-user-extra` (1.35), and the RBAC verbs and `resourceNames` restriction confirmed in the user impersonation page.
- Impersonation not being namespace scoped, and `impersonatedUser` in audit events, confirmed in the same page.
- `ConstrainedImpersonation` stages (alpha v1.35, beta v1.36 default on) confirmed in the feature-gate reference.
- `kubectl auth can-i --list` and `kubectl auth whoami` confirmed in kubectl source and the authentication page.

Method: documentation only; no commands were run.
