---
id: computing-software.database-administration.scylladb.security-auditing
name: security-auditing
category: computing-software
field: database-administration
product: scylladb
tags: [audit, auditing, audit-categories, syslog, alternator]
level: practitioner
status: docs-checked
description: "ScyllaDB auditing: audit backends, audit_categories, audit_keyspaces and audit_tables filters, Alternator coverage and performance cost."
sources: ["https://github.com/scylladb/scylladb/blob/master/docs/operating-scylla/security/auditing.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Auditing

Auditing records CQL queries, data changes and Alternator (DynamoDB API) requests to a table or Syslog. Prerequisite: authentication and authorization enabled.

The `audit:` setting in `scylla.yaml` (auditing is enabled by default with the table backend):
- `none`: disabled.
- `table`: messages stored in a ScyllaDB table (default).
- `syslog`: sent to Syslog.
- `syslog,table`: both. Any other value fails startup.

Filters (`scylla.yaml` entries or flags):
- `audit_categories`: comma-separated list.
- `audit_keyspaces`: keyspaces to audit; you must name at least one, since an empty value audits no keyspace.
- `audit_tables`: `<keyspace>.<table>`, or `alternator.<table>` for Alternator tables.
To audit every table in a keyspace set `audit_keyspaces` and leave `audit_tables` empty. DCL, AUTH and ADMIN categories work without any keyspace or table.

Categories:
- `AUTH`: login events (CQL).
- `DML`: insert, update, delete (CQL, Alternator).
- `DDL`: create, alter, drop of objects and roles (CQL, Alternator).
- `DCL`: grant, revoke, create/drop/list role (CQL).
- `QUERY`: all queries (CQL, Alternator).
- `ADMIN`: service level operations (CQL).

Alternator requests use the same backends and filters (no separate settings), successes and failures both; for example CreateTable and DeleteTable are DDL, PutItem and DeleteItem are DML.

Cost: auditing can reduce performance and audit-to-table uses extra storage, especially with DML and QUERY. Scope it narrowly.

## Checked

2026-11-09. Confirmed prerequisites, backend values, filter options, categories, Alternator behaviour and cost warning against the ScyllaDB auditing guide (all sections read). Removed the unsupported claim about the audit keyspace and decommissioning.

Method: docs-checked 2026-11-09 against the ScyllaDB docs page operating-scylla/security/auditing.rst
