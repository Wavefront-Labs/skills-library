---
id: computing-software.devops-ci-cd.deployment-strategies.header-and-cookie-canary-routing
name: header-and-cookie-canary-routing
category: computing-software
field: devops-ci-cd
product: deployment-strategies
tags: [deployment-strategies, header-based-routing, canary, traffic-splitting]
level: practitioner
status: docs-checked
description: "Route specific users to a canary by header or cookie (ingress-nginx canary annotations, Istio VirtualService) for internal dogfooding before weight-based traffic."
sources: ["https://kubernetes.github.io/ingress-nginx/user-guide/nginx-configuration/annotations/#canary", "https://istio.io/latest/docs/reference/config/networking/virtual-service/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Header and cookie canary routing

Before shifting a percentage of real users, route **chosen** traffic (employees, test accounts,
beta users) to the canary.

## ingress-nginx
Second Ingress for the canary service, same host/path:
```yaml
metadata:
  annotations:
    nginx.ingress.kubernetes.io/canary: "true"
    nginx.ingress.kubernetes.io/canary-by-header: "X-Canary"
    nginx.ingress.kubernetes.io/canary-by-header-value: "always"
    nginx.ingress.kubernetes.io/canary-by-cookie: "canary"      # cookie value "always" -> canary, "never" -> stable
    nginx.ingress.kubernetes.io/canary-weight: "0"
```
Precedence (per the annotations page): canary-by-header, then canary-by-cookie, then canary-weight. A header or cookie value of `always` routes to the canary and `never` never does.

## Istio
```yaml
http:
  - match: [{ headers: { x-canary: { exact: "true" } } }]
    route: [{ destination: { host: api, subset: canary } }]
  - match: [{ headers: { cookie: { regex: ".*beta=1.*" } } }]
    route: [{ destination: { host: api, subset: canary } }]
  - route: [{ destination: { host: api, subset: stable } }]
```

## Practicalities
- Who sets the header? An edge proxy/auth layer sets it for employee identities, or a browser
  extension/feature-flag service sets the cookie. Do not let arbitrary clients opt into unreviewed code
  on sensitive systems: strip incoming `X-Canary` at the edge.
- Downstream services must forward the header for an end-to-end canary across multiple services.

## Verify
- [ ] Requests with the header hit canary pods (check response version header); others always hit stable.

## Checked

2026-10-28. Confirmed against the ingress-nginx canary annotations page (canary, canary-by-header, canary-by-header-value, canary-by-cookie, canary-weight, precedence header then cookie then weight, always and never values) and the Istio VirtualService reference (header match with exact and regex, subsets). Removed: the Gateway API example and description mention (no Gateway API source fetched), the Argo Rollouts setHeaderRoute and Istio header propagation claims.

Method: documentation only; no commands were run.
