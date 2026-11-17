---
id: computing-software.devops-ci-cd.rundeck.postgres-database-backend
name: postgres-database-backend
category: computing-software
field: devops-ci-cd
product: rundeck
tags: [rundeck, postgres, datasource, rundeck-config-properties, database-backend]
level: practitioner
status: docs-checked
description: "Create a PostgreSQL database and user for Rundeck and point rundeck-config.properties at it with the dataSource settings; EDB is unsupported."
sources:
  - https://raw.githubusercontent.com/rundeck/docs/4.0.x/docs/administration/configuration/database/postgres.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Create the database and user in `psql` as the postgres user (names and password below are the page's examples):

```sql
create database rundeck;
create user rundeckuser with password 'rundeckpassword';
grant ALL privileges on database rundeck to rundeckuser;
\c rundeck;
grant ALL privileges on schema public to rundeckuser;
```

Set the datasource in `rundeck-config.properties`:

```properties
dataSource.driverClassName = org.postgresql.Driver
dataSource.url = jdbc:postgresql://pgsql.rundeck.local/rundeck
dataSource.username = rundeckuser
dataSource.password = rundeckpassword
```

Then start Rundeck. Recent versions bundle the PostgreSQL connector, so no driver jar is needed.

Gotchas:
- You may also need a `pg_hba.conf` entry for the new user.
- Enterprise DB (EDB) is not supported even though it is Postgres-based.
- Amazon Aurora PostgreSQL below 15.3.0 logs harmless `unrecognized node type: 378` warnings; queries still run.

Verify: start the server and check `service.log` for database connection errors.

## Checked

2026-11-04. Confirmed against the Rundeck docs page Using Postgres as a database backend: psql statements, dataSource settings, bundled PostgreSQL connector, pg_hba.conf note, EDB unsupported warning, and the Aurora PostgreSQL below 15.3.0 unrecognized node type: 378 warning. Nothing removed.

Method: documentation only; no commands were run.
