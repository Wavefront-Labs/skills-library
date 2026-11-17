---
id: computing-software.systems-network-administration.apache-guacamole.sqlserver-auth-setup
name: sqlserver-auth-setup
category: computing-software
field: systems-network-administration
product: apache-guacamole
tags: [systems-network-administration, apache-guacamole, sql-server, sqlserver, sqlserver-auth, database-setup, sqlcmd, jdbc-driver, microsoft2005, jtds, datadirect]
level: practitioner
status: docs-checked
description: "Set up Guacamole SQL Server authentication: sqlcmd to create DB, login and roles, run schema scripts, install extension and JDBC driver, sqlserver-* properties and driver values."
sources:
  - https://guacamole.apache.org/doc/gug/sqlserver-auth.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SQL Server authentication

With `sqlcmd` as SA:
```
CREATE DATABASE guacamole_db;
GO
CREATE LOGIN guacamole_user WITH PASSWORD = '<PASSWORD>';
GO
USE guacamole_db;
GO
CREATE USER guacamole_user;
GO
ALTER ROLE db_datawriter ADD MEMBER guacamole_user;
ALTER ROLE db_datareader ADD MEMBER guacamole_user;
GO
```
Schema: run both scripts from `sqlserver/schema/` in order:
```
sqlcmd -S localhost -U SA -d guacamole_db -i schema/001-create-schema.sql
sqlcmd -S localhost -U SA -d guacamole_db -i schema/002-create-admin-user.sql
```
Docker: `docker run --rm guacamole/guacamole /opt/guacamole/bin/initdb.sh --sqlserver > initdb.sql`, then run it with sqlcmd.

Install `sqlserver/guacamole-auth-jdbc-sqlserver-1.6.0.jar` in `GUACAMOLE_HOME/extensions/` and your JDBC driver jar in `GUACAMOLE_HOME/lib/` (GUACAMOLE_HOME defaults to /etc/guacamole). The manual recommends the driver from your database vendor unless you have a reason to use another.

Properties:
```
sqlserver-database: guacamole_db
sqlserver-username: guacamole_user
sqlserver-password: <PASSWORD>
```
Optional (default): `sqlserver-hostname` (localhost), `sqlserver-port` (1433), `sqlserver-instance` (default instance), `sqlserver-batch-size` (500), `sqlserver-driver` (`microsoft2005`; others `microsoft` for SQL Server 2000, `jtds`, `datadirect`). If you do not use the Microsoft driver, `sqlserver-driver` must be set to the driver you installed.

Docker: `SQLSERVER_ENABLED=true` plus the uppercased variables; recreate the container.

The page documents no Windows/NTLM authentication options.

Verify: guacadmin/guacadmin works; change the password.

## Checked

2026-11-04. Confirmed against the Guacamole manual page sqlserver-auth: the sqlcmd database, login, user and role commands, both schema scripts, the Docker initdb.sh --sqlserver extraction, extension and JDBC driver locations under GUACAMOLE_HOME, required sqlserver-* properties, optional properties with defaults and driver values, SQLSERVER_ENABLED behaviour, the Tomcat restart and container recreation, and the guacadmin default login. Changed: reworded the path and driver recommendation to match the page.

Method: documentation only; no commands were run.
