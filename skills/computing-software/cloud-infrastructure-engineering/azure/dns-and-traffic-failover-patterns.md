---
id: computing-software.cloud-infrastructure-engineering.azure.dns-and-traffic-failover-patterns
name: dns-and-traffic-failover-patterns
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, bcdr-design, dns-failover, traffic-failover, front-door, traffic-manager, health-probes]
level: advanced
status: docs-checked
description: "Choose and configure regional failover with Front Door, Traffic Manager, DNS TTLs and Load Balancer cross-region, including health probes and failback rules."
sources: ["https://learn.microsoft.com/azure/architecture/guide/networking/global-web-applications/overview", "https://learn.microsoft.com/azure/traffic-manager/traffic-manager-routing-methods", "https://learn.microsoft.com/azure/frontdoor/routing-methods", "https://learn.microsoft.com/azure/load-balancer/cross-region-overview"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DNS and traffic failover patterns

**Goal:** move users to a healthy region automatically and predictably.

## Options
| Service | Layer | Failover speed | Notes |
|---|---|---|---|
| Front Door | HTTP(S) | Driven by health probes | Priority, weighted and latency routing across origin groups |
| Traffic Manager | DNS | Probe settings + DNS TTL + client DNS caching | Routing methods include Priority, Weighted, Performance and Geographic |
| Cross-region Load Balancer | Layer 4 | Driven by regional load balancer health | Global tier load balancer in front of regional load balancers |
| Azure DNS manual change | DNS | Human + TTL | Last-resort runbook |

## Front Door priority failover
- Origin group with origins `prio 1` (primary region) and `prio 2` (secondary).
- Health probe: path `/health` that checks dependencies lightly. Front Door sends traffic to healthy origins at the highest priority (1 is highest) and falls to the next priority level when none is available.
- Failback is automatic when the primary is healthy again; if you need manual failback (data reconciliation), disable the primary origin until ready.

## Traffic Manager
```bash
az network traffic-manager profile create -g rg -n tm-app --routing-method Priority --unique-dns-name app-contoso --ttl 30 \
  --protocol HTTPS --port 443 --path /health --interval 10 --timeout 5 --max-failures 3
az network traffic-manager endpoint create -g rg --profile-name tm-app -n weu --type azureEndpoints --target-resource-id <pipId> --priority 1
```
Fast probing (10 s interval) is billed separately (see the Traffic Manager pricing page); the default interval is 30 s.

## Design rules
- Health endpoints must reflect what users need (deep enough to catch a broken DB connection, shallow enough not to cascade).
- Data tier must fail over too (SQL failover group listener, Cosmos multi-region); traffic failover alone sends users to a broken app.
- Avoid flapping: threshold and failback hysteresis.
- Test by disabling the primary origin/endpoint, not by hoping.

## Verify
- [ ] Drill: disable primary; measure time until traffic in secondary (Front Door access logs by origin), then re-enable.

## Checked
2026-10-31. Confirmed on Microsoft Learn (Traffic Manager monitoring and routing methods, Front Door routing methods): `az network traffic-manager` flags (checked against the CLI reference), probing interval 10 s / 30 s, timeout range 5-9 s at 10 s interval, tolerated failures 0-9, Front Door priority behaviour (priority 1 highest). Removed: failover-speed figures, HEAD probe method, sample-size and 30-60 s interval advice, TTL advice, WAF and caching claims, the `AzureDiagnostics` table name.
Method: documentation only; no commands were run.
