---
id: computing-software.networking-hardware-and-wireless.kea.dhcp6-host-reservations
name: dhcp6-host-reservations
category: computing-software
field: networking-hardware-and-wireless
product: kea
tags: [networking-hardware-and-wireless, kea, kea-dhcp6, host-reservations, duid, ip-addresses, prefixes, excluded-prefixes]
level: practitioner
status: docs-checked
description: "Reserve DHCPv6 addresses and delegated prefixes per host in kea-dhcp6 by DUID or MAC, including multiple IAs and excluded-prefixes."
sources:
  - https://kea.readthedocs.io/en/latest/arm/dhcp6-srv.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DHCPv6 host reservations
Reservations are defined per subnet in an optional `reservations` array. A host is identified by DUID or by hardware/MAC address (see the MAC sources skill). Each element may include one or more addresses, prefixes, a hostname and options. A reserved address must be within the subnet; this does not apply to reserved prefixes.

```json
"reservations": [
  { "duid": "01:02:03:04:05:0A:0B:0C:0D:0E",
    "ip-addresses": [ "2001:db8:1::100" ] },
  { "hw-address": "00:01:02:03:04:05",
    "ip-addresses": [ "2001:db8:1::101", "2001:db8:1::102" ] },
  { "duid": "01:02:03:04:05:06:07:08:09:0A",
    "ip-addresses": [ "2001:db8:1::103" ],
    "prefixes": [ "2001:db8:2:abcd::/64" ], "hostname": "foo.example.com" } ]
```

`ip-addresses` and `prefixes` are arrays because a client may lease several at once. Each reserved item is assigned to one IA of the right type (IA_NA or IA_PD). If the client sends fewer IAs than there are reservations, the extra ones stay reserved for it but are not assigned.

Since Kea 2.7.3, `excluded-prefixes` lists prefixes to exclude from delegated ones; it must have the same number of elements as `prefixes`, and each element is either an empty string or matches the prefix at the same position in `prefixes`.

Since 1.9.1, `reservations-global`, `reservations-in-subnet` and `reservations-out-of-pool` control scope; a subnet reservation beats a global one.

A host reservation should carry only one identifier, either DUID or hardware address; both is a configuration error. A mobile host needs a separate host definition in each subnet it visits, and one hardware address cannot be defined twice within a subnet.

## Checked
Method: docs-only read of cited pages, 2026-11-08

Confirmed against the DHCPv6 chapter sections Host Reservations in DHCPv6 and Address/Prefix Reservation Types (example, IA assignment behaviour, 1.9.1 flags, 2.7.3 excluded-prefixes). Added the single-identifier and per-subnet rules from the same section.
