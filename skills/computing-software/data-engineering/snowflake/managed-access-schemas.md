---
id: computing-software.data-engineering.snowflake.managed-access-schemas
name: managed-access-schemas
category: computing-software
field: data-engineering
product: snowflake
tags: [snowflake, managed-access-schema, access-control, grants, rbac]
level: practitioner
status: docs-checked
description: "Centralise grant management in Snowflake with managed access schemas so object owners cannot grant privileges, plus future grants and migration of existing schemas."
sources:
  - https://docs.snowflake.com/en/user-guide/security-access-control-configure#creating-managed-access-schemas
  - https://docs.snowflake.com/en/sql-reference/sql/create-schema
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Managed access schemas

**Goal:** grant decisions are made at the schema level (schema owner or a role with MANAGE GRANTS), not by whichever role created each table.

## Why
In a normal schema the **object owner** can grant access to anyone. With many roles creating objects (dbt, ingestion, analysts), access sprawls. Managed access moves grant decisions to the schema level.

## Create / convert
```sql
CREATE SCHEMA analytics.marts WITH MANAGED ACCESS;
ALTER SCHEMA analytics.staging ENABLE MANAGED ACCESS;   
ALTER SCHEMA analytics.sandbox DISABLE MANAGED ACCESS;
SHOW SCHEMAS IN DATABASE analytics;
```

## Granting inside
```sql
USE ROLE marts_owner;   -- schema owner, or a role with MANAGE GRANTS
GRANT SELECT ON ALL TABLES IN SCHEMA analytics.marts TO ROLE reporter;
GRANT SELECT ON FUTURE TABLES IN SCHEMA analytics.marts TO ROLE reporter;
```

## Pattern
- Schema owned by an access-admin role per domain; transformation role has CREATE TABLE/VIEW on the schema.
- Read access via database roles or functional roles granted at schema level with future grants.

## Gotchas
- `MANAGE GRANTS` is account-wide and powerful; keep it to security admins.
- When future grants are defined on the same object type at database and schema level, the schema-level grants take precedence and the database-level ones are ignored.

## Verify
`SHOW GRANTS` on a table in the schema shows only grants made by the schema owner or a MANAGE GRANTS role.

## Checked

2026-10-28: reviewed against the Snowflake documentation fetched this batch.

Confirmed: CREATE SCHEMA ... WITH MANAGED ACCESS syntax, grant management needs OWNERSHIP or global MANAGE GRANTS, schema-level future grants take precedence (create-schema, access-control-configure, access-control-overview pages).

Removed or corrected: ENABLE/DISABLE MANAGED ACCESS comment details, dbt grants behaviour, owner-cannot-grant error, ownership-transfer claim and the SHOW SCHEMAS options column (not on the pages read).

Method: documentation only; no commands were run.
