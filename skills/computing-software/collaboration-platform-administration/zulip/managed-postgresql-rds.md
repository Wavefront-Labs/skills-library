---
id: computing-software.collaboration-platform-administration.zulip.managed-postgresql-rds
name: managed-postgresql-rds
category: computing-software
field: collaboration-platform-administration
product: zulip
tags: [amazon-rds, managed-database, remote-postgres-host]
level: advanced
status: docs-checked
description: "Run Zulip against a cloud-managed PostgreSQL such as Amazon RDS: installer flags, create-db.sql, REMOTE_POSTGRES settings and the full-text search trade-off."
sources: ["https://zulip.readthedocs.io/en/latest/production/postgresql.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Cloud-managed PostgreSQL (for example Amazon RDS)

A database-as-a-service works, with one cost: most providers ship no useful dictionary files and let you add none, so full-text search relies on weaker built-in stemming and is less useful.

Decide database and user names first; Zulip defaults both to `zulip`, but alternatives are supported if your central server requires a convention.

Install the app server with the remote database profile plus full-text-search update processing, and tell it the names and the server's PostgreSQL version:

```
./zulip-server-*/scripts/setup/install --certbot \
    --email=YOUR_EMAIL --hostname=YOUR_HOSTNAME \
    --puppet-classes=zulip::profile::standalone_nodb,zulip::process_fts_updates \
    --postgresql-database-name=zulip \
    --postgresql-database-user=zulip \
    --postgresql-version=YOUR_SERVERS_POSTGRESQL_VERSION
```

Using an administrative `psql` session, run the commands in `scripts/setup/create-db.sql`: it creates a `zulip` database with `C.UTF-8` collation and a `zulip` user with full rights. If you cannot run it as is, perform the equivalent actions. Depending on the provider you may need a password or client certificate for the user.

In `/etc/zulip/settings.py` set `REMOTE_POSTGRES_HOST`, `REMOTE_POSTGRES_PORT` and `REMOTE_POSTGRES_SSLMODE`. Put `postgres_password` in `/etc/zulip/zulip-secrets.conf` if you use passwords.

Finally, as the `zulip` user run `scripts/setup/initialize-database` and `manage.py generate_realm_creation_link` from the current deployment directory.

## Checked

Confirmed against the Cloud-provider-managed PostgreSQL section of the PostgreSQL page: the full-text search trade-off, default names, the install command and puppet classes, create-db.sql contents, the REMOTE_POSTGRES settings, postgres_password and the final commands. Nothing removed.

Method: docs-checked 2026-11-09 against docs/production/postgresql.md in the zulip/zulip repository (main), the source of the cited page.
