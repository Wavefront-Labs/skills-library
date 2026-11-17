---
id: computing-software.networking-hardware-and-wireless.juniper-junos.lag-lacp
name: lag-lacp
category: computing-software
field: networking-hardware-and-wireless
product: juniper-junos
tags: [juniper-junos, aggregated-ethernet, lag, lacp, ae-interface]
level: practitioner
status: draft
description: "Create Junos ae interfaces with LACP, member links, min-links and hashing."
sources: ["https://www.juniper.net/documentation/", "https://www.juniper.net/documentation/us/en/software/junos/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Aggregated Ethernet and LACP
Goal: bundle links for bandwidth and redundancy.

```
set chassis aggregated-devices ethernet device-count 4
set interfaces ge-0/0/20 gigether-options 802.3ad ae0
set interfaces ge-0/0/21 gigether-options 802.3ad ae0
set interfaces ae0 aggregated-ether-options lacp active
set interfaces ae0 aggregated-ether-options lacp periodic fast
set interfaces ae0 aggregated-ether-options minimum-links 1
set interfaces ae0 unit 0 family ethernet-switching interface-mode trunk vlan members all
```

```
user@host> show lacp interfaces
user@host> show interfaces ae0 terse
```

- Member options are `gigether-options` (ge), `ether-options` (xe/et) depending on the interface type.
- Load balancing is per flow based on a hash; tune with `forwarding-options enhanced-hash-key` or `load-balance per-packet` (platform-specific: confirm).

Gotcha: forgetting `device-count` means ae0 does not exist after commit. A mismatched LACP mode (passive/passive) never forms.

Operational tip: keep member links the same speed, and use `lacp periodic fast` with care on large bundles since control-plane load increases; check that both peers use the same hashing assumptions.

## Verify
- `show lacp interfaces` shows `Collecting distributing` on all members, and `ae0` is up.
