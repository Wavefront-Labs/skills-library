---
id: computing-software.cloud-infrastructure-engineering.azure.traffic-manager-nested-profiles-performance-and-geographic-routing
name: traffic-manager-nested-profiles-performance-and-geographic-routing
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, traffic-manager, nested-profiles, tm-performance-routing, tm-geographic-routing, dns-load-balancing, min-child-endpoints]
level: advanced
status: docs-checked
description: "Combine Traffic Manager routing methods with nested profiles: performance and geographic routing, minChildEndpoints, endpoint monitoring tuning and DNS TTL trade-offs."
sources: ["https://learn.microsoft.com/azure/traffic-manager/traffic-manager-nested-profiles", "https://learn.microsoft.com/azure/traffic-manager/traffic-manager-routing-methods", "https://learn.microsoft.com/azure/traffic-manager/traffic-manager-monitoring"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Traffic Manager nested profiles

**Goal:** route users to the nearest healthy region, with canary weighting or zone-of-regions logic inside each region.

## Routing methods recap
Priority (failover), Weighted, **Performance** (lowest latency region from the resolver's location, via
Microsoft's latency tables), **Geographic** (by user geography - compliance/data residency), MultiValue, Subnet.

## Nested example: performance across regions, weighted canary inside
```bash
# child profiles (one per region)
az network traffic-manager profile create -g rg-tm -n tm-weu --routing-method Weighted --unique-dns-name contoso-weu --ttl 30
az network traffic-manager endpoint create -g rg-tm --profile-name tm-weu -n weu-stable --type azureEndpoints \
  --target-resource-id <pip-or-app-id-stable> --weight 95
az network traffic-manager endpoint create -g rg-tm --profile-name tm-weu -n weu-canary --type azureEndpoints \
  --target-resource-id <pip-or-app-id-canary> --weight 5
# parent
az network traffic-manager profile create -g rg-tm -n tm-global --routing-method Performance --unique-dns-name contoso-global --ttl 30
az network traffic-manager endpoint create -g rg-tm --profile-name tm-global -n weu --type nestedEndpoints \
  --target-resource-id $(az network traffic-manager profile show -g rg-tm -n tm-weu --query id -o tsv) \
  --endpoint-location westeurope --min-child-endpoints 1
```
`--min-child-endpoints` (default 1): when fewer healthy endpoints than this remain in the child, the parent treats the
whole child profile as unavailable and sends traffic to its other endpoints.

## Geographic routing
Map regions/countries to endpoints with `--geo-mapping <code>`. A region can map to only one endpoint, and the most
specific match wins. A query from an unmapped region gets a NODATA response, so map the World region to one endpoint
(ideally a nested one). Traffic Manager returns the mapped endpoint whether or not it is healthy, so use nested profiles
(a child profile with at least two endpoints per geography) for resilience.

## Monitoring tuning
Protocol/port/path, probing interval (30 s default, or 10 s fast probing, which is billed separately: see the Traffic
Manager pricing page), tolerated failures (0-9, default 3), timeout. Custom headers (up to eight) for host routing.
Expected status code ranges (up to eight, default 200).
Failover time depends on the probing interval, tolerated failures, DNS TTL and client DNS caching.

## Gotchas
- Routing decisions use the IP address of the recursive DNS service that queries Traffic Manager, not the client's own IP.
- The Performance algorithm is deterministic, but updates to the Internet Latency Table can move some clients to a different endpoint.

## Verify
- [ ] `nslookup contoso-global.trafficmanager.net` from different regions returns the nearest region; disabling a region's endpoints shifts answers within the expected time.

## Checked
2026-10-31. Confirmed on Microsoft Learn (Traffic Manager routing methods, nested profiles, endpoint monitoring pages): MinChildEndpoints behaviour and default, geographic mapping rules and NODATA for unmapped regions, probing interval 30 s / 10 s, tolerated failures 0-9 default 3, custom header and status-range limits, resolver-IP based routing, Internet Latency Table. Removed: the NXDOMAIN claim (docs say NODATA), the `GEO-EU` and `WORLD` code values, the failover-time formula, EDNS client subnet, DNS-only and DNS query cost remarks.
Method: documentation only; no commands were run.
