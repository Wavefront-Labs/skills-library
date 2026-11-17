---
id: computing-software.cloud-infrastructure-engineering.kubernetes.istio-traffic-management-virtualservice-destinationrule
name: istio-traffic-management-virtualservice-destinationrule
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, istio, envoy, virtualservice, destinationrule, canary, traffic-splitting, traffic-mirroring, circuit-breaking, outlier-detection, retries, timeouts, fault-injection, service-mesh, subset-routing]
level: advanced
status: docs-checked
description: "Canary traffic splits, shadow mirroring, retries/timeouts, and circuit-breaking with Istio VirtualService/DestinationRule, with the ordering and label gotchas that cause silent misroutes."
sources: ["https://istio.io/latest/docs/reference/config/networking/virtual-service/", "https://istio.io/latest/docs/reference/config/networking/destination-rule/", "https://istio.io/latest/docs/concepts/traffic-management/", "https://www.envoyproxy.io/docs/envoy/latest/intro/arch_overview/upstream/circuit_breaking", "https://www.envoyproxy.io/docs/envoy/latest/configuration/advanced/substitution_formatter"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Istio traffic management — canary, mirroring, circuit-breaking

**Goal:** move traffic between versions, copy it for testing, and stop a failing backend
from taking down its callers, using `VirtualService` and `DestinationRule` correctly. This
assumes sidecar injection and mTLS are already working (`sidecar-injection-and-mtls-enforcement`).
Gateway API's mesh-routing equivalent is `gateway-api-mesh-traffic-routing`.

## 1. Subsets are the unit everything else operates on
Before any split/mirror/circuit-break, define subsets in a `DestinationRule` keyed to pod
labels (usually a `version` label):
```yaml
apiVersion: networking.istio.io/v1
kind: DestinationRule
metadata: {name: reviews}
spec:
  host: reviews
  subsets:
  - {name: v1, labels: {version: v1}}
  - {name: v2, labels: {version: v2}}
```
**Gotcha**: a subset with zero matching pods is not rejected at apply time — requests routed to
it have no healthy upstream (Envoy flag `UH`, 503). Always confirm pod labels first: `kubectl get pods -L version`.

## 2. Canary / weighted traffic split
```yaml
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata: {name: reviews}
spec:
  hosts: [reviews]
  http:
  - route:
    - {destination: {host: reviews, subset: v1}, weight: 90}
    - {destination: {host: reviews, subset: v2}, weight: 10}
```
- Weights are **percentage of requests**, not percentage of pods — a v2 subset with one
  pod and v1 with ten still gets exactly 10% of traffic, concentrated on that one pod.
  Scale replicas to match expected load before raising weight.
- The first rule matching a request is used (the `http` list is ordered); a catch-all `match`-less route
  must be last or it swallows everything below it.
- For progressive automation (step weight on success-rate SLO) use Argo Rollouts or Flagger
  driving these same VirtualService weights — don't hand-step production canaries.

## 3. Traffic mirroring (shadow traffic)
```yaml
  http:
  - route:
    - {destination: {host: reviews, subset: v1}, weight: 100}
    mirror: {host: reviews, subset: v2}
    mirrorPercentage: {value: 100.0}
```
- Mirroring is best effort: the proxy does not wait for the mirror to respond, and the caller only sees v1's response. `mirrorPercentage` defaults to 100 percent when absent.
  Mirroring is for validating v2 under real load/data shape, not for A/B comparison of
  responses (log and diff out-of-band if you need that).
- **Side-effect risk**: mirroring literally duplicates the request, including any writes.
  Never mirror to a service that isn't idempotent or doesn't point at an isolated backend
  (separate DB, feature-flagged no-op writes) — this is the single most common mirroring
  incident.

## 4. Circuit breaking (outlier detection + connection pool limits)
```yaml
apiVersion: networking.istio.io/v1
kind: DestinationRule
metadata: {name: reviews}
spec:
  host: reviews
  trafficPolicy:
    connectionPool:
      tcp: {maxConnections: 100}
      http: {http1MaxPendingRequests: 50, maxRequestsPerConnection: 10}
    outlierDetection:
      consecutive5xxErrors: 5
      interval: 30s
      baseEjectionTime: 30s
      maxEjectionPercent: 50
```
- This is Envoy's **outlier detection**, not a classic app-level circuit breaker: it ejects
  individual *upstream endpoints* (pods) from the load-balancing pool, not the whole
  service. An endpoint stays ejected for `baseEjectionTime` multiplied by the number of times
  it has been ejected (default base time 30s), so repeat offenders stay out longer.
- `maxEjectionPercent` caps how much of the pool can be ejected at once (default 10 percent).
  Keep it below 100 or a correlated failure (bad deploy) can eject every endpoint and turn a
  degradation into a full outage; tune it against your real failure patterns.
- `connectionPool` limits are enforced by each client proxy independently (Envoy's circuit breaking is distributed and not coordinated), not cluster-wide — a client with 20
  replicas each capped at `maxConnections: 100` can still open 2000 connections to the
  backend. Multiply by replica count when sizing.
- Pair with `retries` (`attempts`, `perTryTimeout`, `retryOn`) and a request `timeout` in
  the same VirtualService — circuit breaking without a sane timeout just means slow
  failures eject endpoints slower than they should.

## Verify
- [ ] `kubectl get pods -L version` matches every subset label before touching weights.
- [ ] `istioctl analyze` reports no warnings about missing hosts or subsets.
- [ ] A synthetic 5xx storm on one pod gets it ejected (`istioctl proxy-config endpoint
  <client-pod> --cluster "outbound|...|v1|reviews"` shows it removed) without starving
  the whole service.
- [ ] Mirrored traffic hits only an isolated/idempotent backend — confirmed by reading the
  mirror target's own write path, not assumed.

## Checked
2026-10-26. Checked against the istio/api networking v1alpha3 protos (the source of the VirtualService and DestinationRule references) and the Envoy circuit-breaking docs. Confirmed: the first matching http rule is used; `mirror` plus `mirrorPercentage` (mirrored traffic is best effort and the response is not awaited; absent means 100 percent); outlier detection fields `consecutive5xxErrors`, `interval` (default 10s), `baseEjectionTime` (default 30s), `maxEjectionPercent` (default 10 percent); connection pool fields `maxConnections`, `http1MaxPendingRequests`, `maxRequestsPerConnection`; Envoy describes its circuit breaking as fully distributed and not coordinated; UH is a 503. Corrected: ejection time grows linearly (base time times the number of ejections), not by doubling; removed the 50 percent ceiling recommendation and the `-shadow` Host suffix note, which no fetched doc covers.
Method: documentation only; no commands were run.
