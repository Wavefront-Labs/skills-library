---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.dns-cutover
name: dns-cutover
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, migration-execution, dns-cutover, ttl-lowering, weighted-routing, traffic-switch, blue-green-cutover]
level: practitioner
status: draft
description: "Cut traffic over with DNS safely: lower TTLs in advance, weighted or failover records, client caching realities, validation and fast rollback."
sources: ["https://datatracker.ietf.org/doc/html/rfc1034", "https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/routing-policy-weighted.html", "https://learn.microsoft.com/azure/traffic-manager/traffic-manager-routing-methods"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# DNS and traffic cutover technique

## Steps
1. **Inventory** every name pointing at the source (public and private zones, CNAME chains,
   hard-coded IPs in clients/partners, allow-lists at partners).
2. **Lower TTL** to 60-300 s at least one old-TTL period before cutover (if TTL was 86400, lower it
   >24 h ahead). Verify with `dig +noall +answer name` against authoritative and public resolvers.
3. **Choose method**:
   - Simple record swap at a cutover moment.
   - Weighted records (Route 53 weighted, Traffic Manager weighted, Cloud DNS weighted round robin)
     to shift 1% -> 10% -> 50% -> 100% for stateless services.
   - Load balancer / CDN origin switch where possible (instant, no client caching issues).
4. **Cutover**: change record, watch traffic arrive on target, error rates, latency.
5. **Rollback**: revert record; leave source warm until TTL x 2 has passed plus validation window.
6. **Restore TTL** to normal after stabilisation.

## Client caching realities
- Some clients and JVMs cache DNS beyond TTL (Java `networkaddress.cache.ttl`), corporate resolvers
  may clamp TTLs; long-lived connections keep using old IPs until reconnect.
- Drain connections on the source (connection draining / deregistration delay).

## Gotchas
- Lowering TTL only on the A record while a parent CNAME keeps a long TTL.
- Split-horizon: forgetting the private zone.
- Partner IP allow-lists for new egress IPs not updated.

## Verify
- [ ] Source traffic near zero before decommission.
- [ ] Monitoring shows healthy target at 100%.
