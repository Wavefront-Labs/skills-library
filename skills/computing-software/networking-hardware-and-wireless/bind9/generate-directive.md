---
id: computing-software.networking-hardware-and-wireless.bind9.generate-directive
name: generate-directive
category: computing-software
field: networking-hardware-and-wireless
product: bind9
tags: [networking-hardware-and-wireless, bind9, generate, zone-file, range]
level: practitioner
status: docs-checked
description: "Use the BIND 9 $GENERATE directive to create many similar records with range, step and modifier syntax."
sources:
  - https://bind9.readthedocs.io/en/latest/chapter3.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# generate directive
Syntax: `$GENERATE range owner [ttl] [class] type rdata`.

The range is `start-stop` or `start-stop/step`. In the owner and RDATA, `$` is replaced by the iterator. Modifiers have the form `${offset,width,base}`, where base is one of `d`, `o`, `x`, `X`, `n`, `N`. Write a literal dollar sign as `\$`.

```
$GENERATE 1-2 host$ A 192.0.2.$
```

That produces `host1` and `host2` with matching addresses. The manual uses it to generate the records for sub-/24 reverse delegations (RFC 2317).

## Checked

2026-11-04. Read the $GENERATE section of the zone file chapter: syntax, range forms, $ substitution, modifier syntax and bases, and the escaped literal dollar confirmed. Replaced an unconfirmed use-case sentence with the documented RFC 2317 use.

Method: documentation only; no commands were run.
