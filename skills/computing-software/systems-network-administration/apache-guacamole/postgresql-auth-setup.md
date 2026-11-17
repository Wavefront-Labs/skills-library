---
id: computing-software.systems-network-administration.apache-guacamole.postgresql-auth-setup
name: postgresql-auth-setup
category: computing-software
field: systems-network-administration
product: apache-guacamole
tags: [systems-network-administration, apache-guacamole, postgresql, postgresql-auth, database-setup, initdb, postgresql-ssl-mode, password-policy, connection-limits]
level: practitioner
status: docs-checked
description: "Set up Guacamole PostgreSQL authentication: grants, schema load, extension and JDBC jar, postgresql-* properties, SSL modes, password policy and concurrency limits."
sources:
  - https://guacamole.apache.org/doc/gug/postgresql-auth.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PostgreSQL authentication

```sql
CREATE DATABASE guacamole_db;
CREATE USER guacamole_user WITH PASSWORD '<PASSWORD>';
GRANT SELECT,INSERT,UPDATE,DELETE ON ALL TABLES IN SCHEMA public TO guacamole_user;
GRANT SELECT,USAGE ON ALL SEQUENCES IN SCHEMA public TO guacamole_user;
```
Load the schema (extracted from `guacamole-auth-jdbc-1.6.0.tar.gz`, `postgresql/schema/`):
`cat schema/*.sql | psql -d guacamole_db -f -`
Docker: `docker run --rm guacamole/guacamole /opt/guacamole/bin/initdb.sh --postgresql | psql -d guacamole_db -f -`

Install `postgresql/guacamole-auth-jdbc-postgresql-1.6.0.jar` in `GUACAMOLE_HOME/extensions/` and the PostgreSQL JDBC driver in `GUACAMOLE_HOME/lib/` (`GUACAMOLE_HOME` defaults to `/etc/guacamole`); restart Tomcat. Docker: `POSTGRESQL_ENABLED=true` (false disables even with other vars).

Required: `postgresql-database`, `postgresql-username`, `postgresql-password`. Defaults: `postgresql-hostname` localhost, `postgresql-port` 5432, `postgresql-batch-size` 5000, `postgresql-default-statement-timeout` 0, `postgresql-socket-timeout` 0.

`postgresql-ssl-mode` (default `prefer`): `disable`, `allow`, `prefer`, `require`, `verify-ca`, `verify-full`; PEM files via `-ssl-cert-file`, `-ssl-key-file`, `-ssl-root-cert-file`, `-ssl-key-password`.

Password policy (all off by default): `postgresql-user-password-min-length`, `-require-multiple-case`, `-require-symbol`, `-require-digit`, `-prohibit-username`, `-min-age`/`-max-age` (days), `-history-size`.

Limits (0 = unlimited): `postgresql-default-max-connections`, `-max-group-connections`, `-max-connections-per-user`, `-absolute-max-connections`.

External users: `postgresql-user-required` (false), `postgresql-auto-create-accounts` (false), `postgresql-track-external-connection-history` (true).

Verify: guacadmin login works; change its password.

## Checked

2026-11-04. Confirmed against the Guacamole manual page postgresql-auth: CREATE DATABASE, user and GRANT statements, schema loading with psql and initdb.sh, extension jar and JDBC driver locations, required and optional postgresql-* properties with defaults (5432, 5000, timeouts 0), the postgresql-ssl-mode values with prefer as default and the PEM file properties, password policy and age/history properties, connection-limit properties where zero means unlimited, and the external-user properties. Changed: install paths now use GUACAMOLE_HOME as the page does.

Method: documentation only; no commands were run.
