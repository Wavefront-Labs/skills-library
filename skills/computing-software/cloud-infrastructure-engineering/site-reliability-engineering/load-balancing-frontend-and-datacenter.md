---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.load-balancing-frontend-and-datacenter
name: load-balancing-frontend-and-datacenter
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [site-reliability-engineering, sre, load-balancing, frontend-load-balancing, dns-load-balancing, virtual-ip, consistent-hashing, datacenter-load-balancing, subsetting, deterministic-subsetting, weighted-round-robin, least-loaded, backend-health, lame-duck, flow-control, client-side-load-balancing]
level: advanced
status: docs-checked
description: "Design load balancing as the SRE Book splits it: DNS and virtual-IP at the frontend; lame duck, deterministic subsetting and balancing policies in the datacenter."
sources: ["https://sre.google/sre-book/load-balancing-frontend/", "https://sre.google/sre-book/load-balancing-datacenter/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Load balancing: frontend and datacenter

**Goal:** traffic reaches a healthy backend close to the user, no backend is overloaded while others idle,
and individual backend failures are invisible. All points are from the two SRE Book chapters.

## 1. Frontend: DNS
- "Optimal" depends on the traffic: latency-sensitive search goes to the nearest available datacenter by RTT;
  an upload cares about throughput and may take a different path.
- Returning several A/AAAA records gives little control (records picked roughly equally); SRV weights and
  priorities were not adopted for HTTP.
- Recursive resolvers complicate it: the authoritative server sees the resolver's IP, not the user's. EDNS0
  client-subnet information helps; a resolver may also serve many users in different places.
- A good DNS balancer also considers datacenter capacity and health, via integration with global control
  systems.
- Authoritative servers cannot flush resolver caches, so TTLs must be relatively low, which bounds how fast
  changes propagate (and not every resolver respects TTL).
- DNS replies must fit in 512 bytes (RFC 1035), capping the addresses per reply. DNS is the simplest and most
  effective first layer but is not sufficient alone.

## 2. Frontend: virtual IPs
- A VIP is shared across many devices; a network load balancer forwards packets to backends behind it.
- Always picking the least loaded backend needs per-connection state for stateful protocols. A stateless
  option is a connection ID from packet fields, mod N; removing a backend remaps almost every connection.
- **Consistent hashing** keeps the mapping relatively stable when backends change. The book uses simple
  connection tracking normally and falls back to consistent hashing under pressure (for example a DoS).
- Forwarding choices: NAT (needs a tracking entry per connection); layer-2 MAC rewriting with Direct Server
  Response (saves load-balancer traffic when replies are large, but needs one broadcast domain, which Google
  outgrew); packet encapsulation with GRE (works across networks, adds 24 bytes of overhead for IPv4+GRE, so
  mind MTU and fragmentation).

## 3. Datacenter: health and lame duck
- Simple flow control: stop sending to a backend once a client has a configured number of active requests to
  it (100 is the book's reasonable default). It protects only against extreme overload and can backfire when
  requests are long-lived.
- From a client's view a backend is **healthy**, **refusing connections**, or **lame duck** (listening and
  able to serve, but asking clients to stop sending). Lame duck is broadcast to active clients, and inactive
  clients learn it through periodic health checks, typically within one or two round trips.
- Clean shutdown: on SIGTERM the task enters lame duck, in-flight requests finish, active requests drain to
  zero, then it exits after a configured interval (rule of thumb 10 to 150 seconds, service dependent).

## 4. Subsetting
Connections cost memory and health-check CPU at both ends, so each client talks to a subset. The book
typically uses subsets of 20 to 100 backends (larger if clients are few or bursty).
- **Random subsetting** spreads load badly: with 300 clients, 300 backends and a 30 percent subset the least
  loaded backend got 63 percent of average and the most loaded 121 percent; at 10 percent, 50 and 150 percent.
- **Deterministic subsetting** divides clients into rounds, shuffles the backend list per round with a
  round-specific seed, and gives each client the slice for its position in the round. In the book's 10-of-300
  example every backend gets exactly the same number of connections; in general counts differ by at most one.

## 5. Policies
- **Round robin** is simple but the book saw up to 2x CPU spread between least and most loaded tasks: varying
  client rates and small subsets, query cost differences (the costliest can be 1000x the cheapest), machine
  diversity, and unpredictable factors like antagonistic neighbours and restarts. Keeping restarted tasks in
  lame duck while prewarming is one mitigation.
- **Least-loaded round robin** round-robins among backends with the fewest active requests from that client.
  Pitfall: an unhealthy task answering fast errors sinkholes traffic; count recent errors as active requests.
  Limitations: active count is a poor proxy for capability, and a client only sees its own requests. Large
  services still saw about 2x spread.
- **Weighted round robin**: backends report query rate, error rate and utilisation in each response (including
  health checks); clients adjust capability scores and penalise failures. It reduced the spread drastically.

## Checked
2026-11-01. Confirmed against the SRE Book chapters Load Balancing at the Frontend and Load Balancing in the
Datacenter, both read in full. Removed: Kubernetes, Envoy, Istio, nginx, AWS and GCP settings, anycast and
Maglev claims, P2C, specific TTL values, the 10 percent deterministic-subsetting figure, observability and
verify targets, none of which those chapters state.
Method: documentation only; no commands were run.
