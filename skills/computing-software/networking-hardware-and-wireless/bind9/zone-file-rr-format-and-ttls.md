---
id: computing-software.networking-hardware-and-wireless.bind9.zone-file-rr-format-and-ttls
name: zone-file-rr-format-and-ttls
category: computing-software
field: networking-hardware-and-wireless
product: bind9
tags: [networking-hardware-and-wireless, bind9, zone-file, resource-records, ttl]
level: practitioner
status: docs-checked
description: "BIND 9 zone file record layout: owner, TTL, class, type, RDATA; TTL sources, units, and the SOA minimum as negative-caching TTL."
sources:
  - https://bind9.readthedocs.io/en/latest/chapter3.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# zone file rr format and ttls
A resource record has the fields owner, TTL, class, type and RDATA. Classes are IN, CH and HS.

TTLs come from per-record values, the `$TTL` directive, or the SOA minimum. The SOA minimum field is the negative-caching TTL, with a maximum of 3 hours. Units are allowed, for example `1h30m`.

```
$TTL 1h
@    IN SOA ns1 hostmaster ( 2026110401 1h 15m 4w 1h )
     IN NS  ns1
```

If an owner name is omitted, the previous record's owner is used. `@` stands for the current origin.

## Checked

2026-11-04. Read the zone file section of the Administrator Reference Manual: record fields, classes, TTL units and the 3 hour negative caching maximum confirmed. Removed an unconfirmed closing instruction.

Method: documentation only; no commands were run.
