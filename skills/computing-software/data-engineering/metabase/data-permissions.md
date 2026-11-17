---
id: computing-software.data-engineering.metabase.data-permissions
name: data-permissions
category: computing-software
field: data-engineering
product: metabase
tags: [data-permissions, view-data, create-queries, blocked, all-users, download-results]
level: advanced
status: docs-checked
description: "Configure Metabase data permissions: view data levels, create queries, download limits, how group permissions combine, and why blocking one table disables native SQL."
sources:
  - https://www.metabase.com/docs/latest/permissions/data
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Permission types: View data, Create queries, Download results, Manage table metadata, Manage database and Transform. They can be set on a database, schema or table (some only at certain levels, below).

First step: everyone is automatically in All Users, so block that group's access to the database before granting anything more specific to other groups.

View data levels and where they apply:
- Can view: database, schema, table. The group sees all data from the source, provided it also has collection permissions for the content.
- Granular: database and schema only; it signals that permissions are set one level below. For tables you choose Can view or Sandboxed.
- Row and column security: table level only. Row-level rules from user attributes, or custom views.
- Impersonated: database level only; Metabase defers to a database role.
- Blocked: database, schema, table. Hides the data regardless of collection permissions. It does not hide the query definitions of questions the group can otherwise view.

Create queries: query builder only, query builder plus native, or Granular. It requires the group to be able to view the data source, and it also governs access to the database browser. A group without native permission cannot write SQL, but can still read the SQL of saved native questions in collections it can access.

Download results: No, Granular, 10 thousand rows or 1 million rows.

Other: Manage table metadata is Yes, No or Granular. Manage database opens the database settings page (edit connection options, sync schemas, scan field values); only admins can delete connections. Transform is set at database level only and needs View data plus "Query builder and native" on all tables in that database.

Combining: if a person in a Blocked group is also in a group with "Can view", the more permissive access takes precedence. If Metabase warns that All Users has greater access, All Users must first be set to a less permissive level.

Gotchas:
- Blocked on any table stops the group viewing native-query (SQL) question results for any table in that database, because Metabase does not parse SQL. Likewise Blocked or Row and column security on any table disables native queries for the whole database.
- Native query downloads need download permission for the entire database; Granular download permission does not allow them.
- View data options are not available in open source, which defaults to "Can view"; the setting is shown only in Pro/Enterprise.

## Checked
Method: 2026-11-08 read the cited Metabase permissions/data page in full (raw docs source). Rewrote level-by-level availability, the block-All-Users step, the Blocked/native SQL wording and the download rule to match it; combining and gotcha claims were already accurate.
