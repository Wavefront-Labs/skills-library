---
id: computing-software.cloud-infrastructure-engineering.portainer.upgrade-and-roll-back-portainer
name: upgrade-and-roll-back-portainer
category: computing-software
field: cloud-infrastructure-engineering
product: portainer
tags: [upgrade, rollback, portainer-db, schema, backups]
level: advanced
status: docs-checked
description: "Roll back a Portainer upgrade from a backup or from the automatic portainer.db.bak made during the update."
sources:
  - https://github.com/portainer/portainer-docs/blob/HEAD/2.39-lts/faqs/upgrading/how-can-i-roll-back-to-a-previous-version-of-portainer.md
  - https://github.com/portainer/portainer-docs/blob/HEAD/2.39-lts/faqs/upgrading/how-do-i-upgrade-portainer-to-the-latest-version.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
New Portainer versions generally bump the database schema version, so a newer database cannot run on an older Portainer. Plan rollback before you upgrade: take a manual backup first, then to roll back, wipe the installation and restore the backup during reinstall.

If you took no backup, use the automatic backup made during the update: a copy of `portainer.db` only, stored in the `portainer_data` volume under `backups/portainer.db.bak`. Procedure:

1. Stop and remove the Portainer container, but do not delete the `portainer_data` volume.
2. Rename the existing `portainer.db` in the base of the data directory to something like `portainer.db.oldversion`.
3. Copy `backups/portainer.db.bak` to `portainer.db` in the base of the data directory.
4. Start Portainer using the image version you were previously on, which must match the version of the backed-up database.

The upgrade procedure itself differs by environment and platform; see Upgrading Portainer in the docs.

## Checked

2026-11-04. Checked against the Portainer 2.39 LTS documentation pages in `sources` (portainer-docs on GitHub, fetched this batch): commands, flags, ports, paths, defaults and UI steps. Removed the unconfirmed list of platforms covered by the upgrade docs.

Method: documentation only; no commands were run.
