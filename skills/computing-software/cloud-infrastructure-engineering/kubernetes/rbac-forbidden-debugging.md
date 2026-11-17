---
id: computing-software.cloud-infrastructure-engineering.kubernetes.rbac-forbidden-debugging
name: rbac-forbidden-debugging
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, rbac, forbidden-error, rbac-forbidden, kubectl-auth-can-i, audit-logging]
level: practitioner
status: docs-checked
description: "Decode Forbidden (403) errors from the API server: identify user, verb, resource and namespace, find the missing rule, and check audit logs for the decision."
sources: ["https://kubernetes.io/docs/reference/access-authn-authz/authorization/", "https://kubernetes.io/docs/reference/access-authn-authz/rbac/", "https://kubernetes.io/docs/tasks/debug/debug-cluster/audit/", "https://kubernetes.io/docs/reference/labels-annotations-taints/audit-annotations/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Debugging Forbidden errors

## Read the message
```
Error from server (Forbidden): deployments.apps "web" is forbidden: User
"system:serviceaccount:build:ci" cannot patch resource "deployments" in API group "apps"
in the namespace "prod"
```
It contains everything: user, verb (`patch`), resource and group, namespace. A missing
namespace in the message means a cluster-scoped request (needs a ClusterRoleBinding).

## Reproduce
```bash
kubectl auth can-i patch deployments.apps -n prod --as=system:serviceaccount:build:ci
kubectl auth can-i --list -n prod --as=system:serviceaccount:build:ci
kubectl auth whoami          # who am I really (OIDC, exec plugins can surprise you)
```
For a user with groups: `--as=alice --as-group=dev-team`.

## Find what is bound
```bash
kubectl get rolebindings,clusterrolebindings -A -o json | jq -r '
  .items[] | select(.subjects[]? | .name=="ci" and (.namespace//"")=="build")
  | "\(.metadata.namespace // "cluster")/\(.metadata.name) -> \(.roleRef.kind)/\(.roleRef.name)"'
kubectl rbac-tool lookup ci        # krew plugin rbac-tool; the who-can krew plugin answers: kubectl who-can patch deployments -n prod
```

## Typical root causes
| Cause | Fix |
|---|---|
| Rule uses wrong apiGroup (`""` instead of `apps`) | match the group in the error |
| Subresource missing (`pods/exec`, `deployments/scale`, `pods/log`) | add it explicitly |
| RoleBinding in the wrong namespace | bind in the target namespace |
| SA subject missing `namespace` | add it |
| Cluster-scoped resource with a Role | use ClusterRole + ClusterRoleBinding |
| Webhook authorizer or admission denied (message differs: `admission webhook ... denied`) | not RBAC; check policies |

## Audit log
With audit at Metadata level, denied requests carry
`annotations."authorization.k8s.io/decision": "forbid"` and an `authorization.k8s.io/reason` annotation:
```bash
jq 'select(.annotations["authorization.k8s.io/decision"]=="forbid") | {user:.user.username, verb, uri:.requestURI}' audit.log
```

## Checked
Checked 2026-10-23 against the kubernetes/website docs (current release 1.37), kubectl source, the krew index and plugin READMEs.
Confirmed: audit annotations `authorization.k8s.io/decision` (allow or forbid) and `authorization.k8s.io/reason`; `kubectl auth can-i`
(`--list`, `--as`, `--as-group`, `--subresource`); `kubectl auth whoami`; krew plugins `rbac-tool` (subcommands lookup, who-can) and
`who-can`; wrong-group, missing-subresource and namespaced-Role-for-cluster-resource causes against the RBAC docs (nonResourceURLs
and cluster-scoped rules need a ClusterRole). The sample Forbidden message follows the apiserver's standard wording.
Method: documentation only; no commands were run.
