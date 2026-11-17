---
id: computing-software.messaging-and-integration.temporal.upgrade-server-procedure
name: upgrade-server-procedure
category: computing-software
field: messaging-and-integration
product: temporal
tags: [upgrade-server, schema-upgrade, temporal-sql-tool, temporal-cassandra-tool, temporal-elasticsearch-tool, sequential-upgrade, self-hosted]
level: advanced
status: docs-checked
description: "Upgrade self-hosted Temporal Server: sequential minor versions, schema tools for Cassandra, SQL and Elasticsearch, 10-minute shard settle time, staging roll-out."
sources:
  - https://docs.temporal.io/self-hosted-guide/upgrade-server
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Rules:
- Upgrade one minor version at a time. First move to the highest patch of your current minor (v1.n.latest), then to v1.(n+1).latest, and repeat. Minor versions must not be skipped.
- Compatibility is guaranteed only between consecutive minors, and old code paths are eventually removed, so a skipped version can leave data formats unreadable and the upgrade fails.
- Release notes call out whether a schema change is needed.
- Each version makes the History Service load every shard and update shard metadata; allow about 10 minutes per version before the next step.

Per step: update the database schema first, then the server deployment.

Schema tools:
- Cassandra: `temporal-cassandra-tool --tls --tls-ca-file ... --user ... --password ... --endpoint ... --keyspace temporal --timeout 120 update --schema-dir ./schema/cassandra/temporal/versioned`. Repeat with `--keyspace temporal_visibility` and `./schema/cassandra/visibility/versioned`.
- Elasticsearch: `temporal-elasticsearch-tool --endpoint "$ES_SCHEME://$ES_HOST:$ES_PORT" --user ... --password ... update-schema --index "$ES_VISIBILITY_INDEX"`.
- SQL: `temporal-sql-tool --tls --tls-enable-host-verification --tls-cert-file ... --tls-key-file ... --tls-ca-file ... --ep host -p port -u user -pw pass --pl <plugin> --db <db> update-schema -d <dir>`. Plugins and dirs: `postgres` with `./schema/postgresql/v96/{temporal,visibility}/versioned`; `mysql` with `./schema/mysql/v57/...`. For advanced Visibility on v1.20, upgrade PostgreSQL to 12+ first then use `postgres12` (`./schema/postgresql/v12/visibility/versioned`), or MySQL to 8.0.17+ then `mysql8` (`./schema/mysql/v8/visibility/versioned`).

Roll-out: on staging, create simulated load, upgrade the schema, observe a few minutes for instability, upgrade the server, then repeat in production.

## Checked

2026-11-03. Confirmed against the Temporal documentation pages: self-hosted-guide/upgrade-server (under https://docs.temporal.io/). Removed the unconfirmed statement that patch versions may be skipped (the production checklist page does state it, so it is not load-bearing here).

Method: documentation only; no commands were run.
