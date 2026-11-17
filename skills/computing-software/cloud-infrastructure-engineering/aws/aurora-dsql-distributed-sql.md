---
id: computing-software.cloud-infrastructure-engineering.aws.aurora-dsql-distributed-sql
name: aurora-dsql-distributed-sql
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, aurora-dsql, distributed-sql, optimistic-concurrency, multi-region-active-active, postgresql]
level: advanced
status: docs-checked
description: "Build on Aurora DSQL, the serverless distributed PostgreSQL-compatible database: IAM token auth, optimistic concurrency retries, multi-Region clusters and limits."
sources: ["https://docs.aws.amazon.com/aurora-dsql/latest/userguide/what-is-aurora-dsql.html", "https://docs.aws.amazon.com/aurora-dsql/latest/userguide/working-with-concurrency-control.html", "https://docs.aws.amazon.com/aurora-dsql/latest/userguide/working-with-postgresql-compatibility-unsupported-features.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Aurora DSQL

## 1. Create and connect
```bash
aws dsql create-cluster --deletion-protection-enabled --tags Name=orders
aws dsql get-cluster --identifier <CLUSTER_ID> --query status
TOKEN=$(aws dsql generate-db-connect-admin-auth-token --hostname <CLUSTER_ID>.dsql.<REGION>.on.aws --region <REGION>)
PGPASSWORD="$TOKEN" psql "host=<CLUSTER_ID>.dsql.<REGION>.on.aws user=admin dbname=postgres sslmode=require"
```
- No passwords: IAM-generated tokens (valid 15 minutes by default, up to 604,800 seconds with `--expires-in`).
  The built-in `admin` role is for administration; create custom database roles and map them to IAM roles for apps
  (`AWS IAM GRANT app_role TO 'arn:aws:iam::<ACCOUNT_ID>:role/app';`) and use `generate-db-connect-auth-token`
  (admin uses `generate-db-connect-admin-auth-token`).
- The User Guide's psql example uses `PGSSLMODE=require`. A cluster has one built-in database named `postgres`
  (use schemas or separate clusters for separation). `CreateCluster` accepts `deletionProtectionEnabled`, `tags`,
  `kmsEncryptionKey` and `multiRegionProperties`; cluster status values include `CREATING`, `ACTIVE`, `IDLE`, `INACTIVE`,
  `UPDATING`, `DELETING`, `FAILED`.
- No instances to size; storage and compute scale automatically.

## 2. Optimistic concurrency control
Transactions do not take locks; conflicts are detected at commit. A conflicting commit fails with a
PostgreSQL serialization failure, SQLSTATE `40001`, with an OCC code in the message: `OC000` data conflict, `OC001`
schema conflict. **Every write path needs retry** with idempotent transaction logic. Keep transactions short and spread
updates across the key range (the docs recommend random primary keys such as UUIDs) rather than hammering hot rows.

## 3. Multi-Region
Multi-Region clusters peer clusters in read/write Regions and use a designated witness Region that stores
transaction logs only and has no endpoint. The User Guide describes strongly consistent availability across the
Regions. Multi-Region clusters can only be created within the Region sets listed on the What is Aurora DSQL page.

## 4. Compatibility notes (check the current list)
From the migration page: use `CREATE INDEX ASYNC` for non-blocking index creation; `TRUNCATE` is replaced by `DELETE`
or drop and recreate; no temporary tables (use CTEs, subqueries or regular tables); SQL functions are supported but
not procedural languages such as PL/pgSQL; the page recommends application-level logic instead of triggers; foreign
keys are supported. Limits listed there: isolation level fixed at Repeatable Read; DDL and DML need separate
transactions; one DDL statement per transaction; at most 3,000 rows modified per transaction; connections time out
after 1 hour; C collation only; UTC system time zone.

## Verify
- [ ] Load test with concurrent writers shows retries succeed and no lost updates.
- [ ] App connects with role-mapped IAM tokens, not admin.

## Checked
Date: 2026-10-27. Sources: Aurora DSQL User Guide pages working-with-concurrency-control (SQLSTATE 40001, OC000,
OC001), working-with-postgresql-compatibility-unsupported-features (limits and alternatives), authentication-authorization
and the token page (token lifetime, endpoint format, `AWS IAM GRANT`, psql example), disaster-recovery-resiliency
(witness Region); botocore `dsql` model (CreateCluster members, cluster status enum). Corrected: foreign keys are
supported (the draft said not enforced). Removed the unconfirmed "limited extensions", transaction duration and
commit latency claims. Multi-Region Region sets and service quotas were not read.
Method: documentation only; no commands were run.
