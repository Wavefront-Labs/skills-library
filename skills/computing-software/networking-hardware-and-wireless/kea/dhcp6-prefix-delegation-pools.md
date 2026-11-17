---
id: computing-software.networking-hardware-and-wireless.kea.dhcp6-prefix-delegation-pools
name: dhcp6-prefix-delegation-pools
category: computing-software
field: networking-hardware-and-wireless
product: kea
tags: [networking-hardware-and-wireless, kea, kea-dhcp6, prefix-delegation, pd-pools, delegated-len, excluded-prefix]
level: practitioner
status: docs-checked
description: "Configure DHCPv6 prefix delegation pools in kea-dhcp6 with prefix, prefix-len and delegated-len, including the Prefix Exclude option."
sources:
  - https://kea.readthedocs.io/en/latest/arm/dhcp6-srv.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DHCPv6 prefix delegation pools
A subnet can have one or more `pd-pools`. Each has `prefix`, `prefix-len` and `delegated-len`. The delegated length must be numerically greater than or equal to the prefix length; if equal, only one prefix can be delegated. The delegated prefix need not match the subnet prefix.

```json
"pd-pools": [ { "prefix": "3000:1::", "prefix-len": 64,
                "delegated-len": 96 } ]
```

Prefix Exclude (RFC 6603): the delegating router may exclude one prefix from each delegated prefix; the requesting router must not assign it to downstream interfaces, and it is meant for the link used for DHCPv6 between the two. Add `excluded-prefix` and `excluded-prefix-len` to the pool:

```json
{ "prefix": "2001:db8:1:8000::", "prefix-len": 56, "delegated-len": 64,
  "excluded-prefix": "2001:db8:1:8000:cafe:80::",
  "excluded-prefix-len": 72 }
```

It is sent only to requesting routers that include the Prefix Exclude option in the Option Request option. Overlapping PD pools in one subnet are a startup error.

## Checked

2026-11-08. Read dhcp6-srv.rst (Kea ARM source, master branch) sections Subnet and Prefix Delegation Pools, Prefix Exclude Option and Overlapping Pools (partial read, those sections in full). Confirmed prefix, prefix-len, delegated-len rules, the RFC 6603 exclude behaviour and the overlap error. Nothing removed.

Method: documentation only; no commands were run.
