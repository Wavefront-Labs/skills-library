---
id: computing-software.collaboration-platform-administration.zulip.installer-advanced-options
name: installer-advanced-options
category: computing-software
field: collaboration-platform-administration
product: zulip
tags: [installer-options, postgresql-version, no-init-db, puppet-classes]
level: practitioner
status: docs-checked
description: "Use the advanced Zulip installer flags: PostgreSQL version, database name and user, skipping database init, preserving /etc/zulip settings, and puppet classes."
sources: ["https://zulip.readthedocs.io/en/latest/production/deployment.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Advanced Zulip installer options

Besides the standard flags, the installer in `scripts/setup/install` accepts:

- `--postgresql-version`: PostgreSQL 14, 15, 16, 17 or 18 are supported, with 18 the default.
- `--postgresql-database-name=NAME`: replaces the default database name `zulip`. Only effective on the first install.
- `--postgresql-database-user=USER`: replaces the default database user `zulip`. Also first install only.
- `--no-init-db`: skip database initialisation. Use it when a Zulip database already exists, for example when restoring or using a remote server.
- `--no-overwrite-settings`: keep the existing configuration files in `/etc/zulip` instead of regenerating them.
- `--puppet-classes`: choose which Puppet classes to apply, which is how a host becomes only a database, Redis or Smokescreen server. For instance `--puppet-classes zulip::profile::redis` installs just Redis.

What the installer does: it creates the `zulip` user, creates `~zulip/deployments/`, moves the unpacked code tree there at the very end and points the symlink `~zulip/deployments/current` at it, installs dependencies, configures PostgreSQL, RabbitMQ, Memcached and Redis, and initialises the database.

Because later upgrades add sibling directories under `deployments/`, scripts should always call tools through the `current` path. Pick database name, user and version before the first run, since names cannot be changed through the installer afterwards.

## Checked

2026-11-03: commands, paths, flags, settings and figures read against the Zulip documentation page production/deployment.html (zulip.readthedocs.io, latest). Removed: nothing.

Method: documentation only; no commands were run.
