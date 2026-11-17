---
id: computing-software.database-administration.cockroachdb.logical-data-replication-setup
name: logical-data-replication-setup
category: computing-software
field: database-administration
product: cockroachdb
tags: [logical-data-replication, ldr, create-logically-replicated, unidirectional, bidirectional]
level: advanced
status: docs-checked
description: "Set up CockroachDB logical data replication between two clusters at table level: privileges, external connections, CREATE LOGICALLY REPLICATED and stream syntax."
sources:
  - https://www.cockroachlabs.com/docs/stable/set-up-logical-data-replication
  - https://www.cockroachlabs.com/docs/stable/logical-data-replication-overview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: replicate selected tables between two active clusters (two-datacenter write locality, or workload isolation).

Two syntaxes:
- `CREATE LOGICALLY REPLICATED`: creates the destination table automatically with a fast offline initial scan; accepts `unidirectional` or `bidirectional ON`.
- `CREATE LOGICAL REPLICATION STREAM`: use when the matching destination table already exists; required if the table has user-defined types.
Check the schema validation notes (matching columns and unique secondary indexes) before starting.

Prepare:
```sql
SET CLUSTER SETTING kv.rangefeed.enabled = true;   -- on the source
CREATE USER {your_username} WITH PASSWORD '{your_password}';
GRANT REPLICATIONSOURCE ON TABLE {db}.{schema}.{table} TO {your_username};   -- source
GRANT REPLICATIONDEST ON TABLE {db}.{schema}.{table} TO {your_username};     -- destination, existing table
GRANT CREATE ON DATABASE {db} TO {your_username};   -- destination, for CREATE LOGICALLY REPLICATED
```
For reverse or bidirectional streams grant the opposite privileges in the reverse direction.

Connect destination to source:
```shell
cockroach convert-url --url "postgresql://{user}:{password}@{node IP}:26257" --format crdb --ca-cert {path to CA certificate} --inline
```
```sql
CREATE EXTERNAL CONNECTION {source} AS 'postgresql://{user}:{password}@{node IP}:26257?options=-ccluster%3Dsystem&sslinline=true&sslmode=verify-full&sslrootcert=<encoded-CA>';
```
Start:
```sql
CREATE LOGICALLY REPLICATED TABLE {db.public.dest} FROM TABLE {db.public.src} ON 'external://source' WITH unidirectional;
CREATE LOGICAL REPLICATION STREAM FROM TABLE {db.public.src} ON 'external://{source_external_connection}' INTO TABLE {db.public.dest};
```
Both accept multiple tables in parentheses.

Verify: `SHOW LOGICAL REPLICATION JOBS;` lists the job.

## Checked
2026-11-03. Confirmed on the set-up logical data replication page: self-hosted only, both clusters active, the two syntaxes and when each is required, `unidirectional` and `bidirectional ON`, the `REPLICATIONSOURCE`/`REPLICATIONDEST` table grants and `GRANT CREATE ON DATABASE`, reverse-direction grants for bidirectional, `convert-url` and external connection steps, and `SHOW LOGICAL REPLICATION JOBS`. Removed: the per-table unreplicated tables remark and the insert/read verify.
Method: documentation only; no commands were run.
