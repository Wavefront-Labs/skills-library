---
id: computing-software.cybersecurity-defensive.security-architecture.hybrid-cloud-security
name: hybrid-cloud-security
category: computing-software
field: cybersecurity-defensive
product: security-architecture
tags: [hybrid-cloud-security, expressroute, direct-connect, site-to-site-vpn, hybrid-connectivity, private-connectivity, macsec, route-filtering]
level: advanced
status: draft
description: "Secure hybrid cloud connectivity: private circuits vs VPN, encryption over Direct Connect/ExpressRoute, route filtering, firewall placement, hybrid DNS and identity trust."
sources: ["https://learn.microsoft.com/en-us/azure/expressroute/expressroute-about-encryption", "https://docs.aws.amazon.com/directconnect/latest/UserGuide/MACsec.html", "https://cloud.google.com/network-connectivity/docs/interconnect/concepts/overview"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Hybrid cloud connectivity security

## Choose the transport
| Option | Encrypted? | Notes |
|---|---|---|
| IPsec site-to-site VPN | Yes | Quick, internet-routed, ~1.25 Gbps per tunnel on AWS |
| Direct Connect / ExpressRoute / Interconnect | **No by default** | Private but not encrypted; add MACsec (supported ports) or IPsec over the circuit |
| Both | - | VPN as backup path; make sure failover keeps the same firewall inspection |

## Controls
1. **Encryption:** MACsec on dedicated 10/100 Gbps DX/ExpressRoute Direct ports, or IPsec over the private VIF/private peering (AWS private IP VPN over DX transit VIF; Azure VPN over ExpressRoute private peering).
2. **Route filtering:** advertise only the on-prem prefixes the cloud needs; accept only cloud VPC/VNet prefixes. Never advertise a default route into the cloud unless you intend to backhaul all egress. Set max-prefix limits on BGP sessions.
3. **Inspection:** terminate the circuit into the hub (see hub-and-spoke) so on-prem<->cloud traffic passes the hub firewall in both directions.
4. **DNS:** conditional forwarders both ways (Route 53 Resolver endpoints, Azure DNS Private Resolver) - do not open on-prem DNS to the internet for cloud.
5. **Identity:** extending AD into the cloud places DCs (tier 0) there; protect them as tier 0, or prefer cloud IdP + federation.
6. **Blast radius:** an on-prem compromise can reach the cloud over the circuit; segment so only required ports cross.

## Gotchas
- Teams assume "private circuit = encrypted"; it is not.
- BGP route leaks from on-prem (e.g. a /8 summary) can attract cloud traffic into the wrong path.
- Failover to VPN often lands on a different firewall/route table with weaker rules; test it.

## Verify
- [ ] MACsec/IPsec status shows encrypted sessions on each circuit.
- [ ] BGP received/advertised prefix lists match the documented allow list.
- [ ] Failover drill: traffic still inspected and logged.
