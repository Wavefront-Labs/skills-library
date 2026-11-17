---
id: computing-software.networking-hardware-and-wireless.kea.dhcp6-subnets-pools-and-unicast
name: dhcp6-subnets-pools-and-unicast
category: computing-software
field: networking-hardware-and-wireless
product: kea
tags: [networking-hardware-and-wireless, kea, kea-dhcp6, subnet6, pools, unicast, overlapping-pools]
level: practitioner
status: docs-checked
description: "Define IPv6 subnets and address pools in kea-dhcp6, listen on a unicast address, and know which pool overlaps are allowed."
sources:
  - https://kea.readthedocs.io/en/latest/arm/dhcp6-srv.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DHCPv6 subnets, pools and unicast listening
Address assignment needs at least one `subnet6` with `pools`, a list even for one entry:

```json
"subnet6": [ { "id": 1, "subnet": "2001:db8:1::/64",
  "pools": [ { "pool": "2001:db8:1::1-2001:db8:1::ffff" } ] } ]
```

By default the server listens on multicast ff02::1:2 on each configured interface. To also accept traffic to a global unicast address (commonly so relays can send directly), append it to the interface, for example `"eth1/2001:db8::1"`, and normally add the `unicast` option with that address. The docs note the unicast option was deprecated by RFC 9915.

Overlap rules:
- Overlapping subnets: allowed; think about how clients are matched.
- Overlapping address pools or prefix delegation pools in one subnet: not allowed (startup error DHCP6_PARSER_FAIL).
- Address pools outside their subnet: not allowed (same error).
- Same pool in different subnets: allowed, acting like a global pool; a client keeps its address when moving between those subnets and no other client receives it.
- Prefix delegation pools not matching the subnet prefix: allowed.

## Checked

2026-11-08. Read dhcp6-srv.rst (Kea ARM source, master branch) sections Unicast Traffic Support, Subnet and Prefix Delegation Pools and Overlapping Pools (partial read, those sections in full). Confirmed multicast ff02::1:2 default, interface/address form, unicast option deprecation, and every overlap rule. Nothing removed.

Method: documentation only; no commands were run.
