---
id: computing-software.cloud-infrastructure-engineering.istio.istio-authorizationpolicy-allow-deny
name: istio-authorizationpolicy-allow-deny
category: computing-software
field: cloud-infrastructure-engineering
product: istio
tags: [istio, authorizationpolicy, authz, allow-nothing]
level: practitioner
status: docs-checked
description: "Build deny-by-default access with an empty AuthorizationPolicy, then grant methods and service accounts incrementally with ALLOW policies."
sources: ["https://istio.io/latest/docs/tasks/security/authorization/authz-http/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Start from an allow-nothing policy, then add ALLOW policies one workload at a time (the Istio task does this with Bookinfo).

```yaml
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata: {name: allow-nothing, namespace: shop}
spec: {}
---
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata: {name: web-viewer, namespace: shop}
spec:
  selector: {matchLabels: {app: web}}
  action: ALLOW
  rules:
  - from: [{source: {principals: ["cluster.local/ns/shop/sa/frontend"]}}]
    to: [{operation: {methods: ["GET"]}}]
```

Semantics from the task: a policy without `selector` applies to every workload in its namespace; the empty `spec: {}` permits no traffic, so requests are rejected with `RBAC: access denied`. An ALLOW rule without a `from` field allows all sources (the task's productpage-viewer). With `from.source.principals` set to a service account identity such as `cluster.local/ns/default/sa/bookinfo-productpage`, only that caller is allowed.

Gotchas: the task requires mutual TLS because principal and namespace rules depend on it. The allow-nothing policy also affects a Gateway API gateway workload in the same namespace, so add an ALLOW for it (the task selects it with `gateway.networking.k8s.io/gateway-name: bookinfo-gateway`). Policies can take a few seconds to propagate because of caching and propagation overhead. Expect each missing hop to show up as an error, for example productpage allowed but details and reviews not yet allowed gives "Error fetching product details".

## Checked

2026-11-03. Confirmed against the Istio HTTP Traffic authorization task: allow-nothing, ALLOW policies with methods and principals, mTLS requirement, `RBAC: access denied`, gateway selector, propagation delay. Removed: the CUSTOM/DENY/ALLOW evaluation order and "any DENY match rejects" claims (not on this page), the 403 and POST verify step and the policy naming advice.
Method: documentation only; no commands were run.
