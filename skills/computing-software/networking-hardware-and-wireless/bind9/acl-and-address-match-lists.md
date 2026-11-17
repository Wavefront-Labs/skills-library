---
id: computing-software.networking-hardware-and-wireless.bind9.acl-and-address-match-lists
name: acl-and-address-match-lists
category: computing-software
field: networking-hardware-and-wireless
product: bind9
tags: [networking-hardware-and-wireless, bind9, acl, address-match-list, geoip]
level: practitioner
status: docs-checked
description: "Define named ACLs and address match lists in BIND 9: negation with !, built-in names, first-match order, key elements and GeoIP."
sources:
  - https://bind9.readthedocs.io/en/latest/reference.html
  - https://bind9.readthedocs.io/en/latest/chapter7.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# acl and address match lists
An address match list is a set of elements: IP addresses, prefixes, other ACL names, `key` names, or the built-ins `any`, `none`, `localhost`, `localnets`. Prefix an element with `!` to negate it. Lists can be nested.

Matching is first match wins, so place specific denials before broad allows.

```
acl corpnets { 192.0.2.0/24; 2001:db8::/32; };
options { recursion yes; allow-query { corpnets; }; };
```

A `key` element matches requests signed with that TSIG or SIG(0) key. GeoIP elements (when BIND is built with GeoIP support) look like `geoip country US;`.

## Checked

2026-11-04. Confirmed against the ARM Address Match Lists section and the Access Control chapter: element forms, `!` negation, predefined names, nested lists, first-match order, key elements, GeoIP syntax. Widened the key element to TSIG or SIG(0) and added the GeoIP build note.

Method: documentation only; no commands were run.

