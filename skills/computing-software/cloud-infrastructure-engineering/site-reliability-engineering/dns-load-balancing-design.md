---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.dns-load-balancing-design
name: dns-load-balancing-design
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [dns-load-balancing-design, geo-dns-setup, load-balancing, route53, edns-client-subnet, ttl]
level: advanced
status: docs-checked
description: "Design DNS-level load balancing: geo/latency routing, health-checked failover, TTL trade-offs, recursive resolver effects and EDNS client subnet, with Route 53 policy names."
sources: ["https://sre.google/sre-book/load-balancing-frontend/", "https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/routing-policy.html", "https://datatracker.ietf.org/doc/html/rfc7871"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DNS load balancing design

SRE Book "Load Balancing at the Frontend": DNS is the first layer of balancing, before the client's
connection even starts. Returning several A or AAAA records and letting the client pick gives very little
control: records are selected randomly and each attracts roughly equal traffic. The book says DNS alone is
not sufficient and should be followed by a virtual-IP layer.

## Problems to design around
- **Recursive resolvers**: the authoritative server sees the resolver's IP, not the user's, so it can only
  optimise for the distance between resolver and nameserver. Mitigation: the EDNS0 client-subnet extension
  (RFC 7871), where the resolver includes the client's subnet in the query; the book notes that large
  resolvers support it. Otherwise estimate the size and geography of the user base behind each resolver.
- **Caching**: authoritative servers cannot flush resolver caches, so records need a relatively low TTL,
  which sets a lower bound on how fast DNS changes reach users.
- **Uneven load**: one reply may reach a single user or thousands, and one nameserver may serve a whole
  ISP from one datacenter; changing its answer moves a big chunk of traffic.
- **Answer size**: replies must fit the 512-byte limit of RFC 1035, which caps the number of addresses
  per reply, probably below your server count.
- **Choosing the best location** means more than distance: the balancer must know the datacenter has
  capacity and is healthy, so integrate the authoritative DNS server with capacity and health data.

## Routing policies (Route 53 terms; other DNS providers have equivalents)
| Policy | Documented use |
|---|---|
| Latency | resources in several AWS Regions; route to the Region with best latency |
| Geolocation | route by the location of users |
| Geoproximity | route by the location of resources, optionally shifting traffic between locations |
| Weighted | route to multiple resources in proportions you specify (gradual shift, canary a new region) |
| Failover | active-passive failover |
| Multivalue answer | up to eight healthy records selected at random |
| IP-based | route by the originating IP addresses of the traffic |

Health checking attaches to records so unhealthy targets are dropped from answers; see the Route 53
developer guide for the record and health-check fields.

## Gotchas
- DNS health checks see the endpoint from the provider's checkers, not from users; pair with real SLIs.
- Failing everything over to one region can overload it; check that the surviving regions have capacity
  (the book's DNS balancer must verify the chosen datacenter has enough).
- Virtual IPs (see `virtual-ips-and-maglev-hashing`) complement DNS: DNS picks the datacenter, the VIP layer picks the machine.

## Verify
- [ ] Queries from different locations (or with a client-subnet option, if your resolver tooling supports it) return the expected region.
- [ ] Failover drill: unhealthy region removed from answers within health-check + TTL time.

## Checked
2026-11-01. Confirmed against the SRE Book "Load Balancing at the Frontend" (DNS problems, resolvers,
EDNS0 client subnet, TTL lower bound, 512-byte limit, capacity-aware choice) and the Route 53 "Choosing a
routing policy" page (policy list, multivalue up to eight healthy records). Removed: the Terraform example,
specific TTL ranges, "resolvers ignore low TTLs", and the dig command (no fetched page states them).
Method: documentation only; no commands were run.
