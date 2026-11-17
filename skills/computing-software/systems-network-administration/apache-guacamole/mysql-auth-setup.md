---
id: computing-software.systems-network-administration.apache-guacamole.mysql-auth-setup
name: mysql-auth-setup
category: computing-software
field: systems-network-administration
product: apache-guacamole
tags: [systems-network-administration, apache-guacamole, mysql, mariadb, mysql-auth, database-setup, initdb, connector-j, mysql-ssl-mode, jdbc-driver]
level: practitioner
status: docs-checked
description: "Set up Guacamole MariaDB/MySQL authentication: create DB and user, load schema, install extension jar and Connector/J, mysql-* properties and SSL modes, Docker initdb.sh."
sources:
  - https://guacamole.apache.org/doc/gug/mysql-auth.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MariaDB / MySQL authentication

```sql
CREATE DATABASE guacamole_db;
CREATE USER 'guacamole_user' IDENTIFIED BY '<PASSWORD>';
GRANT SELECT,INSERT,UPDATE,DELETE ON guacamole_db.* TO 'guacamole_user';
FLUSH PRIVILEGES;
```
Schema (from `guacamole-auth-jdbc-1.6.0.tar.gz`): `cat schema/*.sql | mysql -u root -p guacamole_db`

Install: copy `mysql/guacamole-auth-jdbc-mysql-1.6.0.jar` to `GUACAMOLE_HOME/extensions/` and a MariaDB or MySQL Connector/J jar to `GUACAMOLE_HOME/lib/` (`GUACAMOLE_HOME` defaults to `/etc/guacamole`). Use a current driver (old Connector/J has SSL verification bugs). Restart Tomcat only.

`guacamole.properties`:
```
mysql-database: guacamole_db
mysql-username: guacamole_user
mysql-password: <PASSWORD>
```
Optional (default): `mysql-hostname` (localhost), `mysql-port` (3306), `mysql-driver` (auto; `mysql` or `mariadb`), `mysql-server-timezone`, `mysql-batch-size` (1000), `mysql-ssl-trust-store`/`-trust-password`, `mysql-ssl-client-store`/`-client-password` (JKS files).

`mysql-ssl-mode` (default `preferred`): `disabled`; `preferred`; `required` (no cert check); `verify-ca`; `verify-identity` (also hostname match).

Docker: set `MYSQL_ENABLED=true`, `MYSQL_DATABASE`, `MYSQL_USERNAME`, `MYSQL_PASSWORD` (+ optional ones above uppercased), then generate the schema:
`docker run --rm guacamole/guacamole /opt/guacamole/bin/initdb.sh --mysql`

Default login `guacadmin`/`guacadmin`; change it.

Verify: log in as guacadmin; Tomcat log shows the MySQL extension loaded.

## Checked

2026-11-04. Confirmed against the Guacamole manual page mysql-auth: CREATE DATABASE/CREATE USER/GRANT statements, schema loading from guacamole-auth-jdbc-1.6.0.tar.gz, extension jar and Connector/J locations, outdated Connector/J SSL warning, required and optional mysql-* properties with defaults (localhost, 3306, 1000), the five mysql-ssl-mode values with preferred as default, Docker MYSQL_* variables and initdb.sh --mysql, and the guacadmin default login. Changed: install paths now use GUACAMOLE_HOME as the page does. The Verify line about the Tomcat log is practical advice, not a page claim.

Method: documentation only; no commands were run.
