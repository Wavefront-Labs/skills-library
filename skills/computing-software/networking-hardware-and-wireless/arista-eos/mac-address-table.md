---
id: computing-software.networking-hardware-and-wireless.arista-eos.mac-address-table
name: mac-address-table
category: computing-software
field: networking-hardware-and-wireless
product: arista-eos
tags: [arista-eos, mac-address-table, mac-learning, aging, mac-move]
level: practitioner
status: draft
description: "Inspect and tune the EOS MAC table: aging time, static MACs, mac moves and flush."
sources: ["https://www.arista.com/en/support/product-documentation", "https://www.arista.com/en/um-eos/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# MAC address table
Goal: troubleshoot L2 forwarding.

```
mac address-table aging-time 300
mac address-table static 001c.7300.0001 vlan 100 interface Ethernet5
```

```
show mac address-table
show mac address-table address 001c.7300.0001
show mac address-table count
clear mac address-table dynamic vlan 100
show mac address-table notification mac-move
```

- A MAC seen on two ports repeatedly indicates a loop or duplicate.
- In EVPN, local and remote MACs appear with `Vxlan1` and `EvpnDynamicRemoteMac` types.

Gotcha: clearing the table on a busy switch causes flooding while it relearns, so avoid it during peak.

Operational tip: alert on `mac-move` notifications over a threshold and check for duplicate MACs from VM migrations or misconfigured teaming before blaming the fabric. Compare tables across both MLAG peers, since a mismatch indicates synchronisation problems between the peers. Aging defaults of 300 seconds are usually right; shorten only for planned moves and restore them afterwards.

## Verify
- `show mac address-table address <mac>` shows the expected port or VTEP.
