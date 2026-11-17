---
id: computing-software.networking-hardware-and-wireless.bind9.secondary-zone-config
name: secondary-zone-config
category: computing-software
field: networking-hardware-and-wireless
product: bind9
tags: [networking-hardware-and-wireless, bind9, secondary, primaries, axfr]
level: practitioner
status: docs-checked
description: "Configure a BIND 9 secondary zone: type secondary, primaries list, local file, and how refresh and serial comparison trigger transfers."
sources:
  - https://bind9.readthedocs.io/en/latest/chapter3.html
  - https://bind9.readthedocs.io/en/latest/reference.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# secondary zone config
A secondary obtains the zone from a primary by AXFR or IXFR over TCP port 53 when the SOA serial on the primary is higher than its own.

```
zone "example.com" {
    type secondary;
    file "example.com.db";
    primaries { /* primary address */ };
};
```

The secondary reads the primary's SOA periodically, at the interval set by the SOA refresh parameter, and also reacts to NOTIFY from the primary. The primary must permit the transfer through `allow-transfer`.

## Checked

2026-11-04. Confirmed against the ARM Configuration chapter zone transfer description: SOA serial comparison, AXFR or IXFR over TCP port 53, SOA refresh polling, NOTIFY. Nothing removed.

Method: documentation only; no commands were run.
