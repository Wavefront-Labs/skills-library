---
id: computing-software.database-administration.cockroachdb.physical-cluster-replication-setup
name: physical-cluster-replication-setup
category: computing-software
field: database-administration
product: cockroachdb
tags: [physical-cluster-replication, pcr, standby-cluster, virtualized, replication-privileges]
level: advanced
status: docs-checked
description: "Set up CockroachDB physical cluster replication from a primary to a standby: --virtualized init flags, rangefeed, replication privileges, external connection."
sources:
  - https://www.cockroachlabs.com/docs/stable/set-up-physical-cluster-replication
  - https://www.cockroachlabs.com/docs/stable/physical-cluster-replication-overview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: stream a whole primary cluster to a standby for disaster recovery (replication lag generally tens of seconds; optional `SELECT` on the standby).

Prerequisites: both clusters are initialized as virtualized: primary with `--virtualized`, standby with `--virtualized-empty`. The standby must run the same version or one major version ahead. PCR is supported on self-hosted clusters from v23.2.

Primary (connected to the system virtual cluster):
```sql
SET CLUSTER SETTING kv.rangefeed.enabled = true;
CREATE USER {your username} WITH PASSWORD '{your password}';
GRANT SYSTEM REPLICATIONSOURCE TO {your username};
```
```shell
cockroach init --certs-dir=certs --host={address of any node on --join list} --virtualized
```
Standby: init with `--virtualized-empty`, set `kv.rangefeed.enabled`, then
```sql
CREATE USER {your username} WITH LOGIN PASSWORD {'your password'};
GRANT SYSTEM REPLICATIONDEST, MANAGEVIRTUALCLUSTER TO {your username};
```
Connection string: use `cockroach convert-url --url "postgresql://{user}:{password}@{host}:26257" --format crdb --ca-cert certs/ca.crt --inline` to inline the CA, then on the standby:
```sql
CREATE EXTERNAL CONNECTION {source} AS 'postgresql://{user}:{password}@{host}:26257/defaultdb?options=-ccluster%3Dsystem&sslinline=true&sslmode=verify-full&sslrootcert=<inlined-CA>';
CREATE VIRTUAL CLUSTER main FROM REPLICATION OF main ON '{source}';
```
(The page also shows `crdb_route=gateway` for load balancer setups.) Control and watch:
```sql
SHOW VIRTUAL CLUSTERS;
ALTER VIRTUAL CLUSTER main PAUSE REPLICATION;
ALTER VIRTUAL CLUSTER main RESUME REPLICATION;
SHOW VIRTUAL CLUSTER main WITH REPLICATION STATUS;
```
Verify: `SHOW VIRTUAL CLUSTERS;` on the standby shows `main` with data state `replicating`; `SHOW VIRTUAL CLUSTER main WITH REPLICATION STATUS;` shows `replicated_time` and `replication_lag`.

## Checked
2026-11-03. Confirmed on the set-up and overview pages: tens-of-seconds lag, optional standby `SELECT`, v23.2 self-hosted support, standby same version or one ahead, `--virtualized` and `--virtualized-empty`, `kv.rangefeed.enabled`, `REPLICATIONSOURCE`, `REPLICATIONDEST`, `MANAGEVIRTUALCLUSTER` grants, `cockroach convert-url ... --inline`, `CREATE EXTERNAL CONNECTION`, `crdb_route=gateway`, `CREATE VIRTUAL CLUSTER`, pause/resume and status statements. Removed: the identical zone configuration claim (page text is not readable on this point).
Method: documentation only; no commands were run.
