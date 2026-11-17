---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.hybrid-connectivity
name: hybrid-connectivity
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, network-topology, hybrid-connectivity, site-to-site-vpn, direct-connect, expressroute, cloud-interconnect, bgp, redundant-connectivity, macsec]
level: advanced
status: draft
description: "Connect on-premises to cloud: VPN vs dedicated interconnect, redundancy models for SLA, BGP routing and failover, bandwidth/latency sizing, encryption and cost."
sources: ["https://docs.aws.amazon.com/directconnect/latest/UserGuide/resiliency_toolkit.html", "https://learn.microsoft.com/azure/expressroute/designing-for-high-availability-with-expressroute", "https://cloud.google.com/network-connectivity/docs/interconnect/tutorials/production-level-overview"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Hybrid connectivity

## Options
| | Site-to-site VPN | Dedicated / partner interconnect (Direct Connect, ExpressRoute, Cloud Interconnect) |
|---|---|---|
| Setup | hours | weeks (cross-connects, partner) |
| Bandwidth | ~1.25 Gbps per tunnel (AWS); scale with ECMP/multiple tunnels | 50 Mbps-100 Gbps |
| Latency/jitter | internet-dependent | consistent |
| Encryption | IPsec built in | not encrypted by default — MACsec on supported ports or IPsec over it |
| Cost | low fixed | port hours + lower egress rates |

## Redundancy (for production)
- Interconnect: at least two connections at two different locations (AWS "high resiliency";
  "maximum resiliency" = two connections at each of two locations). ExpressRoute: two circuits in
  different peering locations for site resilience; Cloud Interconnect "99.99%" topology needs
  connections in two metros.
- VPN as backup to interconnect is common, with BGP preferences making it secondary.

## Routing
1. BGP everywhere (static routes don't fail over). Use AS-path prepending / local preference /
   MED to steer primary vs backup; BFD for fast failure detection.
2. Summarise advertised prefixes; respect route limits (e.g. Direct Connect private VIF prefix limits;
   ExpressRoute private peering limits per SKU) or sessions drop.
3. Terminate on a transit/hub construct (Transit Gateway via DX gateway, Virtual WAN/hub VNet
   gateway, Cloud Router in a hub VPC) rather than per-VPC.

## Verify
- [ ] Failover test: shut primary BGP session; traffic moves to backup within target time.
- [ ] Bandwidth utilisation alarms at 70% per link.
