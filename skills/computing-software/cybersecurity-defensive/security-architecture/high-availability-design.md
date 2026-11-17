---
id: computing-software.cybersecurity-defensive.security-architecture.high-availability-design
name: high-availability-design
category: computing-software
field: cybersecurity-defensive
product: security-architecture
tags: [resilience, high-availability-design, load-balancing, clustering, redundancy, availability-zones, single-point-of-failure, active-active, active-passive, health-checks]
level: practitioner
status: draft
description: "Design highly available services: remove single points of failure, use load balancing and clustering across zones, health checks, and avoid HA that fails together."
sources: ["CompTIA Security+ SY0-701 objective 3.4 (high availability, load balancing vs clustering)", "AWS Well-Architected Framework - Reliability Pillar", "Google SRE Book (chapters on load balancing and handling overload)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# High availability design

**Goal:** a service keeps working through the failure of any single component, and degrades
gracefully under overload, so availability incidents do not become security incidents.

## Building blocks
- **Load balancing** (active-active): traffic spread across identical stateless instances; failed
  instances removed by health checks.
- **Clustering** (active-passive or active-active with shared state): databases, file systems; a
  quorum/witness prevents split brain.
- **Zones and regions**: instances in at least two availability zones; data replicated across zones.
- **Redundant network and power**: dual uplinks, power supplies, UPS and generator for on-prem.

## Design checklist
1. Draw the request path and mark each component; ask "what if this one fails?" for each.
2. Make app tiers stateless (sessions in a shared store) so any instance can serve.
3. Health checks test real dependencies lightly (a `/healthz` that checks DB connectivity) but
   avoid cascading removal when a shared dependency blips (all instances failing health checks at once).
4. Size N+1 (or N+2 for maintenance plus failure): losing one zone must leave enough capacity.
5. Timeouts, retries with backoff and jitter, circuit breakers between services.
6. Rate limiting and load shedding protect against overload and DoS.
7. Automate failover; manual failover at 3 a.m. is slow and error-prone. Test it.

## Security-relevant points
- HA pairs of firewalls/VPNs: keep configs synchronised; patch one node at a time.
- Certificates, secrets and keys must be available to all nodes and DR.
- Failure mode: decide fail-open vs fail-closed for each security component (see secure design review).

## Gotchas
- Correlated failure: all instances on the same bad config push or certificate expiry fail together; stagger changes.
- Hidden single points: one DNS provider, one NAT gateway, one licence server, one admin.
- Split brain in two-node clusters without a witness corrupts data.

## Verify
- [ ] Chaos/failover tests (terminate an instance, fail a zone) show no customer impact.
- [ ] SLO dashboards show availability against target.
