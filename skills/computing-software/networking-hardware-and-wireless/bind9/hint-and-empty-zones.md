---
id: computing-software.networking-hardware-and-wireless.bind9.hint-and-empty-zones
name: hint-and-empty-zones
category: computing-software
field: networking-hardware-and-wireless
product: bind9
tags: [networking-hardware-and-wireless, bind9, hint, root-hints, empty-zones-enable]
level: practitioner
status: docs-checked
description: "BIND 9 hint zone for root servers (named.root) and the built-in empty zones controlled by empty-zones-enable."
sources:
  - https://bind9.readthedocs.io/en/latest/chapter3.html
  - https://bind9.readthedocs.io/en/latest/reference.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# hint and empty zones
A `hint` zone for "." tells named where to find root servers at startup:

```
zone "." {
    type hint;
    file "named.root";
};
```

If no hint zone is specified for class IN, named uses a compiled-in default set of root hints, so the hint zone is optional.

`empty-zones-enable` is enabled by default. The built-in empty zones (SOA and NS records only) cover reverse namespaces such as RFC 1918 private ranges, so those queries are answered locally and not sent to the Internet root servers. Individual zones can be excluded with `disable-empty-zone`.

## Checked

2026-11-04. Confirmed against the ARM `type hint`, `empty-zones-enable`, `disable-empty-zone` and Built-in Empty Zones entries. Reworded the empty-zone description to match the manual.

Method: documentation only; no commands were run.
