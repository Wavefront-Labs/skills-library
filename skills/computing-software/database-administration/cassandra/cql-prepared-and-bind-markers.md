---
id: computing-software.database-administration.cassandra.cql-prepared-and-bind-markers
name: cql-prepared-and-bind-markers
category: computing-software
field: database-administration
product: cassandra
tags: [cassandra, bind-markers, identifiers-quoting, cql-comments, nosql, wide-column, cql]
level: practitioner
status: docs-checked
description: "Language fundamentals"
sources: ["https://cassandra.apache.org/doc/latest/cassandra/developing/cql/definitions.html", "https://cassandra.apache.org/doc/latest/cassandra/developing/cql/appendices.html", "https://cassandra.apache.org/doc/latest/cassandra/developing/cql/cql_singlefile.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CQL syntax details

Goal: write portable CQL.
- Unquoted identifiers and keywords are case-insensitive; quoted identifiers use double quotes; string constants use single quotes (a quote inside is doubled).
- Bind markers are `?` or `:name`; they can also supply values for LIMIT, TIMESTAMP and TTL.
- Reserved keywords cannot be identifiers unless double-quoted; avoid them.
Verify: statements prepare without error.

## Checked

2026-11-03. Confirmed against the Apache Cassandra documentation: identifier case rules, single-quoted string constants, `bind_marker ::= '?' | ':' identifier`, reserved keywords (CQL definitions, appendices, single-file reference). Removed: nothing.

Method: documentation only; no commands were run.
