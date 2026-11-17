---
id: computing-software.ai-ml-engineering.seldon-core-2.securing-endpoints-istio-jwt
name: securing-endpoints-istio-jwt
category: computing-software
field: ai-ml-engineering
product: seldon-core-2
tags: [seldon-core-2, security, istio, jwt, requestauthentication, authorizationpolicy, oidc, endpoint-security]
level: advanced
status: docs-checked
description: "Secure Seldon Core 2 inference endpoints at the Istio ingress gateway: a RequestAuthentication for your OIDC issuer and a deny-empty-jwt AuthorizationPolicy, verified with curl."
sources: ["https://github.com/SeldonIO/seldon-core/blob/v2/docs-gb/models/securing-endpoints.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Securing endpoints with Istio JWT

Control access to model and pipeline endpoints using mesh-level controls, or a cloud API gateway. With Istio you can enforce JWT authentication at the ingress gateway.

## Prerequisites
A deployed model, a configured Istio gateway, a virtual service exposing REST and gRPC, and an OIDC provider whose `issuer`, `jwksUri` and access token you have.

## Steps
1. Create a `RequestAuthentication` named `ingress-jwt-auth` in `istio-system`, selecting `istio: istio-ingressgateway`:

```yaml
apiVersion: security.istio.io/v1beta1
kind: RequestAuthentication
metadata:
  name: ingress-jwt-auth
  namespace: istio-system
spec:
  selector:
    matchLabels:
      istio: istio-ingressgateway
  jwtRules:
    - issuer: <OIDC_TOKEN_ISSUER>
      jwksUri: <OIDC_TOKEN_ISSUER_JWKS>
```

2. Create `AuthorizationPolicy` `deny-empty-jwt` in `istio-system` with `action: DENY`, a rule whose `from.source.notRequestPrincipals` matches any principal and `to.operation.paths` set to `/v2/*`, selecting `app: istio-ingressgateway`.

3. Verify. A request to `/v2/models/iris/infer` without a token returns `403 Forbidden` with `RBAC: access denied`. Repeating it with the header `Authorization: Bearer $ACCESS_TOKEN` returns `200 OK`.

Authorization policies come in many types, so adapt the rules to your access model.

## Checked

2026-11-09: resource names, namespaces, selectors, policy rules and the 403/200 verification confirmed. Made the path pattern the documented `/v2/*`.

Method: docs-checked 2026-11-09 against the Seldon docs-gb models/securing-endpoints.md
