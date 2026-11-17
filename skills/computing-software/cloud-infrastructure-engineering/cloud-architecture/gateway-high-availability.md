---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.gateway-high-availability
name: gateway-high-availability
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, gateway-patterns, gateway-high-availability, api-gateway, multi-region, zone-redundancy, failover]
level: practitioner
status: docs-checked
description: "Make the API gateway tier highly available: zone-redundant and multi-region deployment, control and data plane separation, scaling headroom and failover testing."
sources: ["https://learn.microsoft.com/en-us/azure/reliability/reliability-api-management", "https://docs.aws.amazon.com/apigateway/latest/developerguide/disaster-recovery-resiliency.html", "https://developer.konghq.com/gateway/hybrid-mode/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Gateway high availability

## Steps
1. **Treat the gateway as tier-0**: every API depends on it, so its availability target must exceed the APIs behind it.
2. **Zone redundancy**: Amazon API Gateway is a regional service that runs in multiple Availability Zones and is
   designed to recover from a zone failure automatically. Azure API Management (APIM) supports zones only in Premium
   (classic), Premium v2 and Standard v2. Prefer automatic zone support (a minimum of two units, spread best-effort); with
   manual zone redundancy the unit count must be a multiple of the number of zones selected (two zones need 2, 4, ...
   units). A zonal instance on its own gives no zone-outage resilience.
3. **Multi-region**: APIM multi-region is Premium (classic) only and replicates just the gateway; the management
   plane and developer portal stay in the primary region. APIM routes each request to the lowest-latency regional
   gateway, or you can supply your own Traffic Manager with custom rules. For Amazon API Gateway, deploy an API per
   region and use Route 53 health checks to control DNS failover from the primary to the secondary region.
4. **Decouple control and data planes**: in Kong hybrid mode the data plane caches the last configuration on local disk
   and keeps proxying (and can restart) while the control plane is down. Similarly, APIM secondary regions keep serving
   with the most recent gateway configuration if the primary region goes offline.
5. **Config propagation**: APIM gateway configuration syncs across zones and regions normally within 10 seconds, and
   changes not yet replicated can be lost in an outage. APIOps tooling and IaC are the documented customer-managed
   options for restoring service components.
6. **Capacity**: APIM gives no guarantee that capacity requests succeed in another zone or region during an outage, so
   over-provision units for the loss of a zone or region. In a multi-region APIM, autoscale applies only to the primary
   region; secondary regions need manual scaling. Amazon API Gateway throttles with an account-level steady-state rate
   and burst limit that you can customise.
7. **Failure drills**: simulate a region failure by disabling routing to a regional gateway; for a zonal APIM
   instance you cannot simulate a zone outage, only redirect traffic through upstream gateways or load balancers.

## Gotchas
- APIM rate-limit counters and the internal cache are region-specific and not replicated between regions, and the
  internal cache is volatile; use an external cache if data must persist.
- A multi-region gateway still needs backends reachable per region (APIM documents routing API calls to regional
  backend services).
- Kong hybrid mode: the rate-limiting plugins do not support the `cluster` policy (use `local` or `redis`), the
  OAuth 2.0 Authentication plugin is not compatible, and deleting the data plane's cache (`dbless.lmdb`) while the
  control plane is down leaves it starting empty.
- Active requests in a failed zone or region may be dropped; clients must retry.

## Verify
- [ ] Region failover drill: traffic moves within the RTO with no manual DNS edits.
- [ ] Zone loss test keeps the gateway serving.

## Checked
2026-11-08. Confirmed against the Azure API Management reliability page (tiers, zones, units, multiregion, capacity,
replication, backup, drills), the Amazon API Gateway resilience page (multi-AZ, throttling, Route 53 health checks)
and the Kong hybrid mode page (cache on disk, restart while disconnected, plugin limitations); all read in full.
Removed: Apigee guidance (the cited regions page is a 404), Kong replica/topology-spread/PodDisruptionBudget advice, APIM
self-hosted gateway caching, Front Door and Google global load balancer routing, per-region custom domains and
certificate renewal, and the 10,000 RPS account throttle figure (no number on the page).
Method: documentation only; no commands were run.
