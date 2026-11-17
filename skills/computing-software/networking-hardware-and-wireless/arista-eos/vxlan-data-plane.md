---
id: computing-software.networking-hardware-and-wireless.arista-eos.vxlan-data-plane
name: vxlan-data-plane
category: computing-software
field: networking-hardware-and-wireless
product: arista-eos
tags: [arista-eos, vxlan, vtep, vni, vxlan-interface]
level: practitioner
status: draft
description: "Configure an EOS VXLAN interface (Vxlan1) with source interface, VLAN-to-VNI map and flood list."
sources: ["https://www.arista.com/en/support/product-documentation", "https://www.arista.com/en/um-eos/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# VXLAN data plane
Goal: bridge VLANs over an IP fabric.

```
interface Vxlan1
   vxlan source-interface Loopback1
   vxlan udp-port 4789
   vxlan vlan 100 vni 10100
   vxlan vrf TENANT-A vni 50001
   vxlan flood vtep 10.255.1.12 10.255.1.13
interface Loopback1
   ip address 10.255.1.11/32
```

```
show interfaces Vxlan1
show vxlan vtep
show vxlan address-table
show vxlan config-sanity
```

- Static (head-end) flooding uses `vxlan flood vtep`; EVPN replaces it with BGP.
- Loopback1 should be advertised in the underlay.
- MTU needs 50 bytes of headroom (jumbo underlay such as 9214).

Gotcha: a VTEP source that is not reachable in the underlay shows the Vxlan1 interface up but no remote VTEPs. Run `show vxlan config-sanity` for missing pieces.

Operational tip: validate underlay MTU end to end with a do-not-fragment ping of 9000 bytes between VTEP loopbacks, because VXLAN hides MTU issues until large frames are used.

## Verify
- `show vxlan vtep` lists remote VTEPs and `show vxlan address-table` learns remote MACs.
