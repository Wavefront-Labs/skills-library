---
id: computing-software.cloud-infrastructure-engineering.kubernetes.gateway-api-advanced-routing-and-mesh
name: gateway-api-advanced-routing-and-mesh
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, gateway-api, httproute, grpcroute, tlsroute, referencegrant, gamma, cross-namespace, tls-passthrough, service-mesh, multi-tenant]
level: advanced
status: docs-checked
description: "Gateway API past the basic HTTPRoute: cross-namespace delegation with ReferenceGrant, TLSRoute passthrough, GRPCRoute, and GAMMA's mesh-traffic reuse of the same resources."
sources: ["https://gateway-api.sigs.k8s.io/reference/api-types/referencegrant/", "https://gateway-api.sigs.k8s.io/reference/api-types/tlsroute/", "https://gateway-api.sigs.k8s.io/reference/api-types/grpcroute/", "https://gateway-api.sigs.k8s.io/docs/mesh/gamma/", "https://gateway-api.sigs.k8s.io/docs/mesh/mesh-overview/", "https://gateway-api.sigs.k8s.io/docs/concepts/versioning/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Gateway API advanced routing — cross-namespace delegation, TLS passthrough, and GAMMA

**Goal:** use Gateway API's multi-tenant delegation model correctly (the thing it exists for,
beyond "nicer Ingress"), and know where it now also covers east-west mesh traffic.

**Relation to existing coverage:** basic `HTTPRoute`/`Gateway`/`GatewayClass` mechanics and
why to prefer Gateway API over Ingress are in
`computing-software.cloud-infrastructure-engineering.kubernetes.k8s-networking-and-ingress`.
This skill covers the parts that only matter in a real multi-team platform.

## 1. The role split, and why cross-namespace needs a grant
Gateway API's core design: the **platform team** owns `GatewayClass`/`Gateway` (the
listener, the TLS cert, the shared LB); **app teams** own `HTTPRoute`/`GRPCRoute`/`TLSRoute`
in their own namespaces, attaching to the shared Gateway via `parentRefs`. This only works
safely across namespace boundaries because of an explicit **trust handshake**:
```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: ReferenceGrant
metadata: {name: allow-shop-routes, namespace: gateway-infra}   # lives in the namespace of the referenced Service
spec:
  from: [{group: gateway.networking.k8s.io, kind: HTTPRoute, namespace: shop}]
  to: [{group: "", kind: Service}]
```
- Without a `ReferenceGrant` in the **target** namespace, a route in another namespace
  referencing a backend Service there is rejected (`ResolvedRefs: False`,
  reason `RefNotPermitted`) — this is deliberate: no namespace can be forced to accept
  traffic routing from another without opting in. The most common "my HTTPRoute isn't
  working" bug in a multi-tenant setup is a missing `ReferenceGrant`, not a routing mistake.
- Gateway's own listener can also restrict which namespaces may attach routes at all via
  `allowedRoutes.namespaces` (`Same` | `Selector` | `All`) — a second, coarser gate above
  `ReferenceGrant`'s per-reference one.

## 2. TLSRoute: SNI routing, passthrough by default
TLSRoute is GA and in the Standard channel since Gateway API v1.5.0 (earlier releases had it only as
`v1alpha2` in the experimental channel).
```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: TLSRoute
metadata: {name: db-passthrough, namespace: shop}
spec:
  parentRefs: [{name: public, namespace: gateway-infra, sectionName: tls-passthrough}]
  hostnames: [db.example.com]
  rules: [{backendRefs: [{name: postgres-proxy, port: 5432}]}]
```
- Routes by **SNI**. In `Passthrough` mode the Gateway does not terminate TLS and the backend handles its
  own cert. Needed for protocols where the Gateway shouldn't (or can't) see plaintext: raw TLS
  services, mTLS-protected backends that must keep client-presented certs, non-HTTP TLS
  protocols.
- Attach it to a `protocol: TLS` listener whose `tls.mode` is `Passthrough`. Every implementation
  claiming TLSRoute must support `Passthrough`; `Terminate` mode (decrypt at the Gateway, plain TCP to the
  backend) is the optional `TLSRouteModeTerminate` feature, and two listeners with different modes on one
  port is `TLSRouteModeMixed`. Mixing the modes up is the usual setup mistake.

## 3. GRPCRoute — first-class gRPC, not HTTP-shaped workarounds
- GA and in the Standard channel since v1.1.0. Matches on gRPC `service` and `method` (for example
  `service: com.example.User`, `method: Login`) instead of encoding them as an HTTP path such as
  `/package.Service/Method`.
- Backends use `backendRefs` as in `HTTPRoute`.

## 4. GAMMA — Gateway API for east-west mesh traffic
- The GAMMA (Gateway API for Mesh Management and Administration) initiative started in 2022 to use
  Gateway API for east/west traffic. A route's `parentRefs` points at a `Service` directly (instead of
  a `Gateway`), meaning "apply this to any traffic directed to the Service". Once any Route is attached
  to a Service, requests that match none of its Routes are rejected; with no Routes attached the mesh's
  default behaviour applies. The mesh-support work has been in the Standard channel since v1.1.0 and is
  considered GA.
- Practical effect: a platform standardizing on Gateway API can, as mesh vendors adopt
  GAMMA, express both ingress and mesh traffic splitting with one resource type —
  reduces the two-API-surfaces problem described in
  `computing-software.cloud-infrastructure-engineering.kubernetes.service-mesh-sidecar-networking-mtls`.
  Confirm support against the specific mesh product's conformance report for the version in use.

## Debug routine
```bash
kubectl get gateway,httproute,grpcroute,tlsroute,referencegrant -A
kubectl describe httproute <name> -n <ns>   # check Accepted / ResolvedRefs conditions and reasons
kubectl get gateway <name> -n gateway-infra -o jsonpath='{.status.listeners}'
```

## Verify
- [ ] A cross-namespace route's `ResolvedRefs` condition is `True` — if `False` with reason
  `RefNotPermitted`, the fix is a `ReferenceGrant` in the target namespace, not the route
  itself.
- [ ] TLSRoute passthrough is confirmed by capturing that the Gateway never decrypts (no cert
  mismatch error at the Gateway layer; the backend's own cert is what the client sees).
- [ ] GRPCRoute method-level matching is tested against an actual gRPC client, not just
  `curl`-based HTTP/2 probing which doesn't exercise the gRPC-specific matcher.
- [ ] If GAMMA is in use, confirm which specific resource (`HTTPRoute` with a `Service`
  `parentRef`) is the one actually enforced by the mesh's current version — don't assume
  full parity with the ingress-facing behavior.

## Checked

Documentation release: Gateway API docs (kubernetes-sigs/gateway-api site/content and apis/v1, latest release v1.6.3, repo commit 2026-10-23; v1.7.0 is at release-candidate stage).
Confirmed: ReferenceGrant is in the Standard channel (docs use `v1`; `v1beta1` also exists); route reason `RefNotPermitted`; TLSRoute Standard since v1.5.0 with Passthrough/Terminate modes and the three feature names; GRPCRoute Standard since v1.1.0 with service/method match; GAMMA Service parentRef semantics and the "unmatched requests are rejected" rule; `allowedRoutes.namespaces.from` values.
Corrected: TLSRoute apiVersion and channel (was `v1alpha2`/experimental), ReferenceGrant apiVersion, the claim that passthrough needs a listener protocol distinct from `HTTPS` (it is `TLS` with `tls.mode: Passthrough`), and the vague GAMMA maturity text.

Method: documentation only; no commands were run.
