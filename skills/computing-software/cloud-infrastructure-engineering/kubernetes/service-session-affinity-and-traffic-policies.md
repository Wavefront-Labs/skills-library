---
id: computing-software.cloud-infrastructure-engineering.kubernetes.service-session-affinity-and-traffic-policies
name: service-session-affinity-and-traffic-policies
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, services, sessionaffinity, internaltrafficpolicy, externaltrafficpolicy, topology-aware-routing, trafficdistribution, cross-zone-traffic]
level: advanced
status: docs-checked
description: "Steer Service traffic: sessionAffinity ClientIP, internal/externalTrafficPolicy Local, and topology-aware routing / trafficDistribution PreferClose."
sources: ["https://kubernetes.io/docs/reference/networking/virtual-ips/", "https://kubernetes.io/docs/concepts/services-networking/service-traffic-policy/", "https://kubernetes.io/docs/concepts/services-networking/topology-aware-routing/", "https://kubernetes.io/docs/concepts/services-networking/service/#traffic-distribution"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Session affinity and Service traffic policies

## sessionAffinity
```yaml
spec:
  sessionAffinity: ClientIP
  sessionAffinityConfig: {clientIP: {timeoutSeconds: 10800}}
```
kube-proxy selects the endpoint from the client IP address. `timeoutSeconds` defaults to 10800
(3 hours). Behind SNAT or an ingress, all clients share the proxy's IP, so one pod can receive
everything. There is no cookie-based affinity at this layer; do that in an ingress or mesh.

## internalTrafficPolicy: Local
Stable since 1.26. kube-proxy uses only node-local endpoints for traffic that originates inside
the cluster; if the node has no local endpoint, the traffic is dropped (it does not fall back to
other nodes). Used for node-local agents (DaemonSet collectors).

## externalTrafficPolicy: Local (NodePort/LoadBalancer)
- Load balancer health checks decide which nodes receive traffic; with `Local`, a node without
  a ready local endpoint should fail its health check and be taken out of rotation. How health
  checks are implemented is decided by the cloud provider integration.
- Uneven pod spread leads to uneven load because balancing happens per node.
- With ProxyTerminatingEndpoints (stable in 1.28), if every local endpoint on the node is
  terminating, kube-proxy still forwards to those terminating endpoints, so draining works while
  the load balancer notices the failing health check.

## trafficDistribution
`.spec.trafficDistribution` expresses a routing preference; it is not a guarantee.
- `PreferSameZone`: prefer endpoints in the client's zone; if the zone has none, traffic goes
  cluster-wide. The EndpointSlice controller sets `hints` and kube-proxy uses them.
- `PreferSameNode`: prefer endpoints on the client's node, then same zone, then cluster-wide.
- `PreferClose` is a deprecated alias for `PreferSameZone`.
- Feature-gate history: ServiceTrafficDistribution (PreferClose) alpha 1.30, beta 1.31, stable
  1.33; PreferSameTrafficDistribution (the two new values) alpha 1.33, beta 1.34, stable 1.35.
- If no value is set, traffic is spread evenly across all endpoints.
- If `internalTrafficPolicy` or `externalTrafficPolicy` is `Local`, that policy takes precedence
  for the matching traffic type.
```yaml
spec:
  trafficDistribution: PreferSameZone
```
- The older Topology Aware Routing (annotation `service.kubernetes.io/topology-mode: Auto`)
  splits endpoints across zones in proportion to allocatable CPU, has fallback safeguards for
  small endpoint counts, and takes precedence over `trafficDistribution` if both are set.
- With `PreferSameZone` you are responsible for avoiding overload of a zone that has few
  endpoints; combine with `topologySpreadConstraints` and autoscaling.

## Choosing
| Goal | Use |
|---|---|
| sticky clients without an L7 proxy | sessionAffinity ClientIP |
| talk to the node's own agent | internalTrafficPolicy: Local |
| client IP preservation at LB | externalTrafficPolicy: Local |
| cut cross-zone traffic, keep failover | trafficDistribution: PreferSameZone |

## Verify
- [ ] Cross-zone traffic drops after enabling the preference, and no zone's pods are saturated.

## Checked

2026-10-23, Kubernetes documentation (kubernetes/website main, v1.36 docs) and kubernetes/kubernetes source. Confirmed: sessionAffinity ClientIP and the 10800 second default (virtual-ips page), internalTrafficPolicy Local dropping traffic without local endpoints, ProxyTerminatingEndpoints stable in 1.28, the trafficDistribution values, deprecation of PreferClose, precedence rules, and feature-gate stages for ServiceTrafficDistribution and PreferSameTrafficDistribution (feature-gate reference). Removed the cloud per-GB price, the grep command and the unconfirmed source-IP and hop-count claims for externalTrafficPolicy.

Method: documentation only; no commands were run.
