---
id: computing-software.cybersecurity-defensive.zeek.script-attributes-core
name: script-attributes-core
category: computing-software
field: cybersecurity-defensive
product: zeek
tags: [cybersecurity-defensive, zeek, attributes, redef, default-attribute, optional-fields]
level: practitioner
status: docs-checked
description: "Zeek script attributes: &redef, &priority, &log, &optional, &default (values, expressions, table functions), &default_insert, and the pitfall that attributes bind to values."
sources: ["https://docs.zeek.org/en/current/reference/zeekscript/attributes.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# core script attributes

- `&redef` lets `redef` change a `global` or `const` initial value: `const clever = T &redef;`.
- `&priority=N` orders event handlers and hooks; higher runs first, default 0. `event zeek_init() &priority=10`.
- `&log` on a record field makes it a log column when the record is used in `Log::create_stream`. Put `&log` after a record's closing brace to cover all its fields; fields added later via `redef` need `&log` again.
- `&optional` allows a missing record field. Test with `?$`; remove a value with `delete`.
- `&default` sets a default for a record field, container element or parameter. It accepts expressions, evaluated on each new record: `ts: time &log &default=network_time();`
- On tables, `&default` may be a function or lambda called on a missing index:

```
global mytable: table[count, string] of string &default=function(c: count, s: string): string {
    return fmt("unknown-%s-%s", c, s);
};
print mytable[0, "a"];   # unknown-0-a
```

A default value is not inserted. `&default="foo"` prints `foo` for a missing key but `|mytable|` stays 0. Use `&default_insert` (page marks it added in 6.1) to insert it; it is often better for table or record values.

Parameters with `&default` must come after those without.

Pitfall: attributes bind to a value, not a variable. After `my_table = table();` the original `&create_expire` is lost. Reassign with `table() &create_expire=1sec`.

## Checked

2026-11-04: read against the official Zeek documentation page(s) listed in sources; the claims, names, values and examples in this skill match the page text. Nothing else was added.

Method: documentation only; no commands were run.
