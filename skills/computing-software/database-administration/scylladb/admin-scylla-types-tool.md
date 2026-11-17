---
id: computing-software.database-administration.scylladb.admin-scylla-types-tool
name: admin-scylla-types-tool
category: computing-software
field: database-administration
product: scylladb
tags: [scylla-types, deserialize, serialize, compound-keys, hex-values]
level: practitioner
status: docs-checked
description: "The scylla types tool: serialize, deserialize, compare and validate raw hex values from SSTables or logs, -t type names, and decoding compound partition or clustering keys."
sources: ["https://github.com/scylladb/scylladb/blob/master/docs/operating-scylla/admin-tools/scylla-types.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# scylla types

Examines raw values found in SSTables, logs or coredumps: `scylla types <operation> [options] <hex_value1> [hex_value2]`. Operations: `serialize`, `deserialize`, `compare`, `validate`, `tokenof` and `shardof` (the last two accept only partition keys, `--full-compound`). Run `scylla types --help`.

Rules:
- Give values in hex without a leading `0x`.
- State the type with `-t`, using the Cassandra marshal class name; the `org.apache.cassandra.db.marshal.` prefix may be omitted (`Int32Type`). A mapping of CQL types to marshal classes exists in the ScyllaDB dev docs.
- Several values must all share one type.
- `serialize` takes one human-readable value and prints hex; separate values from options with `--` to avoid problems with special symbols.

```
scylla types deserialize -t Int32Type b34b62d4 00783562
```

Compounds (partition keys with several columns, clustering keys): pass `--prefix-compound` or `--full-compound`, and one `-t` per component in the same order as in the compound:

```
scylla types deserialize --prefix-compound -t TimeUUIDType -t Int32Type 0010d00819896f6b11ea00000000001c571b000400000010
```

Use `compare` to see how two serialized values order, and `validate` to check a hex value against the declared type.

## Checked

2026-11-04. Confirmed against scylla-types.rst: syntax, hex without 0x, -t marshal class names, shared type, serialize with --, compound options and the example. Added tokenof and shardof. Removed the claim about dump-index and large partition log lines, which the page does not state.

Method: documentation only; no commands were run.
