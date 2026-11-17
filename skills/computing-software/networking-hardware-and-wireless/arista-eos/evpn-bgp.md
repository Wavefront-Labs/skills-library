---
id: computing-software.networking-hardware-and-wireless.arista-eos.evpn-bgp
name: evpn-bgp
category: computing-software
field: networking-hardware-and-wireless
product: arista-eos
tags: [arista-eos, evpn, evpn-vxlan, l2vpn-evpn, route-type]
level: practitioner
status: draft
description: "Configure EOS BGP EVPN overlay with route-reflector or eBGP multihop, RD/RT per VLAN, and verify route types."
sources: ["https://www.arista.com/en/support/product-documentation", "https://www.arista.com/en/um-eos/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# EVPN control plane
Goal: replace flood-and-learn with BGP-distributed MAC/IP.

```
router bgp 65101
   neighbor EVPN-OVERLAY peer group
   neighbor EVPN-OVERLAY remote-as 65100
   neighbor EVPN-OVERLAY update-source Loopback0
   neighbor EVPN-OVERLAY ebgp-multihop 3
   neighbor EVPN-OVERLAY send-community extended
   address-family evpn
      neighbor EVPN-OVERLAY activate
   vlan 100
      rd 10.255.0.11:10100
      route-target both 10100:10100
      redistribute learned
```

```
show bgp evpn summary
show bgp evpn route-type mac-ip
show bgp evpn route-type imet
show vxlan address-table
```

- Route types: 2 (MAC/IP), 3 (IMET, BUM), 5 (IP prefix).
- Spines act as route servers (`next-hop-unchanged`, confirm the setting for your design).
- Use `redistribute learned` per VLAN for MACs.

Gotcha: forgetting `send-community extended` drops route targets, so remote leaves import nothing.

Operational tip: keep RD unique per VTEP per VLAN (`<loopback>:<vni>`) and route targets shared per VLAN, so route reflectors and leaves retain multiple paths for fast failover.

## Verify
- `show bgp evpn summary` is Established and `show bgp evpn route-type imet` includes remote VTEPs.
