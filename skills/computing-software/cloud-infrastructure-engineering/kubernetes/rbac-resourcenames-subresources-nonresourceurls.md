---
id: computing-software.cloud-infrastructure-engineering.kubernetes.rbac-resourcenames-subresources-nonresourceurls
name: rbac-resourcenames-subresources-nonresourceurls
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, rbac, resourcenames, subresource-rbac, nonresourceurls, least-privilege, cka]
level: practitioner
status: docs-checked
description: "Write fine-grained RBAC rules: resourceNames for named objects, subresources like pods/exec and deployments/scale, and nonResourceURLs for /healthz and /metrics."
sources: ["https://kubernetes.io/docs/reference/access-authn-authz/rbac/#referring-to-resources", "https://kubernetes.io/docs/reference/access-authn-authz/authorization/#determine-the-request-verb", "https://kubernetes.io/docs/reference/access-authn-authz/kubelet-authn-authz/#kubelet-authorization", "https://kubernetes.io/docs/concepts/security/rbac-good-practices/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fine-grained RBAC: resourceNames, subresources, nonResourceURLs

## resourceNames
```yaml
rules:
- apiGroups: [""]
  resources: [configmaps]
  resourceNames: [app-config]
  verbs: [get, update, patch]
```
Rules:
- You cannot restrict `deletecollection` or top-level `create` requests by name (the name of a new
  object may not be known at authorization time). The `create` limit applies only to top-level
  resources: `resourceNames` works with a subresource such as `pods/exec`.
- If you restrict `list` or `watch` by name, the client must include a matching
  `metadata.name` field selector to be authorized, for example
  `kubectl get configmaps --field-selector=metadata.name=app-config`.
- Use names for singletons: a leader-election Lease, a specific Secret, a ConfigMap.

## Subresources
Written as `resource/subresource`; granting the parent does **not** grant the subresource.
| Subresource | Verb | Typical use |
|---|---|---|
| `pods/log` | get | `kubectl logs` |
| `pods/exec`, `pods/attach`, `pods/portforward` | create (POST); `get` if the client uses a WebSocket GET | debugging — high risk |
| `pods/ephemeralcontainers` | update/patch | `kubectl debug` |
| `deployments/scale`, `statefulsets/scale` | get, update, patch | autoscalers, `kubectl scale` |
| `*/status` | update, patch | controllers writing status |
| `serviceaccounts/token` | create | minting tokens |
| `nodes/metrics`, `nodes/stats`, `nodes/log`, `nodes/spec` | get | monitoring (kubelet `/metrics`, `/stats`, `/logs`, `/spec` paths) |
| `nodes/proxy` | get is **not** read-only | all other kubelet APIs, including command execution in any container on the node; avoid granting it |

```yaml
- apiGroups: [apps]
  resources: [deployments/scale]
  verbs: [get, update, patch]
```

## nonResourceURLs (ClusterRole only)
```yaml
kind: ClusterRole
rules:
- nonResourceURLs: ["/metrics", "/livez", "/readyz", "/healthz"]
  verbs: [get]
```
Only valid in ClusterRoles bound with ClusterRoleBindings (a namespaced Role is rejected). In
`nonResourceURLs` a `*` is a suffix glob match (for example `/healthz/*`). Non-resource requests use
the lower-cased HTTP method as the verb. Prometheus scraping the apiserver needs `/metrics`.

## Test precisely
```bash
kubectl auth can-i get configmaps/app-config -n app --as=system:serviceaccount:app:sa
kubectl auth can-i create pods/exec -n app --as=jane
kubectl auth can-i get /metrics --as=system:serviceaccount:monitoring:prometheus
kubectl auth can-i patch deployments --subresource=scale -n app --as=hpa-bot
```

## Gotchas
- Exec, attach and port-forward may be authorized as `create` (POST) or, over a WebSocket GET, as
  `get` on the subresource; grant what your real client needs and test with that client.
- `apiGroups: [""]` is the core group; deployments are `apps`, ingresses
  `networking.k8s.io` — wrong group = silently no access.

## Verify
- [ ] `kubectl auth can-i --list` for the subject shows no broader verbs than intended.

## Checked
Checked 2026-10-23 against the kubernetes/website docs (current release 1.37) and kubernetes/kubernetes source.
Confirmed: resourceNames limits (create and deletecollection; list/watch need a metadata.name field selector; `pods/exec`
example); subresource `resource/subresource` syntax; `nonResourceURLs` suffix glob and ClusterRole-only (RBAC validation and docs);
HTTP verb to request verb mapping; kubelet resource/subresource mapping (nodes/stats, metrics, log, spec, proxy); `kubectl auth can-i`
`--subresource` flag. Wrong in the original: list/watch listed as never nameable and "create with resourceNames never matches"
(true only for top-level create), nodes/proxy shown as a monitoring subresource (get on it is not read-only), the claim about
WebSockets since 1.30 (removed, unconfirmed).
Method: documentation only; no commands were run.
