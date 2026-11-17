---
id: computing-software.networking-hardware-and-wireless.arista-eos.mlag
name: mlag
category: computing-software
field: networking-hardware-and-wireless
product: arista-eos
tags: [arista-eos, mlag, peer-link, mlag-domain, mlag-configuration]
level: practitioner
status: draft
description: "Configure an EOS MLAG pair with domain-id, peer-link, peer-address and verify consistency."
sources: ["https://www.arista.com/en/support/product-documentation", "https://www.arista.com/en/um-eos/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# MLAG (multi-chassis LAG)
Goal: build a two-switch logical pair for dual-attached hosts.

```
vlan 4094
   trunk group MLAGPEER
no spanning-tree vlan-id 4094
interface Port-Channel1000
   switchport mode trunk
   switchport trunk group MLAGPEER
interface Vlan4094
   ip address 10.0.199.1/30
mlag configuration
   domain-id MLAG1
   local-interface Vlan4094
   peer-address 10.0.199.2
   peer-link Port-Channel1000
interface Port-Channel20
   mlag 20
```

```
show mlag
show mlag detail
show mlag interfaces
```

- Peer B mirrors with its own address; same domain-id on both.
- Dual-attached hosts use matching `mlag N` IDs on the port-channel on both peers.
- Keep the peer-link VLAN in its own trunk group and out of STP.

Gotcha: `show mlag` state `Inactive` or `config-sanity: inconsistent` usually means differing VLAN/STP settings or peer address mismatch; check `show mlag config-sanity`.

Operational tip: use a dedicated port-channel of at least two links for the peer-link, and monitor `show mlag` state through telemetry. When upgrading, confirm both peers run compatible versions before bringing the pair back.

## Verify
- `show mlag` reports `State: Active`, peer-link `up`, and `config-sanity: consistent`.
