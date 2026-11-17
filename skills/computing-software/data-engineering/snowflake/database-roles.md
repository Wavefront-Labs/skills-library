---
id: computing-software.data-engineering.snowflake.database-roles
name: database-roles
category: computing-software
field: data-engineering
product: snowflake
tags: [snowflake, snowflake-rbac, database-roles, access-roles, functional-roles, role-hierarchy, data-sharing, grants, share-database-roles]
level: practitioner
status: docs-checked
description: "Use Snowflake database roles as database-scoped access roles: create, grant privileges, nest into account roles, use them in shares and clones, and their limits."
sources:
  - https://docs.snowflake.com/en/user-guide/security-access-control-overview#database-roles
  - https://docs.snowflake.com/en/sql-reference/sql/create-database-role
licence: Apache-2.0
version: 5
updated: 2026-11-17
---

# Database roles

**Goal:** keep object privileges inside each database (portable with clones, replication and shares) and map people to them through account-level functional roles.

## Access-role pattern with database roles
```sql
use role SECURITYADMIN;   -- or the database owner
create database role sales.reader;
create database role sales.writer;

grant usage on database sales to database role sales.reader;
grant usage on all schemas in database sales to database role sales.reader;
grant select on all tables in database sales to database role sales.reader;
grant select on future tables in database sales to database role sales.reader;   -- future grants at db level
grant database role sales.reader to database role sales.writer;
grant insert, update, delete on future tables in schema sales.core to database role sales.writer;

-- functional (account) roles get database roles
grant database role sales.reader to role ANALYST;
grant database role sales.writer to role DBT_TRANSFORMER;
```

## Why database roles
- **Clones:** a database role is cloned when you clone the whole database; cloning only a schema or table does not clone the database roles. Cloned dev databases come with ready-made reader/writer roles.
- **Sharing:** a share can include database roles so you can expose different subsets of a shared database to different consumers. Consumers grant the imported database roles to roles in their own account.

## Limits
- A database role cannot be activated directly in a session (`use role` does not work on it); it must be granted to an account role.
- Grant database roles to account roles (which can be activated in a session) rather than to users.

## Inspect
```sql
show database roles in database sales;
show grants to database role sales.reader;
show grants of database role sales.reader;
```

## Gotchas
- Future grants at both database and schema level: schema-level future grants take precedence, and database-level ones are ignored for that schema. Pick one level consistently.
- `MANAGED ACCESS` schemas centralise grant decisions at the schema level, which fits central control with database roles.

## Verify
- [ ] Analyst session can read sales tables only through the inherited database role.
- [ ] Cloned database `dev_sales` contains `reader`/`writer` database roles with grants.

## Checked

2026-10-28: reviewed against the Snowflake documentation fetched this batch.

Confirmed: database roles cannot be activated directly and must be granted to account roles; schema-level future grants take precedence over database-level ones on the same object type; database roles are cloned with a database clone only; consumers grant imported database roles to their own roles (access-control-overview, create-clone, data-share-consumers pages).

Removed or corrected: claims about same-database nesting, outside-database privileges, direct grants to users, delegated admin, share grant syntax and the Terraform resource name (not on the pages read).

Method: documentation only; no commands were run.
