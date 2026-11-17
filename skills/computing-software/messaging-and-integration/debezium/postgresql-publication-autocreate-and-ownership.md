---
id: computing-software.messaging-and-integration.debezium.postgresql-publication-autocreate-and-ownership
name: postgresql-publication-autocreate-and-ownership
category: computing-software
field: messaging-and-integration
product: debezium
tags: [postgresql, pgoutput, publication, ownership]
level: advanced
status: docs-checked
description: "Control how Debezium creates PostgreSQL publications with publication.autocreate.mode and shared table ownership."
sources:
  - https://debezium.io/documentation/reference/stable/connectors/postgresql.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
With `pgoutput`, Debezium streams from a PostgreSQL publication named by `publication.name` (default `dbz_publication`). The docs recommend creating publications manually for the tables you capture before first start. If the publication already exists, Debezium uses it as defined, whether it covers all tables or a subset.

`publication.autocreate.mode` (default `all_tables`) controls creation:

- `all_tables`: use the publication if it exists, otherwise create one for all tables.
- `filtered`: create a publication limited by the connector include and exclude lists.
- `disabled`: never create; if the publication is missing the connector throws and stops.

Creating a publication requires replication privileges, `CREATE` on the database, `SELECT` on the tables, and ownership of each table added. Because source tables already have an owner, share ownership through a group role:

```sql
CREATE ROLE <replication_group>;
GRANT REPLICATION_GROUP TO <original_owner>;
GRANT REPLICATION_GROUP TO <replication_user>;
ALTER TABLE <table_name> OWNER TO REPLICATION_GROUP;
```

`filtered` mode is required for Debezium to apply its own capture configuration. The connector also pushes `skipped.operations` into the publication via `WITH (publish = ...)`.

Gotcha: if a publication predates your deployment and is not `FOR ALL TABLES`, add the heartbeat table with `ALTER PUBLICATION <name> ADD TABLE <heartbeat_table>;`.

Check: list the publication's tables in PostgreSQL and confirm they match the tables you intend to capture.

## Checked

2026-11-03. Page used: the Debezium postgresql connector reference, https://debezium.io/documentation/reference/stable/connectors/postgresql.html.
Confirmed against it: publication.name default, manual creation recommendation, publication.autocreate.mode values, required privileges and shared ownership role, skipped.operations publish clause, heartbeat table in publication.
Removed or reworded: the silent-skip wording and the pg_publication_tables query.
Method: documentation only; no commands were run.
