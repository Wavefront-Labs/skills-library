---
id: computing-software.networking-hardware-and-wireless.check-point.site-to-site-vpn-communities
name: site-to-site-vpn-communities
category: computing-software
field: networking-hardware-and-wireless
product: check-point
tags: [networking-hardware-and-wireless, check-point, site-to-site-vpn, vpn-community, ikev2]
level: practitioner
status: draft
description: "Build a Check Point site-to-site VPN community with IKEv2, encryption domain, DH groups and permanent tunnels."
sources:
  - https://sc1.checkpoint.com/documents/R81.20/WebAdminGuides/EN/CP_R81.20_SitetoSiteVPN_AdminGuide/Default.htm
  - https://www.checkpoint.com/training/certification/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Site-to-site VPN communities and IKEv2

- Gateways join a **VPN Community** (Star or Meshed) under VPN Communities. Each gateway needs the **IPsec VPN** blade on, an **encryption domain** (the networks behind it; "Manually defined" group is best), and the community's IKE/IPsec properties.
```
mgmt_cli -r true add vpn-community-meshed name "Mesh_HQ_BR" gateways.1 "gw1" gateways.2 "gw_br" encryption-method "prefer ikev2 but support ikev1" ike-phase-1.ike-p1-dh-group "group-14" encryption-suite "custom" ike-phase-1.encryption-algorithm "aes-256" ike-phase-1.data-integrity "sha256" ike-phase-2.ike-p2-ipsec-dh-group "group-14" ike-phase-2.encryption-algorithm "aes-gcm-256"
mgmt_cli -r true publish
```
- Rulebase: tunnels pass only if the access rule allows the traffic (Source/Destination in the encryption domains, VPN column "Any" or the community). Use "Accept all encrypted traffic" in the community only for lab.
- **Interoperable devices** (non-Checkpoint peers) are `Interoperable Device` objects with a pre-shared secret (strong, unique) or certificates; both peers must have the same subnets for *Phase 2* ("Support IP compression" no, "Perfect Forward Secrecy" matched). IKEv2 on mismatching peer subnets creates multiple SAs; "Subnet per pair" vs "One tunnel per gateway pair" tunnel sharing must match.
- Permanent tunnels (with tunnel-monitoring) are set in the community's Tunnel Management.
- Gotcha: encryption domains must mirror each other (lifetimes differ safely, the lower wins), or "No proposal chosen"/"Invalid ID" appears.

Verify: `vpn tu` (tunnel utility menu: "List all IKE SAs" and "IPSec SAs"), or `vpn tunnelutil`; SmartView Monitor > Tunnels shows Up.
