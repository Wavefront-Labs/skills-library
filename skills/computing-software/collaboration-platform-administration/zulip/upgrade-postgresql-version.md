---
id: computing-software.collaboration-platform-administration.zulip.upgrade-postgresql-version
name: upgrade-postgresql-version
category: computing-software
field: collaboration-platform-administration
product: zulip
tags: [upgrade-postgresql, postgresql-major-version, manage-backup]
level: advanced
status: docs-checked
description: "Upgrade the PostgreSQL major version on a Zulip server with upgrade-postgresql: update Zulip first, stop-server, manage.py backup, run as root, start-server."
sources: ["https://zulip.readthedocs.io/en/latest/production/upgrade.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Upgrading PostgreSQL on a Zulip server

The PostgreSQL major version is upgraded separately from Zulip, and is not tied to the host OS: the installer uses the latest PostgreSQL available at install time. Each Zulip major version supports a documented range of PostgreSQL versions. Docker deployments upgrade PostgreSQL through image bumps instead of this script.

Procedure:

1. Upgrade Zulip at least to the latest maintenance release of your major version (say 9.1 to 9.4) so you have the most robust upgrade tool.
2. As the `zulip` user, stop the server:

```
~zulip/deployments/current/scripts/stop-server
```

3. Take a backup:

```
~zulip/deployments/current/manage.py backup --output=OUTPUT_DIR/postgresql-upgrade.backup.tar.gz
```

4. As root, run the database upgrade tool:

```
~zulip/deployments/current/scripts/setup/upgrade-postgresql
```

5. As the `zulip` user, start the server:

```
~zulip/deployments/current/scripts/start-server
```

Then open the Zulip URL and confirm everything works.

The tool also appears as a step inside operating system upgrades.

## Checked

2026-11-03: commands, paths, flags, settings and figures read against the Zulip documentation page production/upgrade.html (zulip.readthedocs.io, latest). Removed: the unsupported advice about backup size and never editing the [postgresql] version value; replaced the unexpanded tilde in the --output path with a placeholder.

Method: documentation only; no commands were run.
