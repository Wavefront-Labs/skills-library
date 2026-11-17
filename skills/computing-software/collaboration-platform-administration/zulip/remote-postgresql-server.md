---
id: computing-software.collaboration-platform-administration.zulip.remote-postgresql-server
name: remote-postgresql-server
category: computing-software
field: collaboration-platform-administration
product: zulip
tags: [remote-postgresql, standalone-nodb, pg-hba, create-database]
level: advanced
status: docs-checked
description: "Move the Zulip database to a separate Zulip-managed PostgreSQL host with standalone_nodb, create-database, pg_hba.conf, REMOTE_POSTGRES settings and zulip.conf version."
sources: ["https://zulip.readthedocs.io/en/latest/production/postgresql.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Remote PostgreSQL server for Zulip

Use two hosts: one for the database, one for everything else.

1. On the app server, install with the database-less profile:

```
./zulip-server-*/scripts/setup/install --certbot \
    --email=YOUR_EMAIL --hostname=YOUR_HOSTNAME \
    --puppet-classes=zulip::profile::standalone_nodb
```

2. On the database host, unpack the Zulip tarball and install only PostgreSQL, then create the database:

```
./zulip-server-*/scripts/setup/install --puppet-classes=zulip::profile::postgresql
./zulip-server-*/scripts/setup/create-database
```

Edit `/etc/postgresql/*/main/pg_hba.conf` so the `zulip` user can reach the `zulip` database from the app host; the authentication method is your choice.

3. On the app server set these in `/etc/zulip/settings.py`: `REMOTE_POSTGRES_HOST`, `REMOTE_POSTGRES_PORT` (likely 5432) and `REMOTE_POSTGRES_SSLMODE`. For password authentication, put `postgres_password` in `/etc/zulip/zulip-secrets.conf`. Record the remote server's PostgreSQL version in `/etc/zulip/zulip.conf` under `[postgresql]` as `version`.

4. Finish by running, as the `zulip` user, `scripts/setup/initialize-database` and then `manage.py generate_realm_creation_link` from `~zulip/deployments/current`.

For Docker users, the Docker documentation covers external PostgreSQL separately, with Compose and Helm variants.

## Checked

Confirmed against the Remote PostgreSQL database section of the PostgreSQL page: both install commands, create-database, the pg_hba.conf note, the REMOTE_POSTGRES settings, the zulip.conf version and the final commands. Reworded the tarball step and removed the authentication-method advice (the page leaves the method to the reader).

Method: docs-checked 2026-11-09 against docs/production/postgresql.md in the zulip/zulip repository (main), the source of the cited page.
