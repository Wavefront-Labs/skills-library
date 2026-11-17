---
id: computing-software.cloud-infrastructure-engineering.istio.istio-gateway-api-httproute
name: istio-gateway-api-httproute
category: computing-software
field: cloud-infrastructure-engineering
product: istio
tags: [istio, gateway-api, httproute, gatewayclass]
level: practitioner
status: docs-checked
description: "Expose and route services using Gateway and HTTPRoute with gatewayClassName istio, and check Programmed and Accepted conditions."
sources: ["https://istio.io/latest/docs/tasks/traffic-management/ingress/gateway-api/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Istio implements the Gateway API; creating a `Gateway` auto-deploys a gateway proxy for it.

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata: {name: web-gw}
spec:
  gatewayClassName: istio
  listeners:
  - {name: http, port: 80, protocol: HTTP, allowedRoutes: {namespaces: {from: Same}}}
---
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata: {name: web}
spec:
  parentRefs: [{name: web-gw}]
  hostnames: ["web.example.com"]
  rules:
  - matches: [{path: {type: PathPrefix, value: /}}]
    backendRefs: [{name: web, port: 8080}]
```

Gotchas: the Gateway API CRDs are not installed by default on most clusters; install them first. For east-west (mesh) routing, `parentRefs` point at a Service instead of a Gateway.

Verify: `kubectl wait --for=condition=programmed gateways.gateway.networking.k8s.io web-gw` succeeds, the address in the Gateway's `status.addresses[0].value` answers, and curl with the `web.example.com` Host header returns 200.

## Checked

2026-11-03. Confirmed in the Istio Gateway API task: `gatewayClassName: istio`, `allowedRoutes`, `parentRefs`, `kubectl wait ... --for=condition=programmed`, `status.addresses[0].value`, CRDs not installed by default, and mesh routing via a Service `parentRef`. Removed: the `status.parents[].conditions` check, the `allowedRoutes` default claim and the ReferenceGrant advice (not on the page).

Method: documentation only; no commands were run.
