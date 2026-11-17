---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.network-virtual-appliance
name: network-virtual-appliance
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, network-topology, network-virtual-appliance, nva, cloud-firewall, azure-firewall, aws-network-firewall, gateway-load-balancer, firewall-placement]
level: advanced
status: draft
description: "Decide between native cloud firewalls and third-party NVAs, and place them correctly: hub inspection, gateway load balancer insertion, HA, symmetric routing and throughput limits."
sources: ["https://learn.microsoft.com/azure/architecture/networking/guide/network-virtual-appliance-high-availability", "https://docs.aws.amazon.com/elasticloadbalancing/latest/gateway/introduction.html", "https://docs.aws.amazon.com/network-firewall/latest/developerguide/what-is-aws-network-firewall.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Firewall placement (NVA vs native firewall)

## Native vs NVA
| | Native (Azure Firewall, AWS Network Firewall, Cloud NGFW) | Third-party NVA (Palo Alto, Fortinet, Check Point) |
|---|---|---|
| Ops | Managed scaling and HA | You run VMs, upgrades, licences |
| Features | L3-L7 rules, FQDN filtering, IDPS (premium tiers), TLS inspection (some) | Full NGFW feature set, consistent with on-prem policy |
| Cost | Per hour + per GB processed | VM + licence; often cheaper per GB at very high volumes |
| Skills | Cloud IaC | Existing security team tooling |

## Placement patterns
- **Hub inspection**: all spoke-to-spoke, spoke-to-on-prem and egress traffic routed through the
  hub firewall via route tables/UDRs (Azure) or Transit Gateway route tables with an inspection VPC (AWS).
- **AWS Gateway Load Balancer**: transparent insertion of NVA fleets using GENEVE; endpoints in
  each VPC route traffic to the appliance fleet with flow stickiness.
- **Azure**: NVAs behind an internal Standard Load Balancer with HA ports; or Azure Firewall in
  the hub / Virtual WAN secured hub.
- **Ingress**: WAF/application gateway in front of apps; firewall may sit behind it for east-west only.

## HA and routing
- Symmetric routing is essential for stateful inspection: both directions must traverse the same
  instance (LB with session affinity / GWLB flow stickiness; AWS Transit Gateway appliance mode).
- Spread appliances across zones; health probes that test the data path.

## Gotchas
- Per-GB processing charges for all east-west traffic can dominate network cost.
- Forgetting TGW appliance mode causes asymmetric drops across AZs.
- TLS inspection breaks certificate-pinned clients; maintain bypass lists.

## Verify
- [ ] Flow logs show traffic paths through the firewall as designed.
- [ ] Failover of one appliance/zone without dropped established sessions beyond tolerance.
