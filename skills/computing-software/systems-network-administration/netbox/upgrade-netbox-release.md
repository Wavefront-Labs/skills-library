---
id: computing-software.systems-network-administration.netbox.upgrade-netbox-release
name: upgrade-netbox-release
category: computing-software
field: systems-network-administration
product: netbox
tags: [upgrade, ltree-extension, version-matrix]
level: advanced
status: docs-checked
description: "Follow the backup, release-notes, dependency and upgrade.sh sequence, including the v4.7 ltree requirement."
sources: ["https://netboxlabs.com/docs/netbox/installation/upgrading/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Upgrading NetBox

Goal: move to a newer release without surprises.

**Rules**

- Back up the current deployment and read every release note since your version.
- You can usually jump straight to any newer release; for a major version increment you must come from the latest minor release of the current major.
- Verify every installed plugin supports the target release.

**Dependencies for 4.7:** Python 3.12 to 3.14, PostgreSQL 15+, Redis 6.0+. NetBox 4.5 and later need Python 3.12 or newer.

**ltree.** v4.7 and later need the PostgreSQL `ltree` extension. Migrations install it automatically if the database user has CREATE; installs following the docs already satisfy this because the user owns the database. Otherwise:
```
GRANT CREATE ON DATABASE netbox TO netbox;
-- or, as a DBA:
CREATE EXTENSION IF NOT EXISTS ltree;
```

**Procedure (archive)**
```
sudo ln -sfn /opt/netbox-$NEWVER/ /opt/netbox
```
Copy `local_requirements.txt`, `configuration.py`, `ldap_config.py`, `media/`, `scripts/`, `reports/` and `gunicorn.py` from the old tree. For Git: `git fetch --tags` then `git checkout vX.Y.Z`. Then run `sudo ./upgrade.sh`.

**Checklist**

1. Backup and release notes.
2. Plugin compatibility.
3. Copy local files.
4. Run upgrade.sh.

## Checked

2026-11-03: confirmed against the cited NetBox documentation: Upgrading page: major-version rule, dependency versions, ltree grant, symlink and git procedure, files to copy, upgrade.sh. Removed: Nothing.

Method: documentation only; no commands were run.
