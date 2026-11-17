---
id: computing-software.data-engineering.metabase.impersonation
name: impersonation
category: computing-software
field: data-engineering
product: metabase
tags: [impersonation, database-roles, user-attributes, connection-impersonation, native-sql]
level: sme
status: docs-checked
description: "Use Metabase connection impersonation so queries run under a database role: supported databases, setup steps, per-database caveats and the single-SELECT limit."
sources:
  - https://www.metabase.com/docs/latest/permissions/impersonation
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Availability: Pro and Enterprise only, self-hosted or Cloud. Supported databases: ClickHouse, MySQL, PostgreSQL, Redshift, Snowflake, SQL Server and Starburst/Trino.

Setup:
1. Create a database role with the desired privileges, such as row-level policies.
2. Give the Metabase connection user access to everything any group might need, because it also handles sync and scans.
3. Create a group and add a user attribute to each member; the value must match the database role name.
4. In Permissions set View data to Impersonation for that group and database.
5. Set Create queries to allow native SQL if needed.

Gotchas:
- Redshift connection users must be superusers.
- Snowflake users must have secondary roles disabled.
- Attribute values may be case sensitive.
- Block the All Users group's broader access first.
- Admins do not see impersonation effects, so test with a separate user.

Limitations:
- Native SQL must be a single SELECT statement.
- Hand-typed lists over 2,000 items are rejected.
- Slack alerts and subscriptions are unavailable; email works.
- Model persistence does not work with impersonation.

## Checked
2026-11-03. Confirmed against the Metabase docs page Permissions, Impersonation permissions (and the Model persistence page for the last limitation): supported databases, setup steps, Redshift superuser and Snowflake secondary-roles requirements, case sensitivity, All Users warning, admin override, single SELECT rule, 2,000-item literal list limit, Slack notification restriction. Nothing removed.
Method: documentation only; no commands were run.
