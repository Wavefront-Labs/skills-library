---
id: computing-software.networking-hardware-and-wireless.kea.class-guards-on-subnets-and-pools
name: class-guards-on-subnets-and-pools
category: computing-software
field: networking-hardware-and-wireless
product: kea
tags: [networking-hardware-and-wireless, kea, client-classes, class-guard, subnets, pools, host-reservations]
level: practitioner
status: docs-checked
description: "Restrict Kea subnets and pools to client classes with client-classes guards, and assign classes through host reservations."
sources:
  - https://kea.readthedocs.io/en/latest/arm/classify.html
  - https://kea.readthedocs.io/en/latest/arm/dhcp4-srv.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# class guards on subnets and pools
Put `client-classes` on a subnet to require that clients belong to at least one listed class (a class guard); put it on a pool to restrict that pool's addresses or prefixes the same way. In a shared network, a guarded subnet is not preferred over unguarded ones; it is simply unavailable to non-members.

```json
"subnet4": [ { "id": 1, "subnet": "192.0.2.0/24",
  "client-classes": [ "Client_foo" ],
  "pools": [ { "pool": "192.0.2.10 - 192.0.2.20" } ] } ]
```

where `Client_foo` has `"test": "substring(option[61].hex,0,3) == 'foo'"`.

Order of lookups: subnet reservations are searched after subnet selection. Global reservations are searched at the same time by default; `early-global-reservations-lookup` moves that before subnet selection. Pool selection comes after all reservation lookups.

Classes can be assigned statically by reservation (see the reservation sections for DHCPv4 and DHCPv6). A reservation holding only an identifier puts the host in KNOWN, a basic access-control technique.

## Checked

2026-11-08. Read classify.rst (Kea ARM source, master branch) sections Using Static Host Reservations in Classification, Configuring Subnets With Class Information and Configuring Pools With Class Information, plus the dhcp4-srv.rst sections Client Classification in Shared Networks and Host Reservations as Basic Access Control (partial reads, those sections in full). Confirmed class guards, the Client_foo example, lookup order, early-global-reservations-lookup, the shared-network note and the KNOWN class. Added dhcp4-srv.html to sources since two claims come from it. Nothing removed.

Method: documentation only; no commands were run.
