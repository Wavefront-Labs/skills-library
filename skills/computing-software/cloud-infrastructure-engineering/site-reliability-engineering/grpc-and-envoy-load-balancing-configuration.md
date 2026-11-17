---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.grpc-and-envoy-load-balancing-configuration
name: grpc-and-envoy-load-balancing-configuration
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [grpc-lb-config, envoy-lb-policy, grpc, envoy, kubernetes-headless-service, outlier-detection, load-balancing]
level: practitioner
status: docs-checked
description: "Fix gRPC-on-Kubernetes imbalance and configure load balancing: headless service with round_robin service config, Envoy lb_policy, outlier detection, zone awareness."
sources: ["https://grpc.io/docs/guides/custom-load-balancing/", "https://github.com/grpc/grpc/blob/master/doc/service_config.md", "https://www.envoyproxy.io/docs/envoy/latest/api-v3/config/cluster/v3/cluster.proto", "https://sre.google/sre-book/load-balancing-datacenter/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# gRPC and Envoy load balancing configuration

## The gRPC + ClusterIP problem
gRPC multiplexes RPCs over long-lived HTTP/2 connections. A ClusterIP Service balances *connections* (L4),
so a client can stay pinned to one pod and new pods after a scale-up may get little traffic.

## Fix 1: client-side LB with a headless service
Use a headless Service (`clusterIP: None`) so DNS returns the pod IPs, then set the client's service config
to round robin. The gRPC service config reference shows the JSON form:
```json
{"loadBalancingConfig": [ { "round_robin": {} } ]}
```
Pass it through your language's default-service-config option and use the `dns:///` target. New pods appear
only as the client re-resolves, so have servers close long-lived connections periodically (look up your gRPC
language's max-connection-age setting; its values are not covered by the pages cited here).

## Fix 2: L7 proxy (Envoy / service mesh)
Envoy balances per request across the cluster's endpoints. Relevant `Cluster` fields in the v3 API:
```yaml
clusters:
- name: orders
  type: STRICT_DNS            # or EDS from a control plane
  lb_policy: LEAST_REQUEST    # also ROUND_ROBIN, RING_HASH, MAGLEV, RANDOM
  outlier_detection: {}       # ejection settings, see the OutlierDetection message
  common_lb_config:
    zone_aware_lb_config: { min_cluster_size: <N> }
```
The API notes that only RING_HASH, MAGLEV and LEAST_REQUEST have extra per-policy config (for example
`least_request_lb_config`; a choice count defaults to 2, giving two-choice selection), and that setting such a
config without the matching `lb_policy` errors at runtime.
## Fix 3: proxyless gRPC with xDS
With a service mesh control plane you cannot set a custom balancer in the service config; the control plane
delivers LB configuration to gRPC clients over xDS (gRPC custom load balancing guide). Check your control
plane's documentation for what it supports.

## Gotchas
- Tune outlier-detection ejection limits for small clusters, or it may eject too little to help.
- Ring hash and Maglev give request affinity; Maglev aims for minimal disruption when the host set changes.
  Use them only when affinity is needed.
- Client-side round_robin keeps sending to a draining pod until its connection closes; use the lame duck
  state so servers tell clients to stop (SRE Book, Load Balancing in the Datacenter).

## Verify
- [ ] Per-pod request rate is close to even after a scale-up.
- [ ] Killing a pod causes no client-visible errors beyond retries.

## Checked
2026-11-01. Confirmed in the gRPC service config reference (`loadBalancingConfig` round_robin), the gRPC custom load balancing guide (xDS delivery), the Envoy v3 Cluster reference (`lb_policy` values, `outlier_detection`, `common_lb_config`, `min_cluster_size`, per-policy config rules, choice count default 2, STRICT_DNS) and the SRE Book chapter on load balancing in the datacenter (lame duck state). Removed: Go client and server snippets, DNS re-resolve interval, Envoy HTTP/2 protocol option block (kept out, not confirmed), ejection numbers and the 10 percent default, Istio DestinationRule, xDS bootstrap and weighted_round_robin claims, and the 15 percent and PromQL checks.
Method: documentation only; no commands were run.
