---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.global-traffic-routing
name: global-traffic-routing
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, caching-strategy, global-traffic-routing, latency-based-routing, geo-routing, anycast]
level: practitioner
status: draft
description: "Route global traffic by latency, geography or weight: DNS-based vs anycast load balancers, health checks, failover, and data residency constraints."
sources: ["https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/routing-policy.html", "https://docs.aws.amazon.com/global-accelerator/latest/dg/what-is-global-accelerator.html", "https://learn.microsoft.com/azure/traffic-manager/traffic-manager-routing-methods", "https://cloud.google.com/load-balancing/docs/https"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Global traffic routing

## Options
- **DNS-based**: Route 53 routing policies (latency, geolocation, geoproximity, weighted,
  failover), Azure Traffic Manager, Cloud DNS routing policies. Simple, works for any
  endpoint, but failover depends on resolver TTL behaviour.
- **Anycast / global load balancers**: AWS Global Accelerator, Azure Front Door, Google
  global external Application Load Balancer, Cloudflare. One IP, edge TCP termination,
  failover in seconds independent of DNS caching.

## Steps
1. **Pick policy**: latency for performance; geolocation for residency and legal
   (users in the EU must hit EU regions); weighted for gradual migration or canary.
2. **Health checks** on a deep endpoint that reflects regional dependencies; avoid
   flapping with sensible thresholds.
3. **Failover behaviour**: decide whether traffic may cross jurisdictions on failure
   (geolocation with a default record vs strict).
4. **TTLs**: 60 s for failover records; understand that some clients ignore TTLs.
5. **Session and data**: routing users to another region requires their data to be there
   (replication) and sessions to be portable.
6. **Test** regional failover regularly.

## Gotchas
- Geolocation by resolver IP misroutes users of public resolvers without EDNS client subnet.
- Health checks that only test a static page fail open when the database is down.

## Verify
- [ ] Failover drill timed from health check failure to traffic shift.
- [ ] Residency rules hold during failover.
