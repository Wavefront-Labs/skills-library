---
id: computing-software.networking-hardware-and-wireless.arista-eos.bgp
name: bgp
category: computing-software
field: networking-hardware-and-wireless
product: arista-eos
tags: [arista-eos, bgp, router-bgp, ebgp, ibgp]
level: practitioner
status: draft
description: "Configure EOS BGP with router-id, neighbors, peer-groups, networks, maximum-paths and show commands."
sources: ["https://www.arista.com/en/support/product-documentation", "https://www.arista.com/en/um-eos/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# BGP configuration
Goal: establish eBGP sessions with policy.

```
router bgp 65101
   router-id 10.255.0.11
   maximum-paths 4 ecmp 4
   neighbor SPINES peer group
   neighbor SPINES remote-as 65100
   neighbor SPINES send-community extended
   neighbor SPINES maximum-routes 12000
   neighbor 198.51.100.0 peer group SPINES
   neighbor 198.51.100.0 password 7 <encrypted-placeholder>
   network 10.255.0.11/32
   redistribute connected route-map RM-CONN
```

```
show ip bgp summary
show ip bgp neighbors 198.51.100.0
show ip bgp neighbors 198.51.100.0 advertised-routes
show ip bgp neighbors 198.51.100.0 received-routes
```

- EOS uses `no bgp default ipv4-unicast` and activates AFIs explicitly in newer designs (`address-family ipv4 / neighbor X activate`); confirm on your release.
- Add `update-source Loopback0` and `ebgp-multihop` for loopback peering.
- Received routes display needs `neighbor X soft-reconfiguration inbound` (confirm).

Gotcha: eBGP with no route-map in or out accepts and advertises per default policy on EOS; apply explicit policy at least on external peers.

## Verify
- `show ip bgp summary` shows `Estab` with prefixes received.
