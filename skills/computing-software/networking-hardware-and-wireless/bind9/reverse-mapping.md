---
id: computing-software.networking-hardware-and-wireless.bind9.reverse-mapping
name: reverse-mapping
category: computing-software
field: networking-hardware-and-wireless
product: bind9
tags: [networking-hardware-and-wireless, bind9, reverse-dns, ptr, in-addr-arpa]
level: practitioner
status: docs-checked
description: "Reverse DNS zones in BIND 9: in-addr.arpa zone declarations, PTR records and $GENERATE for reverse delegations."
sources:
  - https://bind9.readthedocs.io/en/latest/chapter3.html
  - https://bind9.readthedocs.io/en/latest/chapter6.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# reverse mapping
IPv4 reverse zones live under `in-addr.arpa`, with the address octets reversed.

PTR records map the reversed name back to a host name:

```
1.2.0.192.in-addr.arpa. IN PTR host.example.com.
```

Declare the reverse zone like any other:

```
zone "2.0.192.in-addr.arpa" {
    type primary;
    file "2.0.192.in-addr.arpa.db";
};
```

`$GENERATE` creates a series of resource records that differ only by an iterator, and can produce the records for sub-/24 reverse delegations (RFC 2317).

## Checked

2026-11-04. Read the sample configurations and the $GENERATE section of the zone file chapter: in-addr.arpa reverse zones and $GENERATE for RFC 2317 delegations confirmed. Removed the ip6.arpa description and an AAAA remark, which the page does not state.

Method: documentation only; no commands were run.
