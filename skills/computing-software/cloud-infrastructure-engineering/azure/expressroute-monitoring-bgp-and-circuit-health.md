---
id: computing-software.cloud-infrastructure-engineering.azure.expressroute-monitoring-bgp-and-circuit-health
name: expressroute-monitoring-bgp-and-circuit-health
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, expressroute, expressroute-monitoring, bgp-peers, circuit-health, bgp-availability, arp-availability, expressroute-insights, route-tables, connection-monitor, gateway-metrics, alerts]
level: advanced
status: docs-checked
description: "Monitor ExpressRoute circuits and gateways: BGP/ARP availability, learned routes, bits in/out per link, gateway CPU and route counts, Insights and alerts for a half-down circuit."
sources: ["https://learn.microsoft.com/en-us/azure/expressroute/monitor-expressroute", "https://learn.microsoft.com/en-us/azure/expressroute/expressroute-monitoring-metrics-alerts", "https://learn.microsoft.com/en-us/azure/expressroute/expressroute-network-insights", "https://learn.microsoft.com/en-us/azure/expressroute/expressroute-troubleshooting-expressroute-overview"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ExpressRoute monitoring — BGP sessions, circuit health, gateway load

**Goal:** know within minutes when one of the two links of a circuit drops, when routes go
missing, or when the gateway (not the circuit) is the bottleneck — before users notice failover.

## 1. Health in one pass
```bash
az network express-route show -g rg-conn -n er-lon-1 --query "{state:circuitProvisioningState, provider:serviceProviderProvisioningState, bw:serviceProviderProperties.bandwidthInMbps}"
az network express-route list-route-tables -g rg-conn -n er-lon-1 --peering-name AzurePrivatePeering --path primary   -o table
az network express-route list-route-tables -g rg-conn -n er-lon-1 --peering-name AzurePrivatePeering --path secondary -o table
az network express-route list-route-tables-summary -g rg-conn -n er-lon-1 --peering-name AzurePrivatePeering --path primary -o table   # neighbor, state, prefixes received
az network express-route list-arp-tables -g rg-conn -n er-lon-1 --peering-name AzurePrivatePeering --path primary -o table
az network vnet-gateway list-bgp-peer-status -g rg-hub -n ergw-hub -o table
az network vnet-gateway list-learned-routes  -g rg-hub -n ergw-hub -o table
```
- Both `serviceProviderProvisioningState: Provisioned` and `circuitProvisioningState: Enabled` are required.
- Route-table summary per path: a neighbor `Idle`/`Active` (not `Established`) or
  zero prefixes received on one path = you are running on one link with no redundancy.
- ARP table empty on a path = layer-2 problem (provider/cross-connect), not BGP.

## 2. Metrics that matter
| Resource | Metric | Alert |
|---|---|---|
| Circuit | `BgpAvailability` (per peer, %) | < 100 for 5 min, split by *Peer* |
| Circuit | `ArpAvailability` (per peer, %) | < 100 for 5 min |
| Circuit | `BitsInPerSecond`/`BitsOutPerSecond` (per peering, per link) | > 80 % of circuit bandwidth sustained 15 min |
| Gateway | `ExpressRouteGatewayCpuUtilization` | > 80 % |
| Gateway | `ExpressRouteGatewayBitsPerSecond` (bits received) | near SKU limit |
| Gateway | `ExpressRouteGatewayCountOfRoutesLearnedFromPeer` / `...AdvertisedToPeer` | step changes; approaching the private-peering limit (4,000 prefixes, 10,000 with Premium) |
| Gateway | `ExpressRouteGatewayNumberOfVmInVnet` | sizing check |
| Gateway connection | `ErGatewayConnectionBitsInPerSecond`/`ErGatewayConnectionBitsOutPerSecond` | per-connection usage |
| Direct ports | `AdminState`, `LineProtocol`, `RxLightLevel`/`TxLightLevel` | optics degrading |
```bash
az monitor metrics alert create -g rg-conn -n er-lon-1-bgp --scopes <circuit-id> \
  --condition "avg BgpAvailability < 100 where Peer includes *" --window-size 5m --evaluation-frequency 1m --severity 1 --action <ag-id>
```

## 3. Insights, logs and end-to-end tests
- **ExpressRoute Insights** (Network Insights → ExpressRoute): topology from on-prem
  through circuit to VNets, availability and throughput workbooks per circuit/connection.
- Diagnostic settings on the circuit: `PeeringRouteLog` (BGP route add/withdraw events) →
  Log Analytics; alert on withdrawn default/major prefixes.
- **Connection Monitor** tests on-prem agent ↔ Azure VM over the circuit (TCP/ICMP) for
  latency and loss — the user's view, independent of BGP state.
- Resource Health and Service Health alerts are activity log alerts; wire them to an action group alongside the metric alerts.

## Gotchas
- A circuit at 100 % `BgpAvailability` with the gateway at 100 % CPU still drops packets:
  watch gateway metrics, not only circuit metrics.
- Microsoft peering and private peering report separately; dimension alerts by *Peering type*.
- Bits metrics are per primary/secondary link; asymmetric use (all on primary) is normal
  unless you set AS-path prepend / weights — it also means a primary failure doubles load on secondary.
- Alert on route counts well before the prefix limits.

## Checked
2026-10-28. Confirmed on Microsoft Learn (Monitor ExpressRoute, ExpressRoute metrics and alerts reference, ExpressRoute FAQ): circuit, gateway and Direct-port metric names, `PeeringRouteLog`, BGP/ARP layer reading, private-peering prefix limits. Corrected gateway route-count and connection metric names. Removed: route-limit-drops-session and maintenance-drain claims. Alert thresholds are suggestions, not documented defaults.
Method: documentation only; no commands were run.

## Verify
- [ ] Both paths show `Established` with expected prefix counts; ARP entries present on both.
- [ ] Alert rules exist for BgpAvailability, ArpAvailability, gateway CPU and route count, all wired to the network on-call action group.
- [ ] A scheduled failover test (provider shuts one link) fires the BGP alert and Connection Monitor shows no sustained loss.
