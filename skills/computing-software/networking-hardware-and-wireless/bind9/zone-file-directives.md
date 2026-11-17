---
id: computing-software.networking-hardware-and-wireless.bind9.zone-file-directives
name: zone-file-directives
category: computing-software
field: networking-hardware-and-wireless
product: bind9
tags: [networking-hardware-and-wireless, bind9, zone-directives, origin, include]
level: practitioner
status: docs-checked
description: "BIND 9 zone file directives: at-sign, $ORIGIN, $INCLUDE, $TTL and their exact behaviour."
sources:
  - https://bind9.readthedocs.io/en/latest/chapter3.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# zone file directives
Zone file directives:

- `@` stands for the current origin.
- `$ORIGIN name` sets the origin for relative names that follow.
- `$INCLUDE file [origin]` reads another file; afterwards both the origin and the current owner name are restored.
- `$TTL value` sets the default TTL, in the range 0 to 2147483647. Units such as `1h30m` are accepted.
- `$GENERATE` creates ranges of records; see generate-directive.

```
$ORIGIN example.com.
$TTL 1h
```

The current `$ORIGIN` is appended to unqualified names. When a zone is first read there is an implicit `$ORIGIN zone_name.`, with the trailing dot.

## Checked

2026-11-04. Confirmed against ARM chapter 3 section 3.4.5 (`@`, `$ORIGIN`, `$INCLUDE`, `$TTL`, `$GENERATE`). Reworded the relative-name sentence to the manual's wording.

Method: documentation only; no commands were run.
