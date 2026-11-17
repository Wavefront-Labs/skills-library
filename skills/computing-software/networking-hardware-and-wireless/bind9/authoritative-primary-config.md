---
id: computing-software.networking-hardware-and-wireless.bind9.authoritative-primary-config
name: authoritative-primary-config
category: computing-software
field: networking-hardware-and-wireless
product: bind9
tags: [networking-hardware-and-wireless, bind9, authoritative, primary, allow-transfer]
level: practitioner
status: docs-checked
description: "Minimal BIND 9 authoritative primary configuration: recursion off, no cache queries, allow-transfer to secondaries, zone file."
sources:
  - https://bind9.readthedocs.io/en/latest/chapter3.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# authoritative primary config
A primary zone reads its data from a file. An authoritative-only server turns off recursion and the cache:

```
options {
    recursion no;
    allow-query-cache { none; };
    allow-transfer { /* secondary addresses */ };
};
zone "example.com" {
    type primary;
    file "example.com.db";
};
```

Restrict `allow-transfer` to the secondaries so the zone cannot be pulled by anyone. Increase the SOA serial on every change, or secondaries do not transfer.

## Checked

2026-11-04. Confirmed against the ARM Configuration chapter authoritative-only example: `recursion no`, `allow-query-cache { none; }`, `allow-transfer`, primary zone with file, and the secondary comparing SOA serial numbers before transferring. Nothing removed.

Method: documentation only; no commands were run.
