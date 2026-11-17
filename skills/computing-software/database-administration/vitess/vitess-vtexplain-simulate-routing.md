---
id: computing-software.database-administration.vitess.vitess-vtexplain-simulate-routing
name: vitess-vtexplain-simulate-routing
category: computing-software
field: database-administration
product: vitess
tags: [vtexplain, explain, vschema, routing, scatter-query, lookup-vindex, vexplain]
level: practitioner
status: docs-checked
description: "Use vtexplain to see which shards Vitess queries for a statement before a cluster exists: inputs, flags, and how to read the sequence output for selects and lookup-vindex inserts."
sources:
  - https://vitess.io/docs/25.0/user-guides/sql/vtexplain/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`vtexplain` works like MySQL `EXPLAIN` but needs no running cluster, so you can try schemas and VSchemas quickly. On a live cluster the docs point to `VEXPLAIN QUERIES|ALL|PLAN` from a SQL console. A prebuilt binary ships with Vitess releases.

Inputs: a SQL schema file with the tables, and a VSchema file. The VSchema must nest each keyspace under its name, otherwise vtexplain fails with `initVtgateExecutor: json: cannot unmarshal bool into Go value of type map[string]json.RawMessage`.

```
vtexplain --shards 8 --vschema-file vschema.json --schema-file schema.sql --replication-mode "ROW" --output-mode text --sql "SELECT * from users"
```

Output lines read `[Sequence number] [keyspace]/[shard]: [query]`. For the select above across 8 evenly split shards, every shard gets `select * from users limit 10001` with sequence number 1, meaning they run in parallel; Vitess adds `LIMIT 10001` to protect against huge results.

For `INSERT INTO users (user_id, name) VALUES(1, 'john')` with a secondary lookup vindex on name, with 128 shards, the output shows: sequence 1 begins a transaction on one shard and inserts into `users_name_idx`; sequence 2 begins another transaction on a different shard and inserts into `users`; sequences 3 and 4 commit them. This shows the cross-shard cost of a lookup vindex.

For unevenly sharded keyspaces, replace `--shards` with `--ks-shard-map` set to a JSON mapping of keyspace to shard ranges, structured like the output of `vtctl FindAllShardsInKeyspace <keyspace>`.

## Checked

2026-11-04. Inputs, error text, command line, output format and both worked examples and the uneven-keyspace `--ks-shard-map` option confirmed on the VTExplain page.

Method: documentation only; no commands were run.
