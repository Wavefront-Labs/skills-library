---
id: computing-software.database-administration.cassandra.udf-and-uda
name: udf-and-uda
category: computing-software
field: database-administration
product: cassandra
tags: [cassandra, udf, uda, enable-user-defined-functions, user-defined-functions, aggregates, cql-functions, nosql, wide-column, cql]
level: practitioner
status: docs-checked
description: "Defining server-side functions"
sources: ["https://cassandra.apache.org/doc/latest/", "https://github.com/apache/cassandra/blob/trunk/conf/cassandra.yaml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# User-defined functions and aggregates

Goal: add functions with eyes open.
- Enable `user_defined_functions_enabled: true` in cassandra.yaml (default `false`; JavaScript UDFs are deprecated since 4.1).
- `CREATE FUNCTION f(x int) CALLED ON NULL INPUT RETURNS int LANGUAGE java AS 'return x+1;'`.
- UDFs run sandboxed, but the docs warn no sandbox is perfect; slow ones hurt latency.
- Built-ins: `count`, `sum`, `avg`, `min`, `max`, `token()`.
Verify: `SELECT f(col) FROM t LIMIT 1` works.

## Checked

2026-11-02. Confirmed against Apache Cassandra trunk docs (doc/modules/cassandra/pages) and conf/cassandra.yaml, nodetool sources: user_defined_functions_enabled default false, CREATE FUNCTION ... CALLED ON NULL INPUT, sandbox warning, JavaScript deprecation, count/sum/avg/min/max and token() (functions page, cassandra.yaml).
Removed: scripted-UDF flag and `toJson()` (docs use `from_json()`).
Method: documentation only; no commands were run.
