---
id: computing-software.devops-ci-cd.gitea.database-preparation
name: database-preparation
category: computing-software
field: devops-ci-cd
product: gitea
tags: [gitea-database-prep, gitea, mysql, mariadb, postgresql, utf8mb4-bin, scram-sha-256, pg-hba]
level: practitioner
status: docs-checked
description: "Prepare MySQL/MariaDB or PostgreSQL for Gitea: user, UTF-8 database, collation, pg_hba rule order, remote bind addresses and connection tests."
sources: ["https://gitea.com/gitea/docs/src/branch/main/docs/installation/database-preparation.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Preparing a database for Gitea

Supported engines per the docs: PostgreSQL >= 12, MySQL >= 8.0, MariaDB >= 10.4, SQLite (built in) and MSSQL >= 2012 SP4. Pick the final engine at first install: converting between types is described as not well tested, and SQLite does not scale.

## MySQL/MariaDB
1. Remote DB only: set `bind-address` under `[mysqld]` in `/etc/mysql/my.cnf`.
2. `mysql -u root -p`, then create the user. Local: `CREATE USER 'gitea'@'%' IDENTIFIED BY '<password>';` Remote: use the Gitea host IP instead of `%` (the docs first run `SET old_passwords=0;`).
3. Create the database with a case-sensitive collation:
```sql
CREATE DATABASE giteadb CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_bin';
GRANT ALL PRIVILEGES ON giteadb.* TO 'gitea';
FLUSH PRIVILEGES;
```
`utf8mb4_bin` is the common starting collation; at startup Gitea tries to find a better one (`utf8mb4_0900_as_cs` or `uca1400_as_cs`) and alters the database if possible. To force another, set `[database].CHARSET_COLLATION` in `app.ini`.
4. From the Gitea host test with `mysql -u gitea -h <db-ip> -p giteadb` (omit `-h` for a local DB).

## PostgreSQL
1. Remote DB only: set `listen_addresses = 'localhost, <db-ip>'` in `postgresql.conf`.
2. Switch from the md5 scheme to `password_encryption = scram-sha-256` and restart.
3. As superuser: `CREATE ROLE gitea WITH LOGIN PASSWORD '<password>';`
4. `CREATE DATABASE giteadb WITH OWNER gitea TEMPLATE template0 ENCODING UTF8 LC_COLLATE 'en_US.UTF-8' LC_CTYPE 'en_US.UTF-8';`
5. Add a rule to `pg_hba.conf`: local `local giteadb gitea scram-sha-256`, remote `host giteadb gitea <gitea-ip>/32 scram-sha-256`. Rules are evaluated top-down and the first match wins, so a generic catch-all rule above yours will override it; place yours above. Restart PostgreSQL.
6. Test: `psql -U gitea -d giteadb` (local) or `psql "postgres://gitea@<db-ip>/giteadb"` (remote).

## Collation
The MySQL/MariaDB database needs a UTF-8 charset and a case-sensitive collation, so create it with the statement above.

See `gitea-database-tls` for encrypting the link.

## Checked
2026-11-03. Commands, flags, settings, numbers and behaviour were compared line by line with the Gitea docs source page named in `sources` (read in full from the docs repository raw file). Removed the unsupported "Failure modes" advice (connection-refused diagnosis, same engine version for client tools); kept the collation requirement.
Method: documentation only; no commands were run.
