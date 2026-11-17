---
id: computing-software.networking-hardware-and-wireless.arista-eos.acls
name: acls
category: computing-software
field: networking-hardware-and-wireless
product: arista-eos
tags: [arista-eos, access-lists, ip-access-list, acl-counters, ipv6-acl]
level: practitioner
status: draft
description: "Create EOS standard and extended ACLs, apply them to interfaces and read hardware counters."
sources: ["https://www.arista.com/en/support/product-documentation", "https://www.arista.com/en/um-eos/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# IP access lists
Goal: filter traffic in hardware.

```
ip access-list WEB-IN
   10 permit tcp any host 192.0.2.10 eq 443
   20 permit icmp any any
   30 deny ip any any log
interface Vlan100
   ip access-group WEB-IN in
```

```
show ip access-lists WEB-IN
show ip access-lists counters
clear ip access-list counters
```

- Sequence numbers allow insertion; resequence with `resequence`.
- Hardware TCAM is limited and `show hardware tcam profile` shows the current profile (platform specific: confirm).
- Counters need `hardware counter feature acl in ...` on some platforms: confirm.

Gotcha: a trailing `deny ... log` on busy interfaces uses CPU and can be rate limited; only log what you need. Missing `permit` for routing protocols (OSPF, BGP) on a control-plane ACL breaks adjacency.

Operational tip: build ACLs with object-style naming and review TCAM usage before large rule sets. Test with counters, and prefer `permit` rules for known traffic ahead of a final explicit deny.

## Verify
- `show ip access-lists WEB-IN` shows hit counts on the permit and deny entries as you test.
