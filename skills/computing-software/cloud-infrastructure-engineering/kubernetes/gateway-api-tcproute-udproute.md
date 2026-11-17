---
id: computing-software.cloud-infrastructure-engineering.kubernetes.gateway-api-tcproute-udproute
name: gateway-api-tcproute-udproute
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, gateway-api, tcproute, udproute, layer4, experimental-channel]
level: practitioner
status: docs-checked
description: "Route raw TCP and UDP traffic through a Gateway with TCPRoute and UDPRoute listeners, and know their experimental status and implementation support."
sources: ["https://gateway-api.sigs.k8s.io/reference/api-types/tcproute/", "https://gateway-api.sigs.k8s.io/reference/api-types/udproute/", "https://gateway-api.sigs.k8s.io/guides/user-guides/tcp/", "https://gateway-api.sigs.k8s.io/docs/concepts/versioning/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TCPRoute and UDPRoute

Layer-4 routes for protocols with no HTTP or TLS SNI to route on (databases, DNS, VoIP, games). Both
are GA (`v1`) and in the Standard channel since Gateway API v1.6.0; on earlier releases they were
`v1alpha2` in the experimental channel.

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata: {name: l4, namespace: infra}
spec:
  gatewayClassName: eg
  listeners:
  - {name: postgres, protocol: TCP, port: 5432, allowedRoutes: {namespaces: {from: All}}}
  - {name: dns, protocol: UDP, port: 53, allowedRoutes: {namespaces: {from: All}}}
---
apiVersion: gateway.networking.k8s.io/v1
kind: TCPRoute
metadata: {name: pg, namespace: data}
spec:
  parentRefs: [{name: l4, namespace: infra, sectionName: postgres}]
  rules:
  - backendRefs: [{name: postgres, port: 5432}]
---
apiVersion: gateway.networking.k8s.io/v1
kind: UDPRoute
metadata: {name: dns, namespace: infra}
spec:
  parentRefs: [{name: l4, sectionName: dns}]
  rules:
  - backendRefs: [{name: coredns-ext, port: 53}]
```

## Rules
- Traffic is classified only by the listener's protocol and port: neither route has hostnames, matches
  or filters. Each has a single rule with 1 to 16 backendRefs (TCPRoute weights are Extended support);
  use one listener per backend set, or TLSRoute with SNI for TLS traffic.
- Without `sectionName` or `port`, a TCPRoute attaches to every TCP listener on the Gateway.
- Cross-namespace backendRefs need a ReferenceGrant in the backend namespace.
- Support varies: check your implementation's conformance report for TCPRoute and UDPRoute. A
  Gateway can offer DNS on TCP and UDP 53 only if the implementation supports both protocols on one port.

## Debug
`kubectl describe tcproute pg -n data`: `Accepted` and `ResolvedRefs` conditions per parent.
`NotAllowedByListeners` means the listener's `allowedRoutes` or kind list excludes it.

## Verify
`nc -vz <gateway-address> 5432` connects; `dig @<gateway-address> example.internal` answers.

## Checked

Documentation release: Gateway API docs (kubernetes-sigs/gateway-api site/content and apis/v1, latest release v1.6.3, repo commit 2026-10-23; v1.7.0 is at release-candidate stage).
Confirmed: TCPRoute and UDPRoute GA with Standard channel since v1.6.0, apiVersion `v1`; single rule with 1 to 16 backendRefs; no hostnames/matches/filters; attachment by `sectionName` to named TCP or UDP listeners; the Gateway must allow the route's namespace.
Corrected: channel and apiVersion (were experimental `v1alpha2`).

Method: documentation only; no commands were run.
