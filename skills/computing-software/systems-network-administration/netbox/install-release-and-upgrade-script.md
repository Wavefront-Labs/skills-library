---
id: computing-software.systems-network-administration.netbox.install-release-and-upgrade-script
name: install-release-and-upgrade-script
category: computing-software
field: systems-network-administration
product: netbox
tags: [install-netbox, upgrade-sh, local-requirements]
level: practitioner
status: docs-checked
description: "Lay out /opt/netbox, create the system user and run upgrade.sh."
sources: ["https://netboxlabs.com/docs/netbox/installation/3-netbox/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Install NetBox from archive or Git

Goal: get the application installed and migrated.

**Prerequisites:** Python 3.12 or later (`python3 -V`) and system packages including `python3-venv`, `python3-dev`, `build-essential`, `libpq-dev`.

**Get the code**

- Archive: extract into a version-named directory and symlink it:
```
sudo tar -xzf vX.Y.Z.tar.gz -C /opt
sudo ln -s /opt/netbox-X.Y.Z/ /opt/netbox
```
- Git: clone into `/opt/netbox` and `git checkout vX.Y.Z`; upgrades later are just a checkout of a new tag.

**System user**
```
sudo adduser --system --group netbox
sudo chown --recursive netbox /opt/netbox/netbox/media/
```
The docs also chown `reports/` and `scripts/` so uploads and scripts are writable.

**Optional packages** go in `local_requirements.txt`: `django-storages` for remote file storage, `boto3` (S3) or `dulwich` (Git) for data sources, `sentry-sdk` for Sentry.

**Run** `sudo /opt/netbox/upgrade.sh`. It creates the virtualenv, installs packages, runs migrations (skip with `--readonly`), builds docs and collects static files. If the default Python is too old, set `PYTHON=/usr/bin/python3.12`.

NetBox ships with no accounts, so create a superuser afterwards.

**Checklist**

1. Python 3.12 or later.
2. Optional packages listed.
3. upgrade.sh completed.

## Checked

2026-11-03: confirmed against the cited NetBox documentation: Install page: Python 3.12 or later, archive and Git install steps, system user, local_requirements.txt packages, upgrade.sh behaviour (--readonly, PYTHON variable). Removed: Nothing.

Method: documentation only; no commands were run.
