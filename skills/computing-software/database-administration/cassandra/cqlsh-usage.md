---
id: computing-software.database-administration.cassandra.cqlsh-usage
name: cqlsh-usage
category: computing-software
field: database-administration
product: cassandra
tags: [cassandra, cqlsh-ssl, cqlsh-paging, cqlshrc, cqlsh, describe, sstabledump, nosql, wide-column, cql]
level: practitioner
status: docs-checked
description: "Connecting and shaping output"
sources: ["https://cassandra.apache.org/doc/latest/", "https://github.com/apache/cassandra/blob/trunk/conf/cassandra.yaml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# cqlsh sessions and options

Goal: use cqlsh effectively.
- `cqlsh [options] [host [port]]`, for example `cqlsh <host> 9042 -u user --ssl`; `~/.cassandra/cqlshrc` (or `--cqlshrc`) holds defaults, including credentials (protect that file on shared hosts).
- `DESCRIBE KEYSPACES`, `DESCRIBE KEYSPACE <name>`, `DESCRIBE TABLE <name>`, `DESCRIBE SCHEMA`, plus `PAGING`, `EXPAND`, `CAPTURE`, `SOURCE`.
- `--request-timeout` sets the default request timeout in seconds (default 10).
Verify: DESCRIBE output rebuilds the schema on a new cluster.

## Checked

2026-11-02. Confirmed against Apache Cassandra trunk docs (doc/modules/cassandra/pages) and conf/cassandra.yaml, nodetool sources: cqlsh usage line, --ssl, -u/--username, --cqlshrc and ~/.cassandra/cqlshrc, --request-timeout default 10 s, DESCRIBE forms, PAGING/EXPAND/CAPTURE/SOURCE (cqlsh page).
Removed: the quoted `SOURCE 'file.cql'` form.
Method: documentation only; no commands were run.
