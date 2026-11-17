---
id: computing-software.networking-hardware-and-wireless.bind9.stub-and-static-stub-zones
name: stub-and-static-stub-zones
category: computing-software
field: networking-hardware-and-wireless
product: bind9
tags: [networking-hardware-and-wireless, bind9, stub, static-stub, server-addresses]
level: advanced
status: docs-checked
description: "Use BIND 9 stub zones (NS-only transfer) and static-stub zones (fixed server-addresses or server-names) to steer resolution."
sources:
  - https://bind9.readthedocs.io/en/latest/reference.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# stub and static stub zones
A `stub` zone holds a duplicate of a zone's NS records, which named queries the configured primaries for. It overrides NS records in the parent zone until an authoritative server is reached.

A `static-stub` zone holds statically configured NS data: it lists servers directly, and unlike `stub` it also overrides NS records offered by those servers.

```
zone "internal.example" {
    type static-stub;
    server-addresses { /* addresses */ };
};
```

`server-names` supplies server names; `server-addresses` and `server-names` must point to authoritative servers. The manual does not recommend either zone type: use proper NS delegation in the parent zone.

## Checked

2026-11-04. Confirmed against the ARM `type stub` and `type static-stub` entries. Removed the unconfirmed glue claim and added the manual's recommendation.

Method: documentation only; no commands were run.
