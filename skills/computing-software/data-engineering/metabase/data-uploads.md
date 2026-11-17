---
id: computing-software.data-engineering.metabase.data-uploads
name: data-uploads
category: computing-software
field: data-engineering
product: metabase
tags: [uploads, csv-upload, local-infile, upload-schema, curate-access]
level: intro
status: docs-checked
description: "Set up CSV uploads in Metabase: supported databases, the upload schema and table prefix, user permission requirements, and the MySQL local_infile slowdown."
sources:
  - https://www.metabase.com/docs/latest/databases/uploads
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Supported databases: PostgreSQL, MySQL, Snowflake, Redshift and ClickHouse (ClickHouse Cloud and self-hosted single node only).

Admin setup:
- Connect Metabase with a database user that has write access.
- In Admin, Settings, Uploads, choose the database and schema where uploaded tables are stored.
- Optionally add a prefix for uploaded table names.
- Each upload creates a table plus a model wrapping it, saved to the collection where the CSV was uploaded.

User permissions: the user's group needs "Can view" data access and Query builder "Create queries" access or higher on the upload schema, plus Curate access to the target collection. The upload icon appears only where they have it. Personal collections grant it by default.

Gotchas:
- The docs say uploads suit ad hoc analysis of spreadsheet data. Load large or regularly updated data into the database directly.
- For MySQL, enable `local_infile` on the MySQL server (not in Metabase). If it is disabled, Metabase falls back to much slower uploads.

## Checked
2026-11-03. Confirmed against the Metabase docs page Databases, Setting up data uploads: supported databases (ClickHouse Cloud and self-hosted single node), write-access user, Admin Settings Uploads path, schema and table prefix, table plus model creation, View data and Create queries requirements, Curate access and personal collections, MySQL local_infile guidance. Removed the unsupported line about a separate write role.
Method: documentation only; no commands were run.
