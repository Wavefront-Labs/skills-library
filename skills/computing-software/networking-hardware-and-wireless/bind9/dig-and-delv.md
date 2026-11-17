---
id: computing-software.networking-hardware-and-wireless.bind9.dig-and-delv
name: dig-and-delv
category: computing-software
field: networking-hardware-and-wireless
product: bind9
tags: [networking-hardware-and-wireless, bind9, dig, delv, dns-lookup]
level: practitioner
status: docs-checked
description: "Query DNS with dig and validate with delv: server, name and type syntax, +trace, +short, +tcp, +dnssec, -x, and delv trace options."
sources:
  - https://bind9.readthedocs.io/en/latest/manpages.html
  - https://bind9.readthedocs.io/en/latest/chapter4.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# dig and delv
```
dig @server name type
```

Common `dig` options: `-4`/`-6`, `-x addr` reverse lookup, `-k`/`-y` TSIG, `+trace` follow delegations from the root, `+short` terse, `+tcp`, `+tls`, `+dnssec` request DNSSEC records, `+nssearch` query every zone name server for the SOA, `+subnet` EDNS client subnet, `+nsid`, `+ttlunits`. Default options can go in `.digrc`.

`delv` does validating lookups using named's validator logic. It takes trust anchors with `-a`, and `+vtrace` / `+rtrace` show validation and resolution steps. Use it to check whether a DNSSEC failure is real before touching the server.

`host` is a simpler tool; `nslookup` is not recommended.

## Checked

2026-11-04. Confirmed against the dig and delv man pages and the ARM Diagnostic Tools chapter: the listed dig options, `.digrc`, delv `-a`, `+vtrace`, `+rtrace`, and the nslookup recommendation. Nothing removed.

Method: documentation only; no commands were run.
