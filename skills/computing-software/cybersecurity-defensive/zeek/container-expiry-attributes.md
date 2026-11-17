---
id: computing-software.cybersecurity-defensive.zeek.container-expiry-attributes
name: container-expiry-attributes
category: computing-software
field: cybersecurity-defensive
product: zeek
tags: [cybersecurity-defensive, zeek, table-expiry, create-expire, expire-func, ordered-containers]
level: advanced
status: docs-checked
description: "Expire Zeek table and set entries with &read_expire, &write_expire, &create_expire, &expire_func, table_expire_interval, and &ordered."
sources: ["https://docs.zeek.org/en/current/reference/zeekscript/attributes.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# container expiry attributes

Timeouts for table and set elements:

- `&read_expire`: expires after the given time since the last read (a write also counts as a read).
- `&write_expire`: since the last write.
- `&create_expire`: since insertion, regardless of reads or writes.
- `&expire_func`: called just before an element expires. First argument is the container, then one argument per index. For `table[string,string] of count`:

```
function(t: table[string, string] of count, s: string, s2: string): interval
```

The returned interval is extra time to wait before expiring that element, which triggers another call.

Zeek keeps a timer per container that weeds out stale entries. Effort is governed by three tunables: `table_expire_interval` (how often members are checked; an upper bound on reaction time), `table_incremental_step` (members checked per batch), and `table_expire_delay` (wait before the next batch).

Remember attributes bind to values: reassigning the variable with a plain `table()` drops the expiry. Write `my_table = table() &create_expire=1sec;`.

`&ordered` on a table or set makes iteration follow insertion order. Without it, order is undefined:

```
global sset: set[string] &ordered;
```

## Checked

2026-11-08. Read the Attributes page in full; every claim confirmed.

Method: documentation only; no commands were run.
