---
id: computing-software.software-engineering.api-design.grpc-load-balancing-and-keepalive
name: grpc-load-balancing-and-keepalive
category: computing-software
field: software-engineering
product: api-design
tags: [api-design, grpc, grpc-load-balancing, grpc-keepalive, round-robin, xds, http2]
level: advanced
status: docs-checked
description: "Balance long-lived gRPC HTTP/2 connections with client-side round_robin or a proxy, configure keepalive and max connection age, and avoid the one-backend hotspot."
sources: ["https://grpc.io/blog/grpc-load-balancing/", "https://grpc.io/docs/guides/keepalive/", "https://github.com/grpc/grpc/blob/master/doc/load-balancing.md", "https://kubernetes.io/docs/concepts/services-networking/service/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# gRPC client-side load balancing and keepalive

## The problem
gRPC multiplexes all RPCs over one long-lived HTTP/2 connection. An L4 load balancer (such as a
Kubernetes ClusterIP Service) balances **connections**, so each client pins to one backend; new pods get no
traffic until clients reconnect.

## Options
1. **Client-side LB**: resolve all backend addresses and spread RPCs.
   ```go
   conn, _ := grpc.NewClient("dns:///orders.default.svc.cluster.local:50051",
       grpc.WithDefaultServiceConfig(`{"loadBalancingConfig":[{"round_robin":{}}]}`))
   ```
   `pick_first` is the default policy; `round_robin` opens a subchannel to every resolved address.
   In Kubernetes use a **headless Service** (`clusterIP: None`) so DNS returns pod IPs. DNS
   re-resolution can lag behind pod changes, so pair with server
   `MaxConnectionAge` to force periodic reconnects.
2. **L7 proxy / mesh**: Envoy, Linkerd, Istio, or an HTTP/2-aware ingress balance per request. No
   client changes; extra hop.
3. **xDS / proxyless**: clients get endpoints from an xDS control plane.

## Server-side settings (Go names; equivalents exist in all languages)
```go
grpc.KeepaliveParams(keepalive.ServerParameters{
    MaxConnectionAge: 5 * time.Minute, MaxConnectionAgeGrace: 30 * time.Second,
    Time: 2 * time.Hour, Timeout: 20 * time.Second}),
grpc.KeepaliveEnforcementPolicy(keepalive.EnforcementPolicy{MinTime: 30 * time.Second, PermitWithoutStream: true})
```

## Client keepalive
Detects dead connections through NATs/firewalls that silently drop idle flows:
`keepalive.ClientParameters{Time: 30*time.Second, Timeout: 10*time.Second, PermitWithoutStream: true}`.
Client `Time` must be >= server `MinTime`, or the server sends GOAWAY `too_many_pings`
and closes the connection.

## Verify
Scale the backend from 2 to 6 pods under load; per-pod RPS (from server metrics) should even out
within `MaxConnectionAge`. Check logs for `too_many_pings`.

## Checked
2026-11-01. Confirmed against the gRPC keepalive guide (MAX_CONNECTION_AGE, grace, 2-hour default ping time, GOAWAY with too_many_pings), the gRPC load-balancing blog and doc (pick_first default, round_robin, L4 vs L7, Envoy/Linkerd/Istio) and the Kubernetes Service page (ClusterIP). Removed: the Go re-resolve interval, ENHANCE_YOUR_CALM, AWS NLB and Traffic Director names.
Method: documentation only; no commands were run.
