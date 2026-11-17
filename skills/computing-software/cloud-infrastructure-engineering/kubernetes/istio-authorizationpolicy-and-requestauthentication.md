---
id: computing-software.cloud-infrastructure-engineering.kubernetes.istio-authorizationpolicy-and-requestauthentication
name: istio-authorizationpolicy-and-requestauthentication
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, istio, service-mesh, authorizationpolicy, requestauthentication, jwt, zero-trust, mtls]
level: advanced
status: docs-checked
description: "Enforce service-to-service and end-user access in Istio: AuthorizationPolicy ALLOW/DENY/CUSTOM evaluation order, principals from mTLS, JWT validation with RequestAuthentication."
sources: ["https://istio.io/latest/docs/concepts/security/", "https://istio.io/latest/docs/reference/config/security/authorization-policy/", "https://istio.io/latest/docs/reference/config/security/request_authentication/", "https://istio.io/latest/docs/reference/commands/istioctl/", "https://istio.io/latest/docs/ambient/usage/l4-policy/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Istio AuthorizationPolicy and RequestAuthentication

## Evaluation order (per workload)
1. **CUSTOM** (external authorizer) — deny if it denies.
2. **DENY** policies — any match denies.
3. **ALLOW** policies — if **any** ALLOW policy applies to the workload, the request must match
   one; otherwise it is denied.
4. No ALLOW policies → allowed.
So the first ALLOW policy you add to a workload flips it to default-deny for everything else.

## Mesh-wide default deny, then allow
```yaml
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata: {name: allow-nothing, namespace: istio-system}   # root namespace = mesh-wide
spec: {}                                                   # ALLOW with no rules = deny all
---
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata: {name: orders-from-frontend, namespace: orders}
spec:
  selector: {matchLabels: {app: orders}}
  action: ALLOW
  rules:
  - from:
    - source: {principals: ["cluster.local/ns/shop/sa/frontend"]}   # SPIFFE identity from mTLS
    to:
    - operation: {methods: ["GET","POST"], paths: ["/api/orders*"]}
```
`principals` require **STRICT mTLS** (PeerAuthentication) — with plaintext, no identity exists
and the rule never matches. Use `namespaces:` for coarse rules. Ambient mode: L4 rules enforced by
ztunnel; HTTP-attribute rules need a waypoint proxy.

## End-user JWTs
```yaml
apiVersion: security.istio.io/v1
kind: RequestAuthentication
metadata: {name: jwt, namespace: orders}
spec:
  selector: {matchLabels: {app: orders}}
  jwtRules:
  - issuer: https://auth.example.com/
    jwksUri: https://auth.example.com/.well-known/jwks.json
    audiences: [orders-api]
    forwardOriginalToken: true
---
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata: {name: require-jwt, namespace: orders}
spec:
  selector: {matchLabels: {app: orders}}
  action: ALLOW
  rules:
  - from: [{source: {requestPrincipals: ["https://auth.example.com/*"]}}]
    when: [{key: "request.auth.claims[scope]", values: ["orders:write"]}]
```
RequestAuthentication alone only rejects **invalid** tokens; requests with **no** token pass —
pair it with an AuthorizationPolicy requiring `requestPrincipals`.

## Debug
```bash
istioctl x authz check <pod>.orders
kubectl logs <pod> -c istio-proxy                 # raise log levels with: istioctl proxy-config log <pod> --level <logger>:debug
```
Policy denials appear as `RBAC: access denied`; check `istioctl proxy-config log <pod> --help` for the current logger names.

## Verify
- [ ] Requests from an unlisted SA get 403; with a valid JWT and scope succeed; missing JWT denied.

## Checked
2026-10-26. Checked against the istio.io docs source (repository istio/istio.io, last commit 2026-10-23). Confirmed: evaluation order CUSTOM, DENY, ALLOW; deny-by-default applies only when a workload has at least one ALLOW policy; an ALLOW policy with no rules matches nothing (allow-nothing) and a policy in the root namespace is mesh-wide; `security.istio.io/v1` apiVersion; ztunnel enforces only L4 policy in ambient mode; `istioctl experimental authz check` (alias `x`) and `istioctl proxy-config log` exist. The `403`/`401` response mapping and the rbac logger name are from experience and were not confirmed in the fetched pages, so they are removed.
Method: documentation only; no commands were run.
