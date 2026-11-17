---
id: computing-software.cloud-infrastructure-engineering.kubernetes.linkerd-lightweight-mesh-architecture
name: linkerd-lightweight-mesh-architecture
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, linkerd, service-mesh, linkerd2-proxy, mtls, trafficsplit, httproute, golden-metrics, tap, viz, destination-controller, identity-controller, lightweight-mesh]
level: advanced
status: docs-checked
description: "Linkerd's architecture (Rust micro-proxy, identity/destination controllers, default mTLS) and when its smaller feature set is a feature, not a gap, versus Istio."
sources: ["https://linkerd.io/2-edge/reference/architecture/", "https://linkerd.io/2-edge/features/automatic-mtls/", "https://linkerd.io/2-edge/features/traffic-split/", "https://linkerd.io/2-edge/reference/httproute/", "https://linkerd.io/2-edge/features/cni/", "https://linkerd.io/2-edge/features/server-policy/", "https://linkerd.io/2-edge/features/telemetry/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Linkerd — the lightweight-mesh architecture

**Goal:** know what Linkerd deliberately does *not* do, because that's the whole pitch —
fewer moving parts, a smaller proxy, mTLS with no configuration surface to get wrong. Use
this to decide Istio vs Linkerd, not just to deploy Linkerd blind. Resource-overhead
numbers are in `sidecar-resource-overhead-and-ambient-tradeoffs`.

## 1. Control plane: three small pieces, not one istiod
- **`identity`**: the CA. Accepts CSRs from proxies and returns signed TLS certs (they expire after 24
  hours) that chain to an issuer certificate and trust anchor you provide or `linkerd install` generates.
- **`destination`**: service discovery (where to send a request and the TLS identity expected), policy
  information about which requests are allowed, and service profile information for per-route metrics,
  retries and timeouts. Policy CRDs include `Server`, `HTTPRoute` and `GRPCRoute`.
- **`proxy-injector`**: the admission webhook that adds the `proxy-init` and `linkerd-proxy` containers to
  pods annotated `linkerd.io/inject: enabled` (on the pod or its namespace), with iptables rules redirecting
  traffic to the proxy (inbound port 4143, outbound port 4140). As of Linkerd 2.20 the proxy is a native
  sidecar container by default. The init container needs `CAP_NET_ADMIN`; where pods are not granted it,
  use Linkerd's CNI plugin to install the rules instead.
There is no fourth "policy brain" to reason about — this is the main cognitive-load
reduction versus Istio's istiod doing discovery + CA + xDS + validation all at once.

## 2. The proxy: `linkerd2-proxy`, written in Rust
- Purpose-built for the service mesh use case and, per the docs, "not designed as a general-purpose
  proxy". Features: zero-config HTTP, HTTP/2, WebSocket and arbitrary TCP proxying, automatic TLS,
  latency-aware layer-7 load balancing, layer-4 load balancing for non-HTTP traffic, Prometheus metrics
  and an on-demand tap API.
- Top-line ("golden") metrics (request volume, success rate, latency) are recorded by the proxy; the
  `viz` extension (`linkerd viz install`) adds the commands and dashboard, for example `linkerd viz stat`.

## 3. mTLS is not optional configuration — it's the default
Linkerd transparently applies mTLS to all TCP communication between meshed pods, except for traffic to
non-meshed pods and ports marked as skip ports (which bypass the proxy). There is no PeerAuthentication-style
resource to set PERMISSIVE or STRICT (Istio's PeerAuthentication has both modes). By default Linkerd allows
all traffic, and you restrict it with default-inbound-policy annotations and the policy CRDs.

## 4. Traffic management: deliberately smaller
- `TrafficSplit` (SMI) and the `linkerd-smi` extension are deprecated and will be removed; the docs point
  to dynamic request routing with `HTTPRoute` instead. TrafficSplit cannot be used with headless services.
- Linkerd's `HTTPRoute` filters are `RequestHeaderModifier`, `ResponseHeaderModifier` and `RequestRedirect`
  only, per the HTTPRoute reference, so Gateway API's `RequestMirror` filter is not documented as supported.
  Check the docs for your version before promising shadow traffic to a team.

## 5. When Linkerd is the right call
- Team wants mTLS and golden metrics with the smallest possible operational surface and
  does not need deep L7 policy, WASM extensibility, or multi-cluster federation with fine-
  grained control.
- Proxy CPU/memory overhead per pod matters (many small pods, cost-sensitive cluster): measure on your own
  traffic rather than quoting a vendor benchmark (see `sidecar-resource-overhead-and-ambient-tradeoffs`).
- Istio may fit better when you need request mirroring or other features Linkerd's route filters do not
  cover — see `istio-control-plane-architecture` and
  `istio-traffic-management-virtualservice-destinationrule`.

## Verify
- [ ] `linkerd check` passes with no warnings post-install.
- [ ] `linkerd viz stat deploy -n <ns>` shows live golden metrics with zero extra
  Prometheus config for a freshly injected deployment.
- [ ] `linkerd check` (identity section) reports the trust roots and issuer valid and issued by the trust root.
- [ ] Before promising mirroring or deep L7 policy to a team, confirmed against current
  Linkerd docs rather than assumed from this skill.

## Checked

Documentation release: Linkerd docs (linkerd/website linkerd.io/content/2-edge, repo commit 2026-10-15; linkerd2 edge release edge-26.10.1).
Confirmed in reference/architecture, features/automatic-mtls, features/cni, features/server-policy, features/traffic-split, features/telemetry and reference/httproute: control plane components and their roles, 24 hour proxy certificates, injection annotation, ports 4143 and 4140, native sidecar default from 2.20, CAP_NET_ADMIN and the CNI plugin, proxy feature list, viz golden metrics, mTLS scope and skip ports, policy CRDs (Server, HTTPRoute, GRPCRoute), TrafficSplit deprecation, HTTPRoute filter list. The Istio PeerAuthentication PERMISSIVE/STRICT modes were confirmed in the Istio reference.
Removed because the docs do not support them: the lighter-than-Envoy benchmark claim, the "no WASM/Lua" and EnvoyFilter remarks, the Prometheus wiring comparison, the PSA-exemption remark, and the claim that `linkerd identity` compares issuer and trust anchor.

Method: documentation only; no commands were run.
