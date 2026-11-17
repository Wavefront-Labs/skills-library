---
id: computing-software.cloud-infrastructure-engineering.kubernetes.multi-cluster-ingress-and-global-load-balancing
name: multi-cluster-ingress-and-global-load-balancing
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, multi-cluster-ingress, global-load-balancer, glbc, anycast, dns-based-failover, health-check, mci, multi-region, north-south-traffic, cdn, traffic-director]
level: advanced
status: docs-checked
description: "Route external traffic across regions and clusters with multi-cluster ingress and global load balancing, with health-based failover."
sources: ["https://cloud.google.com/kubernetes-engine/docs/concepts/multi-cluster-ingress", "https://docs.aws.amazon.com/global-accelerator/latest/dg/introduction-how-it-works.html", "https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover.html", "https://developers.cloudflare.com/load-balancing/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multi-cluster ingress — getting external traffic to the right cluster

**Goal:** route a client's request to whichever cluster/region should serve it right
now (nearest healthy one, or a weighted split), from outside the mesh. This is
north-south traffic (external client in); it's a different problem from
`computing-software.cloud-infrastructure-engineering.kubernetes.multi-cluster-service-mesh-federation`
(east-west, service-to-service) and from
`computing-software.cloud-infrastructure-engineering.kubernetes.submariner-multi-cluster-networking`
(pod network connectivity) — a fleet commonly needs this layer regardless of whether
it also federates its mesh.

## 1. The two mechanisms
- **DNS-based global load balancing**: a DNS service (Route 53 failover or weighted records
  with health checks, Cloudflare Load Balancing in DNS-only mode, or a dedicated GSLB product)
  resolves a hostname to the nearest or healthiest region's entry point based on client
  location and live health checks. DNS TTLs mean failover isn't instant: low TTLs trade faster
  failover for more DNS query volume, and some resolvers and clients cache longer anyway.
- **Anycast or edge-IP based**: one IP address is advertised from many points of presence and
  the network delivers the client to a nearby one, so failover needs no DNS change. GKE Multi
  Cluster Ingress creates Premium Tier external Application Load Balancers on global anycast
  IPs; AWS Global Accelerator gives static IP addresses that take traffic in at the edge
  location closest to the user and shifts new connections away from unhealthy endpoints.
  Check whether your provider's "global load balancer" is anycast or DNS-based under the hood.

## 2. Cluster-side wiring
- Cloud-managed options let one object front Services in several clusters. In GKE Multi
  Cluster Ingress, a `MultiClusterIngress` and `MultiClusterService` live in a config cluster;
  the controller tracks Pod endpoints in each cluster through network endpoint groups and
  programs one load balancer VIP with health checking and failover. GKE also offers
  multi-cluster Gateways through the Gateway API.
- Self-managed alternative: each cluster runs its own ingress controller with a
  public endpoint; an external DNS/GSLB layer (e.g. a GSLB appliance, or Route 53
  weighted/failover records) health-checks each cluster's endpoint directly and
  decides routing — more moving parts to own, more portable across clouds.
- **Health check granularity matters**: checking only "is the LB endpoint up" misses
  a cluster that's up but whose actual application backend is unhealthy — wire health
  checks to an application-meaningful endpoint (readiness-gated), not just a TCP/ingress
  liveness check.

## 3. Traffic splitting patterns
- **Weighted** — percentage split across regions for canary or capacity-balancing
  reasons, independent of health.
- **Latency/geo-based** — route to nearest region by client location; combine with
  health-based failover so a nearby-but-unhealthy region isn't preferred.
- **Active-passive** — all traffic to a primary region/cluster until its health check
  fails, then cutover to a standby; simplest but wastes standby capacity unless it's
  also serving some other traffic.

## Gotchas
- DNS caching at resolvers and clients (including some that ignore TTL on cache
  eviction policy) means "set TTL to 30s" does not guarantee a 30s failover for every
  client — test actual failover time with real client populations, not just `dig`
  against an uncached resolver.
- A global LB's own control plane/API is itself a dependency with its own failure mode
  — a provider-side outage of the GSLB/anycast layer can take down routing to *all*
  regions even though every regional cluster is healthy; know what that provider's own
  SLA and failure history looks like before treating this layer as infallible.
- Session affinity/sticky sessions interact badly with cross-region failover — a
  client mid-session routed to a now-unhealthy region may need to re-establish state;
  design for statelessness or externalized session state before relying on failover
  for a stateful workload.
- Cost: managed global load balancers and cross-region data transfer are billed separately;
  price the design for your cluster and region count before committing.

## Verify
- [ ] A simulated regional outage (fail the health check endpoint, not just the LB)
      causes traffic to shift to the remaining healthy region(s) within the expected
      time, measured from real client vantage points.
- [ ] Health checks target an application-meaningful endpoint, confirmed to actually
      fail when the backend is degraded (not just when the pod/ingress is down).
- [ ] DNS TTL and observed failover time are measured together, not assumed equal.
- [ ] Weighted/geo traffic splits are confirmed against real traffic logs to match the
      configured percentages/regions, not just the LB config intent.

## Checked
2026-10-27 against the GKE Multi Cluster Ingress concepts page, the AWS Global Accelerator "how it
works" page, the Route 53 DNS failover guide and the Cloudflare Load Balancing docs. Confirmed:
MCI's config cluster, `MultiClusterIngress`/`MultiClusterService` resources, NEG-based endpoint
tracking and anycast VIPs; Global Accelerator's static edge IPs and health-based failover;
Cloudflare's proxied and DNS-only modes. Fixed: Global Accelerator and GKE MCI were listed as
DNS-based, and prose source titles were replaced with URLs.
Method: documentation only; no commands were run.
