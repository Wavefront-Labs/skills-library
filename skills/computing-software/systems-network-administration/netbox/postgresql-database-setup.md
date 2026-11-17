---
id: computing-software.systems-network-administration.netbox.postgresql-database-setup
name: postgresql-database-setup
category: computing-software
field: systems-network-administration
product: netbox
tags: [postgresql, database-creation, utf8-encoding]
level: practitioner
status: docs-checked
description: "Create the database, owner role and schema grant NetBox needs, and avoid SQL_ASCII."
sources: ["https://netboxlabs.com/docs/netbox/installation/1-postgresql/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# PostgreSQL database setup

Goal: prepare PostgreSQL for a NetBox install.

NetBox requires PostgreSQL 15 or later. MySQL and other relational databases are not supported. Verify with `psql -V`.

**Create database and role** (from `sudo -u postgres psql`):
```
CREATE DATABASE netbox;
CREATE USER netbox WITH PASSWORD '<strong-random-password>';
ALTER DATABASE netbox OWNER TO netbox;
\connect netbox;
GRANT CREATE ON SCHEMA public TO netbox;
```
Use a strong random password, not the docs' example one.

**Encoding.** Use UTF8 (the default for new installs). Never use SQL_ASCII, which can cause unpredictable and unrecoverable errors. Check with `\l`.

**Verify authentication** by connecting with the configured credentials:
```
psql --username netbox --password --host localhost netbox
```
At the `netbox=>` prompt, `\conninfo` confirms database, user, host and port; `\q` exits. Replace `localhost` with your server if the database is remote.

Making the NetBox user the database owner also satisfies the later `ltree` extension requirement for v4.7 and newer.

**Checklist**

1. PostgreSQL 15 or later.
2. Owner and schema grant applied.
3. UTF8 confirmed.
4. Login tested with the role.

## Checked

2026-11-03: confirmed against the cited NetBox documentation: PostgreSQL page: PostgreSQL 15 or later, CREATE DATABASE/USER/OWNER and GRANT CREATE statements, UTF8 and SQL_ASCII warning, connection test, ltree requirement for v4.7. Removed: Nothing.

Method: documentation only; no commands were run.
