---
id: computing-software.cloud-infrastructure-engineering.kubernetes.header-and-cookie-canary-routing
name: header-and-cookie-canary-routing
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, deployment-strategies, header-based-canary, canary, ingress-nginx, gateway-api]
level: practitioner
status: docs-checked
description: "Route chosen users to a canary by header or cookie with ingress-nginx canary annotations, Gateway API header matches, or Argo Rollouts header routes (Istio, ALB, APISIX)."
sources: ["https://kubernetes.github.io/ingress-nginx/user-guide/nginx-configuration/annotations/#canary", "https://github.com/kubernetes-sigs/gateway-api/blob/main/apis/v1/httproute_types.go", "https://argo-rollouts.readthedocs.io/en/stable/features/traffic-management/", "https://github.com/kubernetes/ingress-nginx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Header and cookie based canary routing

Internal testers or a beta cohort see the new version before any random traffic split.

## ingress-nginx
ingress-nginx is retired: its README says best-effort maintenance ran until March 2026 and
there are no further releases or security fixes afterwards, and it recommends choosing a
Gateway API implementation for new deployments. The annotations below are for clusters
still running it.

A second Ingress for the same host, marked canary (at most one canary Ingress per Ingress
rule):
```yaml
metadata:
  name: shop-canary
  annotations:
    nginx.ingress.kubernetes.io/canary: "true"
    nginx.ingress.kubernetes.io/canary-by-header: "X-Canary"
    nginx.ingress.kubernetes.io/canary-by-header-value: "always"
    nginx.ingress.kubernetes.io/canary-by-cookie: "canary"      # cookie value "always" routes to canary
    # nginx.ingress.kubernetes.io/canary-weight: "5"             # optional random share
spec:
  ingressClassName: nginx
  rules: [{host: shop.example.com, http: {paths: [{path: /, pathType: Prefix, backend: {service: {name: shop-canary, port: {number: 80}}}}]}}]
```
Precedence documented by ingress-nginx: `canary-by-header` -> `canary-by-cookie` -> `canary-weight`.
Without `canary-by-header-value`, the header value `always` routes to the canary and `never`
keeps the request off it; with `canary-by-header-value` set, only that value matches.
`canary-by-cookie` only reads the cookie (`always` or `never`); something else, such as
your app or an edge proxy after a beta opt-in, has to set it.

## Gateway API
```yaml
rules:
- matches: [{headers: [{name: X-Canary, value: always}]}]
  backendRefs: [{name: shop-canary, port: 80}]
- backendRefs: [{name: shop, port: 80}]
```
`HTTPRoute` (`gateway.networking.k8s.io/v1`, GA since Gateway API v1.0) matches headers by
`name` and `value`. The spec orders matches by exact path, then longest prefix, then method,
then the largest number of header matches, so the header rule above wins over the
catch-all rule; ties go to the first rule in list order. There is no cookie-specific
match; a cookie is just the `Cookie` header.

## Argo Rollouts
```yaml
strategy:
  canary:
    trafficRouting:
      managedRoutes: [{name: header-route}]
      istio: {virtualService: {name: shop}}
    steps:
    - setHeaderRoute: {name: header-route, match: [{headerName: X-Canary, headerValue: {exact: always}}]}
    - pause: {}
    - setWeight: 10
```
Argo documents header-based routing for Istio, Apache APISIX, AWS ALB and (via plugin)
Gateway API. `headerValue` takes exactly one of `exact`, `regex` or `prefix`, and not every
router supports every match type. Routes listed in `managedRoutes` are removed at the end
of a rollout or on abort, so do not list hand-made routes there. A second
`setHeaderRoute` step with only the route `name` disables the header route.

## Gotchas
- CDNs and caches must vary on the header or cookie, or canary responses get served to everyone.

## Verify
`curl -H 'X-Canary: always' https://shop.example.com/version` returns the canary version and plain
`curl` returns stable.

## Checked
2026-10-27. Documentation releases: ingress-nginx README and annotation docs (controller v1.15.1 tree), Gateway API v1.6.3 (`HTTPRoute` types), Argo Rollouts v1.10.1 traffic-management docs.
Confirmed: canary annotation names, header/cookie `always`/`never` semantics and precedence, one canary Ingress per rule, ingress-nginx retirement text, HTTPRoute header match fields and match precedence, v1 GA at v1.0, Argo `managedRoutes`/`setHeaderRoute` fields, supported routers and disable behaviour.
Method: documentation only; no commands were run.
