---
id: computing-software.cloud-infrastructure-engineering.kubernetes.istio-control-plane-architecture
name: istio-control-plane-architecture
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, istio, istiod, envoy, xds, service-mesh, control-plane, pilot, citadel, galley, revisions, canary-upgrade, sidecar-mode, ambient-mode]
level: advanced
status: gated
description: "How istiod's xDS, discovery and cert-issuing roles fit together, and how sidecar and ambient modes differ at the control-plane level."
sources: ["https://istio.io/latest/docs/ops/deployment/architecture/", "https://istio.io/latest/docs/setup/upgrade/canary/", "https://istio.io/latest/docs/reference/commands/pilot-discovery/", "https://istio.io/latest/docs/ambient/architecture/control-plane/", "https://istio.io/latest/news/releases/1.24.x/announcing-1.24/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Istio control plane architecture — what istiod actually does

**Goal:** reason about Istio as a system, not a YAML dialect. Know what talks to what,
what breaks when istiod is slow or down, and what changed between the old multi-binary
architecture and today's single `istiod`. This is the architecture map; mTLS mechanics are
in `sidecar-injection-and-mtls-enforcement`, ambient's data plane in
`istio-ambient-mode-ztunnel-waypoint`, traffic shaping in
`istio-traffic-management-virtualservice-destinationrule`.

## 1. From four binaries to one
Older Istio shipped Pilot, Citadel, Galley and Mixer as separate deployments (gated: unconfirmed, source is paywalled or blocked); the current docs describe a single `istiod` that provides service discovery, configuration and certificate management. The old release history was not in the fetched docs, so treat any four-box architecture diagram as describing a long-unsupported version.

`istiod` does three jobs:
1. **Service discovery** — watches the Kubernetes API (Services, Endpoints/EndpointSlices,
   Pods) and Istio CRDs (VirtualService, DestinationRule, Gateway, PeerAuthentication,
   AuthorizationPolicy, Sidecar) and turns them into Envoy configuration.
2. **xDS server** — pushes that configuration to every Envoy sidecar/ztunnel over gRPC
   (ADS: Aggregated Discovery Service — one stream carrying CDS/LDS/RDS/EDS instead of four).
3. **Certificate authority** — issues and rotates workload certs via SDS (Secret Discovery
   Service), the same xDS transport.

## 2. The data plane is independent of the control plane — mostly
Envoy sidecars are generally expected to keep proxying with the last config they received if istiod is unreachable, while new pods, new routes and cert rotation stall (gated: unconfirmed, source is paywalled or blocked; the fetched docs do not state outage behaviour). Test it in a non-production cluster before relying on it. Inspect sync state with:
```bash
istioctl proxy-status          # SYNCED / STALE / NOT SENT per proxy
kubectl -n istio-system get pods -l app=istiod
```
A fleet showing STALE while istiod is up is worth checking against `istiod` logs for push errors before assuming a networking problem.

## 3. Revisions, not just versions
Istio supports **canary control-plane upgrades** via revisions: install a second `istiod`
revision (for example `canary`, which runs as `istiod-canary`) alongside the running one,
then label a test namespace `istio.io/rev=canary` and remove `istio-injection` (the
`istio-injection` label takes precedence over `istio.io/rev` for backward compatibility, so
leaving both set keeps the old revision). Restart pods to re-inject. Revision tags
(`istioctl tag set <tag> --revision <rev>`) add an indirection so namespaces point at a tag.
Full upgrade mechanics (including proxy version skew limits) are in `service-mesh-upgrade-strategy`.

## 4. Sidecar mode vs ambient mode, at the control-plane level
- **Sidecar mode**: every pod gets its own Envoy; istiod pushes per-pod config; identity
  and L7 policy are enforced in-process with the app.
- **Ambient mode** (GA as of Istio 1.24):
  removes the sidecar. A per-node **ztunnel** DaemonSet handles L4 (mTLS, basic
  authorization) for every pod on the node; an optional per-namespace **waypoint** proxy
  (still Envoy) handles L7 (retries, HTTP routing, telemetry) only for namespaces that need
  it. istiod now pushes config to ztunnels and waypoints instead of per-pod sidecars — fewer,
  larger config recipients, which changes your capacity-planning math (node count, not pod
  count, drives ztunnel config size).

## 5. What to watch operationally
- `istiod` load grows with the amount of configuration pushed to each proxy (gated: unconfirmed, source is paywalled or blocked). A `Sidecar` resource that limits each workload's visible config is the usual lever for large clusters; the threshold is not documented, so watch istiod memory and push latency.
- `pilot_proxy_convergence_time` (delay between a config change and a proxy receiving all
  required configuration) and `pilot_xds_push_time` (time to push lds, rds, cds and eds) are
  istiod metrics listed in the pilot-discovery reference; alert on sustained growth.
- Istio resource validation is served by an istiod-backed webhook (the istioctl install docs
  mention an `istiod-default-validator` webhook configuration); behaviour when istiod is down
  is not documented in the fetched pages (gated: unconfirmed, source is paywalled or blocked).

## Verify
- [ ] `istioctl proxy-status` shows SYNCED fleet-wide after any config or istiod change.
- [ ] You can state, for your cluster, whether it's sidecar or ambient mode and why.
- [ ] `istioctl version` shows no more than one minor version of proxy/control-plane skew.
- [ ] You know which Prometheus dashboard shows istiod push latency, and it's not red.

## Checked
2026-10-26. Checked against the istio.io docs source (repository istio/istio.io, last commit 2026-10-23). Confirmed: istiod provides service discovery, configuration and certificate (CA) management; ambient GA in 1.24; revisioned control planes (`istiod-<revision>`, namespace label `istio.io/rev`); `istio-injection` takes precedence over `istio.io/rev` for backward compatibility, so it must be removed (the old text called the labels mutually exclusive); metrics `pilot_proxy_convergence_time` and `pilot_xds_push_time` exist in the pilot-discovery reference. Not confirmed in any fetched page and marked gated: the pre-1.5 component history, the cached-config outage behaviour, the validation-webhook dependency and the Sidecar-scoping advice.
Method: documentation only; no commands were run.
