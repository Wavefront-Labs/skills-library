---
id: computing-software.networking-hardware-and-wireless.bind9.mirror-zones
name: mirror-zones
category: computing-software
field: networking-hardware-and-wireless
product: bind9
tags: [networking-hardware-and-wireless, bind9, mirror, root-zone, dnssec-validated]
level: advanced
status: docs-checked
description: "Configure a BIND 9 mirror zone: type mirror, DNSSEC validation of the transferred zone, and request-ixfr no."
sources:
  - https://bind9.readthedocs.io/en/latest/reference.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# mirror zones
A mirror zone is similar to a secondary zone, except its data is DNSSEC-validated before use. If validation of a new version fails, a retransfer is scheduled and the most recent validated version is used until it expires or a newer one validates; with no usable data, normal recursion answers instead. It is intended for a fast local copy of the root zone, and a default primaries list for the IANA root is built in:

```
zone "." {
    type mirror;
};
```

Each IXFR revision is validated separately, so it can be useful to force AXFR with `request-ixfr no`. Answers from a mirror zone have the AD bit set and the AA bit unset. Use `file` to keep contents across restarts. Mirror zones cannot be used in a view without recursion.

## Checked

2026-11-04. Confirmed against the ARM `type mirror` entry. Replaced the claim that named does not use the zone on failure and the IXFR-support reason for `request-ixfr no` with the manual's wording.

Method: documentation only; no commands were run.
