---
id: computing-software.cloud-infrastructure-engineering.kubernetes.sidecar-resource-overhead-and-ambient-tradeoffs
name: sidecar-resource-overhead-and-ambient-tradeoffs
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, service-mesh, sidecar, resource-overhead, cpu, memory, requests-limits, ambient-mode, linkerd2-proxy, envoy, cost, capacity-planning, latency-overhead]
level: advanced
status: docs-checked
description: "What a sidecar proxy costs per pod in CPU/memory/latency, how that multiplies cluster-wide, and when ambient mode or a sidecar-free mesh changes the math."
sources: ["https://istio.io/latest/docs/ops/deployment/performance-and-scalability/", "https://istio.io/latest/docs/ambient/overview/", "https://istio.io/latest/docs/ops/configuration/mesh/configuration-scoping/", "https://istio.io/latest/docs/setup/additional-setup/sidecar-injection/", "https://linkerd.io/2/reference/architecture/", "https://docs.cilium.io/en/stable/security/network/proxy/envoy/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sidecar resource overhead and ambient-mode tradeoffs

**Goal:** put real numbers against "sidecars are expensive" so you can decide, per
cluster, whether that is actually true for your workload shape, and know which lever
(right-sizing, ambient mode, a lighter proxy) fixes it if it is.

## 1. Where the cost actually comes from
Every sidecar-injected pod gets its **own** proxy process:
- A CPU/memory **request** reserved per pod (the requests, not just limits, drive
  bin-packing), multiplied by every pod in the mesh.
- A **per-hop path cost**: Istio's performance page describes sidecar mode as client sidecar
  then server sidecar before the server, ambient mode as client-node ztunnel then
  server-node ztunnel, and ambient with a waypoint as a waypoint proxy between the
  ztunnels. Latency depends on traffic pattern and enabled features (Istio notes telemetry
  filters have a moderate impact), so load-test your own path and treat any vendor number
  as not yours.
- **Config push cost at scale**: `istiod` programs every proxy, and a proxy that can see
  every service holds more configuration. Istio recommends configuration scoping at large
  scale: the `Sidecar` resource's `egress.hosts` limits what a workload's sidecar imports,
  and `exportTo` lets service owners limit visibility. Do this before blaming the proxy.

## 2. Sizing the sidecar itself
- Istio's performance page reports, for Istio 1.24 at 1000 HTTP requests per second with
  1 KB payloads: a sidecar proxy with 2 worker threads uses about 0.20 vCPU and 60 MB; a
  waypoint proxy with 2 worker threads about 0.25 vCPU and 60 MB; a ztunnel about 0.06
  vCPU and 12 MB. Proxy memory grows with the number of listeners, clusters and routes it
  holds. Treat these as one data point from Istio's test setup, not as a sizing rule.
- Istio's `istio-discovery` chart (1.31.3) ships `global.proxy.resources` defaults of
  requests 100m CPU / 128Mi memory and limits 2000m CPU / 1024Mi memory. Set the
  mesh-wide default there and override outliers per workload with the
  `sidecar.istio.io/proxyCPU` / `proxyMemory` annotations; Istio's injection docs warn that
  setting a request annotation without the matching `proxyCPULimit` / `proxyMemoryLimit`
  leaves that limit unlimited.
- **Measure your own proxy**: `kubectl top pod --containers` (the `istio-proxy` or
  `linkerd-proxy` container) for a high-QPS and a low-QPS workload, rather than trusting
  defaults.
- Linkerd describes linkerd2-proxy as an ultralight micro-proxy written in Rust and
  purpose-built for Linkerd; it publishes no sizing numbers on the architecture page, so
  compare on your own workload.

## 3. What ambient mode / sidecar-free actually changes
- Istio ambient mode uses a per-node L4 proxy (`ztunnel`) and, optionally, per-namespace
  L7 proxies (waypoints): the cost shifts from per-pod to per-node plus waypoints only where
  L7 features are needed. With many small pods per node, one ztunnel's footprint is shared
  by all of them; the Istio numbers above show ztunnel at a fraction of a sidecar's CPU
  and memory at the same request rate.
- Latency does not simply improve: with a waypoint, traffic goes through an extra proxy
  between the ztunnels (Istio's latency section shows the three paths side by side). L4
  mTLS traffic with no waypoint uses ztunnels only. Measure both paths for your mix.
- Cilium's sidecar-free design (`cilium-service-mesh-sidecar-free`) applies L7 policy,
  Ingress and Gateway API handling through a per-node Envoy (embedded in the agent or the
  separate `cilium-envoy` DaemonSet), so L7 traffic depends on that node-level proxy; Cilium
  does not need a proxy for traffic that only needs L3/L4 policy.

## 4. Decision shortcut
- Many small, low-QPS pods, cost-sensitive cluster, need L7 features broadly: ambient mode or
  Linkerd are stronger candidates than classic sidecar Istio; benchmark them.
- Need deep per-route traffic shaping on most services: classic sidecar mode is the mode
  with per-workload L7 everywhere; pay the per-pod cost deliberately. Check Istio's
  feature-stage page for what ambient supports in your version.
- Mesh is mostly L4 (mTLS + basic policy), little L7 need: do not default to a sidecar mesh
  at all; see `when-not-to-use-a-service-mesh`.

## Verify
- [ ] `kubectl top pod --containers` (or Prometheus) gives real proxy CPU and memory for
  at least one high-QPS and one low-QPS workload, not assumed defaults.
- [ ] Cluster-wide sidecar resource *requests* (sum, not limits) are accounted for in node
  capacity planning.
- [ ] If evaluating ambient or sidecar-free, latency was measured end-to-end on your own
  traffic, not taken from a vendor blog.
- [ ] `Sidecar` resource scoping (Istio) or namespace isolation is in place before blaming
  per-proxy overhead for a slow mesh at scale.

## Checked
2026-10-27. Documentation releases: istio.io docs (main; performance page figures are for Istio 1.24, chart defaults read from Istio 1.31.3), Linkerd website architecture page, Cilium v1.20.4 Envoy proxy page.
Confirmed: sidecar/ztunnel/waypoint resource figures and latency path description, chart default requests/limits, `proxyCPU`/`proxyMemory` annotation caveat, configuration scoping resources, ambient layer split, Cilium per-node Envoy for L7.
Method: documentation only; no commands were run.
