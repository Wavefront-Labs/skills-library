---
id: computing-software.cloud-infrastructure-engineering.azure.nat-gateway-metrics-and-idle-timeout
name: nat-gateway-metrics-and-idle-timeout
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, nat-gateway, nat-gateway-metrics, nat-idle-timeout, snat-connection-count, datapath-availability, tcp-keepalive]
level: practitioner
status: docs-checked
description: "Monitor NAT gateway health and SNAT usage with its metrics, alert on dropped packets and port pressure, and tune TCP idle timeout and keepalives."
sources: ["https://learn.microsoft.com/azure/nat-gateway/nat-metrics", "https://learn.microsoft.com/azure/nat-gateway/troubleshoot-nat-connectivity", "https://learn.microsoft.com/azure/nat-gateway/nat-gateway-resource#tcp-idle-timeout"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NAT gateway metrics and idle timeout

**Goal:** know before users do when NAT gateway is dropping connections or running out of ports,
and stop idle connections being silently cut.

## Key metrics (Azure Monitor, namespace Microsoft.Network/natGateways)
| Metric | Use | Suggested alert (starting point, tune) |
|---|---|---|
| Datapath availability | Health of the NAT data path | < 90% for 15 min |
| SNAT connection count (split by *Connection State*: Attempted, Failed) | Connection churn, failures | Failed > 0 sustained |
| Total SNAT connection count | Active flows | Approaching IPs × 64,512 SNAT ports (each IP also supports up to 50,000 simultaneous connections per unique destination endpoint) |
| Dropped packets | Packets NAT couldn't process | > baseline |
| Bytes / Packets (split by direction) | Throughput (50 Gbps per Standard NAT gateway; StandardV2 is 100 Gbps) | — |
Metric IDs: `DatapathAvailability`, `SNATConnectionCount` (dimensions Protocol, ConnectionState), `TotalConnectionCount`, `PacketDropCount`, `ByteCount`, `PacketCount`. Build alert rules on these in Azure Monitor.

## Port math
SNAT ports are allocated per destination IP:port; the same source port can be reused to
different destinations. Exhaustion mostly happens when many connections go to **one** endpoint
(e.g. a single SaaS API IP). Fixes: add public IPs (scales linearly), connection pooling/HTTP keep-alive,
private endpoints for Azure services (removes them from NAT entirely).

## Idle timeout
- TCP idle timeout configurable **4–120 minutes** (default 4); UDP fixed 4 min.
- After timeout, the flow mapping is removed; the next packet on that connection is dropped (no RST) → apps see hangs.
- Prefer TCP keepalives below 4 min in apps/OS (`net.ipv4.tcp_keepalive_time=180`) over raising the timeout — long timeouts hold ports.
```bash
az network nat gateway update -g rg-net -n ng-weu-z1 --idle-timeout 10
```

## Gotchas
- Connection failures can be remote-side (destination rate limits) — check *Failed* vs destination.

## Verify
- [ ] Alerts exist for datapath availability and failed SNAT connections.
- [ ] Peak total SNAT connections < 50% of IPs × 64,512 for the top destination.

## Checked

- 2026-10-27. Confirmed on Microsoft Learn (NAT gateway metrics, NAT gateway resource, troubleshoot NAT connectivity, NAT overview): metric IDs and dimensions, 64,512 SNAT ports per IP, 16 IP limit, TCP idle timeout 4-120 minutes (default 4), UDP fixed 4 minutes, silent drop after idle timeout, 50 Gbps per Standard NAT gateway.
- Removed: the FIN 65 s / RST 16 s port-hold figures, the `az monitor metrics` commands (syntax not confirmed), and statements about flow logging and per-VM metrics. Alert thresholds are now labelled as suggestions, not documented values.

Method: documentation only; no commands were run.
