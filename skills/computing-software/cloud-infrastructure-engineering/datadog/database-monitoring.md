---
id: computing-software.cloud-infrastructure-engineering.datadog.database-monitoring
name: database-monitoring
category: computing-software
field: cloud-infrastructure-engineering
product: datadog
tags: [datadog, database-monitoring, dbm, query-samples, explain-plans]
level: practitioner
status: docs-checked
description: "Enable Database Monitoring for self-hosted Postgres with a read-only Agent user, query metrics and explain plans."
sources: ["https://docs.datadoghq.com/database_monitoring/setup_postgres/selfhosted/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Database Monitoring
Goal: query-level performance visibility.

Postgres self-hosted setup (Agent 7.36.1 or later; Postgres 9.6 to 18). Set in `postgresql.conf` and restart the server:

```
shared_preload_libraries = 'pg_stat_statements'
track_activity_query_size = 4096
```

Run on the primary as a superuser, with the schema steps repeated in every database (Postgres 10 and later):

```sql
CREATE USER datadog WITH password '<PASSWORD>';
CREATE SCHEMA datadog;
GRANT USAGE ON SCHEMA datadog TO datadog;
GRANT USAGE ON SCHEMA public TO datadog;
GRANT pg_monitor TO datadog;
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;
```

```yaml
# conf.d/postgres.d/conf.yaml
init_config:
instances:
 - dbm: true
   host: localhost
   port: 5432
   username: datadog
   password: 'ENC[datadog_user_database_password]'
```

- On Postgres 15 and later also run `ALTER ROLE datadog INHERIT;`. On 9.6, grant `SELECT ON pg_stat_database` instead of `pg_monitor` and create `SECURITY DEFINER` wrapper functions `datadog.pg_stat_activity()` and `datadog.pg_stat_statements()`.
- Explain plans need a `datadog.explain_statement(l_query TEXT, OUT explain JSON)` plpgsql function, created in every database with `SECURITY DEFINER`; copy it from the docs page.
- `track_activity_query_size` at the default means queries over 1024 characters are not collected.
- Optional parameters: `pg_stat_statements.track = ALL`, `pg_stat_statements.max = 10000`, `pg_stat_statements.track_utility = off`, `track_io_timing = on`.
- Wrap a password with special characters in single quotes, then restart the Agent.
- The Agent must connect directly to the database host, not through a proxy, load balancer or pooler such as `pgbouncer`; with failover it would compute statistic differences between two hosts and give inaccurate metrics.
- The docs describe the default Agent load as under one percent of query execution time and CPU.

Gotcha: the Agent user is read-only; do not make it a superuser. Run the docs' verification `psql` commands as the `datadog` user to confirm it can read `pg_stat_database`, `pg_stat_activity` and `pg_stat_statements`.

## Verify
- Run `select * from pg_stat_statements limit 1;` as the datadog user (on 9.6 use `datadog.pg_stat_statements()`), then check Agent status for the postgres check.

## Checked
2026-11-09. Confirmed against the Postgres self-hosted setup page (versions, parameters, user and schema SQL per version, INHERIT step, explain function, password quoting, direct-connection rule, verification commands, performance statement). Removed: all MySQL and `performance_schema` content (MySQL page not read), the "separate user per instance", password-rotation and network-restriction advice, the comparison with slow query logs, the claim that obfuscation hides literals (the docs only point to a Sensitive information page), and the `Databases > Query Metrics` and `[OK]` status wording.
Method: documentation only; no commands were run.
