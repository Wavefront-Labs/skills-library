---
id: computing-software.networking-hardware-and-wireless.bind9.mx-records
name: mx-records
category: computing-software
field: networking-hardware-and-wireless
product: bind9
tags: [networking-hardware-and-wireless, bind9, mx, mail-exchanger, priority]
level: practitioner
status: docs-checked
description: "MX record rules in a BIND 9 zone file: preference order, target must be an address record, never a CNAME."
sources:
  - https://bind9.readthedocs.io/en/latest/chapter3.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# mx records
An MX record gives a mail host and a preference value.

```
@    IN MX 10 mail.example.com.
@    IN MX 20 backup.example.com.
```

The `check-mx-cname` option (`fail`, `warn` or `ignore`; the default is to warn) controls how named treats MX records that refer to a CNAME, so point MX at a host with address records instead.

## Checked

2026-11-04. Confirmed against the ARM `check-mx-cname` entry. Removed the preference-ordering and trailing-dot statements, which the cited pages do not state.

Method: documentation only; no commands were run.
