---
id: computing-software.systems-network-administration.network-design.multicloud-networking-interconnect
name: multicloud-networking-interconnect
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, cloud-networking, multicloud-networking, cloud-interconnect, megaport, ip-address-planning]
level: practitioner
status: docs-checked
description: "Connect AWS, Azure, GCP and on-prem: IPsec between clouds, private interconnect via colocation or NaaS fabrics, routing domains, non-overlapping addressing and DNS."
sources:
  - https://learn.microsoft.com/en-us/azure/expressroute/expressroute-introduction
  - https://cloud.google.com/network-connectivity/docs/interconnect/concepts/cross-cloud-interconnect
  - https://docs.aws.amazon.com/directconnect/latest/UserGuide/Welcome.html
  - https://www.megaport.com/services/megaport-cloud-router/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multicloud networking

## Options
| Option | Bandwidth | Notes |
|---|---|---|
| IPsec VPN between cloud gateways | per-tunnel limits apply (see each cloud's VPN limits) | quick, internet path, encryption included, per-tunnel limits: use ECMP across tunnels |
| Private interconnect through your colocation router | port speeds vary | DX + ExpressRoute + Interconnect cross-connects to your router in a colocation site |
| NaaS fabric with virtual router (Megaport Cloud Router) | flexible | no hardware; routes between clouds at layer 3 |
| Cross-Cloud Interconnect (Google Cloud) | check current options | managed physical link to another cloud; check supported providers |
| Overlay platforms (vendor overlay or SD-WAN platforms) | | consistent policy and visibility, extra cost |

## Design rules
- **One global IP plan**: no overlapping CIDRs between clouds and on-prem (or you will need NAT).
- Separate BGP ASNs per cloud edge; control route propagation (summaries, prefix limits: Azure
  ExpressRoute private peering allows 4,000 routes, or 10,000 with the Premium add-on; check the other clouds' limits).
- Egress and interconnect data-transfer costs dominate; route bulk flows deliberately.
- DNS: conditional forwarding between each cloud's resolver and on-prem DNS.
- Redundancy: two connections in different metros/devices per cloud; BFD for fast failover.
- Security: consistent segmentation (per-environment VRFs/route domains), encryption over
  interconnect where required (for example IPsec overlays).

## Verify
- [ ] Route tables in each cloud show only intended prefixes; failover test per link; latency matrix between regions documented.

## Checked

- Date: 2026-10-28
- Confirmed: ExpressRoute intro: BGP route exchange, private peering 4,000 routes raised to 10,000 by the Premium add-on; Direct Connect guide: BGP and optional BFD; Megaport MCR is a managed layer 3 routing platform.
- Removed: per-tunnel VPN throughput, interconnect bandwidth figures, Direct Connect per-VIF prefix limit, Azure-OCI row, DNS product names, MACsec claim and overlay vendor names (Google Cross-Cloud page failed to load).
Method: documentation only; no commands were run.
