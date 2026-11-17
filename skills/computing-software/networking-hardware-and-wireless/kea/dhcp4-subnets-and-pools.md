---
id: computing-software.networking-hardware-and-wireless.kea.dhcp4-subnets-and-pools
name: dhcp4-subnets-and-pools
category: computing-software
field: networking-hardware-and-wireless
product: kea
tags: [networking-hardware-and-wireless, kea, kea-dhcp4, subnet4, pools, subnet-id]
level: intro
status: docs-checked
description: "Define IPv4 subnets, stable subnet IDs and address pools in kea-dhcp4, in range or prefix notation."
sources:
  - https://kea.readthedocs.io/en/latest/arm/dhcp4-srv.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DHCPv4 subnets, IDs and pools
A working server needs at least one subnet and one pool, under `Dhcp4/subnet4`.

```json
"subnet4": [ { "id": 1, "subnet": "192.0.2.0/24",
  "pools": [ { "pool": "192.0.2.10 - 192.0.2.20" },
             { "pool": "192.0.2.64/26" } ] } ]
```

- `pools` is a list even with one entry. A pool is a range (spaces around the hyphen optional) or a prefix; both can be mixed.
- The number of pools is not limited, but use as few as possible for performance.
- Subnet IDs must be unique and stable, greater than zero and less than 4294967295. They link leases to subnets.
- Kea accepts non-canonical prefixes such as `192.0.2.1/24`; only the text is compared to detect duplicates, and abuse can lead to incorrect subnet selection.
- The `exclude-first-last-24` compatibility flag excludes .0 and .255 addresses from subnets with prefix length 24 or shorter.

## Checked
Method: docs-only read of cited pages, 2026-11-08

Confirmed against the DHCPv4 chapter sections IPv4 Subnet Identifier, IPv4 Subnet Prefix and Configuration of IPv4 Address Pools (ID range, non-canonical prefixes, pool formats, pool count advice, exclude-first-last-24). Nothing removed.
