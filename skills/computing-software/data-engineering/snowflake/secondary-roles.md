---
id: computing-software.data-engineering.snowflake.secondary-roles
name: secondary-roles
category: computing-software
field: data-engineering
product: snowflake
tags: [snowflake, secondary-roles, rbac, default-secondary-roles, access-control]
level: practitioner
status: docs-checked
description: "Use Snowflake secondary roles: USE SECONDARY ROLES ALL vs specific roles, DEFAULT_SECONDARY_ROLES, what the primary role still controls, and session policy limits."
sources:
  - https://docs.snowflake.com/en/user-guide/security-access-control-overview#authorization-through-primary-role-and-secondary-roles
  - https://docs.snowflake.com/en/sql-reference/sql/use-secondary-roles
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Secondary roles

**Goal:** let a user read across all their granted roles in one session without role switching, while keeping object creation tied to one role.

## Commands
```sql
USE ROLE analyst;                      -- primary role
USE SECONDARY ROLES ALL;               -- all granted roles add read/use privileges
USE SECONDARY ROLES finance_reader, marketing_reader;   -- specific list
USE SECONDARY ROLES NONE;
SELECT CURRENT_ROLE(), CURRENT_SECONDARY_ROLES();
```

## Rules
- **Primary role** alone authorises `CREATE <object>` and becomes the owner of created objects.
- Privileges for all other SQL (SELECT, INSERT, USAGE...) are the union of primary + secondary roles.

## When to turn it off
- Service users and pipelines: run with exactly one role and no secondary roles (`USE SECONDARY ROLES NONE`) so permissions are reproducible. A session starts with the user's default role and default secondary roles.
- Testing RBAC: secondary roles hide missing grants on the role you think you are testing.

## Session policies
The `USE SECONDARY ROLES` page notes that activated secondary roles can be limited by a session policy; see that page for the policy parameters.

## Gotchas
- Users surprised that they can query something "their role" cannot: check `CURRENT_SECONDARY_ROLES()`.
- dbt and BI tools may run `USE SECONDARY ROLES` themselves; check connection settings.

## Verify
As a test user with two roles: with secondary roles ALL, a cross-role join works; with NONE it fails.

## Checked

2026-10-28: reviewed against the Snowflake documentation fetched this batch.

Confirmed: USE SECONDARY ROLES ALL / list syntax, CURRENT_SECONDARY_ROLES(), CREATE statements authorised by the primary role only and owned by it, other privileges from the union of active roles, default role and default secondary roles activate at session start (access-control-overview, use-secondary-roles pages).

Removed or corrected: the ALTER USER DEFAULT_SECONDARY_ROLES line, the CREATE SESSION POLICY ALLOWED_SECONDARY_ROLES example, the warehouse and access-history bullets (parameters not on the pages read).

Method: documentation only; no commands were run.
