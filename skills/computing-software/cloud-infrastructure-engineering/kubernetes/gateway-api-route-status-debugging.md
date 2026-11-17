---
id: computing-software.cloud-infrastructure-engineering.kubernetes.gateway-api-route-status-debugging
name: gateway-api-route-status-debugging
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, gateway-api, route-status, resolvedrefs, httproute, referencegrant]
level: practitioner
status: docs-checked
description: "Debug Gateway API routes from status: parent Accepted and ResolvedRefs conditions, listener and Gateway Programmed status, and the common reason codes."
sources: ["https://gateway-api.sigs.k8s.io/docs/concepts/troubleshooting/", "https://gateway-api.sigs.k8s.io/reference/api-spec/main/spec/", "https://github.com/kubernetes-sigs/gateway-api/blob/main/apis/v1/shared_types.go", "https://gateway.envoyproxy.io/docs/tasks/operations/egctl/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Debugging Gateway API route status

## Read status on each layer
```bash
kubectl get gatewayclass
kubectl describe gateway -n infra prod          # status conditions per Gateway and listener
kubectl describe httproute -n shop web          # status.parents[] conditions
```
- GatewayClass: `Accepted` (controller claimed it).
- Gateway: `Accepted`, `Programmed` (data plane configured, address assigned), and per listener
  `Accepted`, `Programmed`, `ResolvedRefs`, `Conflicted`, plus `attachedRoutes` count.
- Route: one entry per parentRef with `Accepted` and `ResolvedRefs`.

## Route reasons
| Condition/reason | Meaning | Fix |
|---|---|---|
| Accepted False `NotAllowedByListeners` | listener `allowedRoutes` excludes this namespace or kind | set `allowedRoutes.namespaces.from: Selector/All` |
| Accepted False `NoMatchingListenerHostname` | route hostnames do not intersect listener hostname | align hostnames |
| Accepted False `NoMatchingParent` | `sectionName`/`port` matches no listener | fix parentRef |
| ResolvedRefs False `BackendNotFound` | Service missing | create it or fix name/port |
| ResolvedRefs False `RefNotPermitted` | cross-namespace backend without ReferenceGrant | add ReferenceGrant in backend namespace |
| ResolvedRefs False `InvalidKind` | unsupported backend kind | use Service or supported kind |
| no status at all | no controller processes this parent | wrong gateway name/namespace, or class not accepted |

Accepted True with ResolvedRefs False: the route is attached but requests sent to the invalid backend
get a 500 (the spec requires 500 for invalid backendRefs, proportional to their weight).

## Listener side
`attachedRoutes: 0` on the listener while the route says Accepted means you are looking at
another listener; check `sectionName`.

## Data plane
```bash
kubectl get gateway prod -n infra -o jsonpath='{.status.addresses[*].value}'
curl -sv -H 'Host: shop.example.com' http://<address>/
```
Implementation-specific: `egctl config envoy-proxy route` (Envoy Gateway),
`istioctl proxy-config routes` (Istio).

## Checked

Documentation release: Gateway API docs (kubernetes-sigs/gateway-api site/content and apis/v1, latest release v1.6.3, repo commit 2026-10-23; v1.7.0 is at release-candidate stage).
Confirmed in apis/v1 shared_types.go and gateway_types.go: route conditions `Accepted` and `ResolvedRefs` with reasons `NotAllowedByListeners`, `NoMatchingListenerHostname`, `NoMatchingParent`, `BackendNotFound`, `RefNotPermitted`, `InvalidKind`; Gateway and listener conditions `Accepted`, `Programmed`, `ResolvedRefs`, `Conflicted`; the 500 response rule for invalid backendRefs; `egctl config envoy-proxy route` and `istioctl proxy-config routes` exist in vendor docs.
Removed: the `yq` pipelines (no documented grammar to confirm).

Method: documentation only; no commands were run.
