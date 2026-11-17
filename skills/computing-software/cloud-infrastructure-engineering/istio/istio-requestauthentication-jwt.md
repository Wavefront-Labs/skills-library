---
id: computing-software.cloud-infrastructure-engineering.istio.istio-requestauthentication-jwt
name: istio-requestauthentication-jwt
category: computing-software
field: cloud-infrastructure-engineering
product: istio
tags: [istio, requestauthentication, jwt, end-user-auth]
level: practitioner
status: docs-checked
description: "Configure RequestAuthentication jwtRules and pair it with a DENY AuthorizationPolicy, because requests without a token are accepted otherwise."
sources: ["https://istio.io/latest/docs/tasks/security/authentication/authn-policy/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
RequestAuthentication validates a JWT when one is provided; it does not require one.

```yaml
apiVersion: security.istio.io/v1
kind: RequestAuthentication
metadata: {name: jwt-example, namespace: shop}
spec:
  selector: {matchLabels: {app: web}}
  jwtRules:
  - issuer: "https://issuer.example.com"
    jwksUri: "https://issuer.example.com/.well-known/jwks.json"
```

Apply the policy in the namespace of the workload it selects (the task applies the ingress gateway's policy in `istio-system`, or with `targetRef` for a Gateway API Gateway). The token is read from the `Authorization` header by default.

To require a token, add an AuthorizationPolicy with `action: DENY` and a rule `from: [{source: {notRequestPrincipals: ["*"]}}]`. Request principals exist only when a valid JWT is provided. You can narrow it with `to: [{operation: {paths: ["/headers"]}}]` so only that path needs a token.

Observed in the task: no token gives 200 before the DENY policy and 403 after; an invalid token (`Authorization: Bearer deadbeef`) gives 401; a valid token gives 200. JWT validation allows 60 seconds of clock skew: a token becomes valid 60 seconds before its `nbf` and stays valid 60 seconds after its `exp` (a 5 second token was still accepted for about 65 seconds). A policy on the ingress gateway can cover all services bound to it.

## Checked

2026-11-03. Confirmed against the Istio Authentication Policy task (End-user authentication section): RequestAuthentication shape, default header, DENY with `notRequestPrincipals`, per-path variant, 200/401/403 results, 60 second skew. Removed: the claims that istiod must reach `jwksUri` and about JWKS caching and rotation, which the page does not cover.
Method: documentation only; no commands were run.
