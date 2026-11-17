---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.network-latency-optimisation
name: network-latency-optimisation
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, performance-engineering, network-latency-optimisation, latency, keep-alive, http2, http3, tls-1-3, placement, cross-az-traffic]
level: practitioner
status: draft
description: "Cut network latency in cloud systems: placement and AZ affinity, connection reuse, TLS 1.3 and HTTP/2-3, edge termination, chattiness reduction and measuring RTT per hop."
sources: ["https://aws.amazon.com/blogs/networking-and-content-delivery/", "https://learn.microsoft.com/azure/virtual-network/accelerated-networking-overview", "https://cloud.google.com/compute/docs/networking/using-gvnic", "https://hpbn.co/", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/placement-groups.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Network latency optimisation

## Steps
1. **Measure each hop.** Break down a request with tracing and `curl -w
   '%{time_namelookup} %{time_connect} %{time_appconnect} %{time_starttransfer}\n'`:
   DNS, TCP, TLS, server time, transfer. Use `mtr` / `tcptraceroute` for path RTT, and
   cloud tools (AWS Network Manager Infrastructure Performance, Azure Connection Monitor,
   GCP Performance Dashboard) for inter-AZ/region baselines.
2. **Place compute near data and users.** Same region as the database; keep chatty services in
   the same AZ (zone-aware routing in Envoy/Istio, Kubernetes `trafficDistribution: PreferClose`
   or topology-aware hints) while keeping multi-AZ redundancy. Cross-AZ RTT is roughly
   0.5-2 ms and costs money; cross-region is tens to hundreds of ms.
3. **Reuse connections.** HTTP keep-alive and connection pools to databases and downstreams;
   gRPC/HTTP/2 multiplexing; avoid a new TLS handshake per request. Check pool sizes and idle
   timeouts against NAT and load balancer idle timeouts (AWS NLB 350 s, ALB default 60 s).
4. **Shorten handshakes.** TLS 1.3 (1-RTT, 0-RTT resumption only for idempotent requests),
   OCSP stapling, session tickets; HTTP/3 (QUIC) at the edge for lossy mobile links.
5. **Terminate at the edge.** CDN / global accelerator (AWS Global Accelerator, Azure Front Door,
   Google Cloud global LB) terminates TCP/TLS near the user and rides the provider backbone.
6. **Reduce round trips.** Batch and aggregate calls (gateway aggregation, GraphQL/BFF), avoid
   N+1 queries, compress payloads (gzip/brotli/zstd), paginate.
7. **Tune the host**: enhanced networking (ENA, Azure Accelerated Networking, gVNIC), cluster
   placement groups or proximity placement groups for tightly coupled HPC, jumbo frames inside a VPC.

## Gotchas
- Private endpoints and NAT add hops; verify paths after network changes.
- DNS TTLs too low cause resolver latency on every call; cache in the client.
- Zone-affinity routing can overload one AZ; keep spillover enabled.
- 0-RTT data is replayable; never for non-idempotent requests.

## Verify
- [ ] Per-hop latency breakdown exists for top journeys.
- [ ] Connection reuse rate high (new TLS handshakes per request near zero).
- [ ] Cross-AZ and cross-region calls on hot paths justified or removed.
