---
id: computing-software.cloud-infrastructure-engineering.kubernetes.gateway-api-gateways-listeners-and-httproute-filters
name: gateway-api-gateways-listeners-and-httproute-filters
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, gateway-api, gatewayclass, gateway-listeners, httproute-filters, requestredirect, requestheadermodifier, allowedroutes, referencegrant]
level: practitioner
status: docs-checked
description: "Configure Gateway API: GatewayClass, Gateway listeners with TLS and allowedRoutes, HTTPRoute matches and filters (redirect, rewrite, headers), and ReferenceGrant."
sources: ["https://gateway-api.sigs.k8s.io/reference/api-types/gateway/", "https://gateway-api.sigs.k8s.io/reference/api-types/httproute/", "https://gateway-api.sigs.k8s.io/guides/user-guides/http-redirect-rewrite/", "https://gateway-api.sigs.k8s.io/guides/user-guides/http-header-modifier/", "https://gateway-api.sigs.k8s.io/reference/api-types/referencegrant/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Gateway API: GatewayClass, listeners and HTTPRoute filters

## Roles
GatewayClass (infra provider: which controller) → Gateway (cluster operator: listeners,
addresses, TLS) → HTTPRoute (app team: routing). CRDs ship separately:
`kubectl apply --server-side -f https://github.com/kubernetes-sigs/gateway-api/releases/download/v1.6.1/standard-install.yaml`.

## Gateway with listeners
```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata: {name: public, namespace: gateway-infra}
spec:
  gatewayClassName: envoy            # kubectl get gatewayclass → ACCEPTED True
  listeners:
  - name: http
    protocol: HTTP
    port: 80
    allowedRoutes: {namespaces: {from: All}}
  - name: https-apps
    protocol: HTTPS
    port: 443
    hostname: "*.apps.example.com"
    tls:
      mode: Terminate
      certificateRefs: [{name: wildcard-apps-tls}]
    allowedRoutes:
      namespaces:
        from: Selector
        selector: {matchLabels: {gateway-access: public}}
```
Listener names must be unique, and listeners must be distinct (port, protocol and hostname); ones that
are not distinct are `Conflicted`. `kubectl describe gateway` shows per-listener conditions
(`Accepted`, `Programmed`, `ResolvedRefs`, `Conflicted`).

## HTTPRoute with filters
```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata: {name: shop, namespace: shop}
spec:
  parentRefs: [{name: public, namespace: gateway-infra, sectionName: https-apps}]
  hostnames: [shop.apps.example.com]
  rules:
  - matches: [{path: {type: PathPrefix, value: /api}}]
    filters:
    - type: URLRewrite
      urlRewrite: {path: {type: ReplacePrefixMatch, replacePrefixMatch: /}}
    - type: RequestHeaderModifier
      requestHeaderModifier:
        set: [{name: X-Env, value: prod}]
        remove: [X-Debug]
    backendRefs: [{name: shop-api, port: 8080, weight: 90}, {name: shop-api-v2, port: 8080, weight: 10}]
  - matches: [{path: {type: PathPrefix, value: /old}}]
    filters:
    - type: RequestRedirect
      requestRedirect: {path: {type: ReplaceFullPath, replaceFullPath: /new}, statusCode: 301}
---
# HTTP → HTTPS redirect on the port 80 listener
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata: {name: redirect-https, namespace: gateway-infra}
spec:
  parentRefs: [{name: public, sectionName: http}]
  rules:
  - filters: [{type: RequestRedirect, requestRedirect: {scheme: https, statusCode: 301}}]
```
Other filters: `ResponseHeaderModifier`, `RequestMirror` (shadow traffic), `ExtensionRef`
(implementation-specific). RequestRedirect and URLRewrite can't be combined in one rule, and a
RequestRedirect rule must not have `backendRefs`. `ReplacePrefixMatch` needs exactly one `PathPrefix`
match in the rule. `statusCode` 301 and 302 are Core; other redirect codes are Extended.

## Cross-namespace references
A route in `shop` pointing to a Service in `catalog`, or a Gateway using a cert Secret in
another namespace, needs a **ReferenceGrant** in the target namespace:
```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: ReferenceGrant
metadata: {name: allow-shop, namespace: catalog}
spec:
  from: [{group: gateway.networking.k8s.io, kind: HTTPRoute, namespace: shop}]
  to: [{group: "", kind: Service}]
```

## Verify
```bash
kubectl describe httproute shop -n shop      # status.parents[].conditions
```
- [ ] Route `Accepted=True` and `ResolvedRefs=True`; `curl -I http://shop...` returns 301 to https.

## Checked

Documentation release: Gateway API docs (kubernetes-sigs/gateway-api site/content and apis/v1, latest release v1.6.3, repo commit 2026-10-23; v1.7.0 is at release-candidate stage).
Confirmed: Gateway/HTTPRoute `v1`, listener conditions and conflict rule, `allowedRoutes.namespaces.from` (All/Same/Selector) and `tls.mode: Terminate`, filter enum (RequestHeaderModifier, ResponseHeaderModifier, RequestMirror, RequestRedirect, URLRewrite, ExtensionRef), the URLRewrite/RequestRedirect exclusion, `ReplacePrefixMatch`/`ReplaceFullPath`, redirect status codes, ReferenceGrant semantics.
Corrected: ReferenceGrant apiVersion, install version, and extra validation rules. Removed the unconfirmed `jq` pipeline.

Method: documentation only; no commands were run.
