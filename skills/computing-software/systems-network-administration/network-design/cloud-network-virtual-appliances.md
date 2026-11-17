---
id: computing-software.systems-network-administration.network-design.cloud-network-virtual-appliances
name: cloud-network-virtual-appliances
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, cloud-networking, nva, network-virtual-appliance, gateway-load-balancer, cloud-firewall]
level: practitioner
status: docs-checked
description: "Deploy firewalls and routers as network virtual appliances in cloud VPCs/VNets: routing through them, HA patterns, symmetric flows, GWLB/Gateway LB and throughput limits."
sources:
  - https://learn.microsoft.com/en-us/azure/architecture/networking/guide/network-virtual-appliance-high-availability
  - https://docs.aws.amazon.com/elasticloadbalancing/latest/gateway/introduction.html
  - https://cloud.google.com/architecture/architecture-centralized-network-appliances-on-google-cloud
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Network virtual appliances in the cloud

## Why and when
Third-party NGFW features (IPS, URL filtering, same policy as on-prem) or SD-WAN hubs in the
cloud. Native cloud firewall services are alternatives; consider them first
for simpler HA and scaling.

## Routing traffic through the NVA
- Cloud route tables (user-defined routes in Azure, VPC route tables in AWS and GCP) send subnet traffic to the NVA.
- Check each cloud's requirement for letting a VM forward traffic not addressed to it.
- HA must use cloud constructs (load balancers, route updates, Azure Route Server with BGP).

## HA patterns
| Pattern | How | Watch out |
|---|---|---|
| Load balancer sandwich | Azure load balancer in front of active-active NVAs | stateful NVAs need symmetric flows: Microsoft describes SNAT or other symmetric designs |
| Gateway Load Balancer | AWS Gateway Load Balancer (GENEVE on port 6081, endpoints across VPCs); Azure Gateway Load Balancer inserts NVAs without UDRs and keeps traffic symmetric without SNAT | appliance must support the GENEVE exchange |
| Route table update on failover | script/Function rewrites routes to standby | slower failover, API dependency |

## Sizing
VM size caps throughput and NICs (bandwidth per VM type); licensed throughput. Test with realistic flow counts, not one iperf stream.

## Verify
- [ ] Kill the active NVA: traffic restored within target; flow logs show return traffic through the same NVA instance.

## Checked

- Date: 2026-10-28
- Confirmed: Azure NVA high-availability article: UDRs, Azure Route Server (BGP), load-balancer designs needing SNAT for symmetry, Gateway Load Balancer without UDRs or SNAT; AWS GWLB guide: GENEVE on port 6081.
- Removed: AWS source/destination check and Azure IP forwarding statements, native service names, GCP next-hop wording, failover timing, accelerated networking (Google page returned almost no text).
Method: documentation only; no commands were run.
