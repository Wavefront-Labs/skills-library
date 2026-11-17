---
id: computing-software.software-engineering.erlang.mnesia-schema-tables
name: mnesia-schema-tables
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-mnesia, mnesia-schema-tables]
level: advanced
status: docs-checked
description: "Mnesia setup: create_schema, create_table with attributes, ram_copies/disc_copies/disc_only_copies, indexes, add_table_copy and wait_for_tables."
sources:
  - https://www.erlang.org/doc/apps/mnesia/mnesia.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Schema, tables and storage types
**Goal:** create a persistent Mnesia table.

```erlang
-record(user, {id, name}).
mnesia:create_schema([node()]),
mnesia:start(),
{atomic, ok} = mnesia:create_table(user,
    [{attributes, record_info(fields, user)},
     {disc_copies, [node()]}, {type, set}, {index, [name]}]),
ok = mnesia:wait_for_tables([user], 5000).
```
- `mnesia:create_schema/1` fails if any listed node is not alive, if Mnesia is running on any of them, or if a node already has a schema (use `mnesia:delete_schema/1` to remove an old one). List only nodes with disc. The data directory is chosen with the `-mnesia dir Directory` parameter and must be unique per node; two nodes must never share it.
- Storage: `ram_copies` (not written to disc per transaction; can be dumped with `mnesia:dump_tables/1`), `disc_copies` (writes go to disc and to the RAM copy), `disc_only_copies` (kept on disc only, considerably slower than RAM; `ordered_set` is not supported for them).
- The table type is `set`, `ordered_set` or `bag`. The record name defaults to the table name unless `{record_name, Name}` is given. `{index, Attrs}` builds extra index tables.
- `mnesia:add_table_copy(Tab, Node, Type)` adds a replica on another node.

## Self-check
Create a table, restart the node, and confirm data survives with `disc_copies`.

## Checked

2026-11-03. Confirmed in the `mnesia` reference page: `create_schema/1`, `create_table/2` options, storage types, `record_name`, `index`, `add_table_copy/3`, `wait_for_tables/2` and the `-mnesia dir` parameter. Removed: the `/var/lib/myapp` path, the "size limits apply" wording, the `create_table` failure claim and the network-partition gotcha.
Method: documentation only; no commands were run.
