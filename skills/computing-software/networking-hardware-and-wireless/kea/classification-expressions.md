---
id: computing-software.networking-hardware-and-wireless.kea.classification-expressions
name: classification-expressions
category: computing-software
field: networking-hardware-and-wireless
product: kea
tags: [networking-hardware-and-wireless, kea, client-classes, expressions, substring, match, ifelse, relay4]
level: advanced
status: docs-checked
description: "Write Kea classification test expressions: values, equal and match, substring, ifelse, logical operators, and debug logging."
sources:
  - https://kea.readthedocs.io/en/latest/arm/classify.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# classification expressions
A class `test` is a quoted string that must evaluate to a boolean.

Values include: string literal `'example'`, hex literal `0x5a7d`, IP literal, `option[123].hex`, `option[123].exists`, sub-option `option[12].option[34].hex`, `member('foobar')`, `known` / `unknown`, `relay4[123].hex`, `relay6[nest].peeraddr`, `relay6[nest].linkaddr`, `pkt.iface`, `pkt.src`, `pkt.dst`, `pkt.len`, `pkt4.mac`, `pkt4.hlen`.

Operators:
- Predicates: equal (`==`) and `match`. Inequality is `not (a == b)`; case-insensitive match is `match('foo.*', lcase('FooBar'))`. Invalid regexes are syntax errors; runtime exceptions count as no match. Beware ReDoS: `match` can be very slow.
- Logic: `not` binds tightest, `or` loosest; `and`/`or` are left associative. `A and B or C` means `(A and B) or C`.
- `substring(value, start, length)`: start 0 is the first byte, -1 the last; negative length counts backward; `all` means to the end; out-of-range start gives an empty string. `substring('foobar', 3, 3) == 'bar'`.
- `ifelse(cond, iftrue, iffalse)`: `ifelse(option[230].exists, option[230].hex, 'none')`.

Both operands may be runtime expressions, e.g. `option[82].option[2].hex == pkt4.mac`, but each token costs performance.

Debugging: set severity DEBUG and debug level at least 55 on the loggers `kea-dhcp4.eval` or `kea-dhcp6.eval`.

## Checked

2026-11-08. Read the Client Classification chapter in full, in particular section 15.3: the value table, predicates, ReDoS warning, logical operator precedence, substring semantics, ifelse, runtime operands and the kea-dhcp4.eval and kea-dhcp6.eval debug level 55. The skill's not (a == b) form is the docs' own not (substring(...) == 'bar') pattern. Description no longer lists concat, which the body does not cover. Nothing removed.

Method: documentation only; no commands were run.
