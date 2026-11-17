---
id: computing-software.devops-ci-cd.gitea.upgrade-gitea
name: upgrade-gitea
category: computing-software
field: devops-ci-cd
product: gitea
tags: [gitea-upgrade-path, gitea, downgrade-backup, deprecated-config, database-migration, customized-templates]
level: practitioner
status: docs-checked
description: "Upgrade Gitea safely: changelog and deprecation checks, patch-version downgrade rules, backup list, binary/Docker/package upgrade steps, template drift."
sources: ["https://gitea.com/gitea/docs/src/branch/main/docs/installation/upgrade-from-gitea.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Upgrading Gitea

1. **Read the changelog** (Gitea blog) for breaking changes in the target release.
2. **Clear deprecations**: warnings about changed config options show at the top of the Site Administration panel for at least a release cycle; unresolved ones may stop Gitea starting in the following version.
3. **Know the downgrade rule**: patch versions sharing the first two fields (`1.4.0` to `1.4.1`) share the DB structure and are interchangeable. `1.4.1` to `1.4.0` is "take your own risk". `1.4.x` to `1.5.y` upgrades the DB directly (you may jump to the latest `1.5.y`) but `1.5.y` back to `1.4.x` is not possible without restoring a backup.
4. **Back up first** (even for patch upgrades in production): stop Gitea; back up the database, the config, the data files in `APP_DATA_PATH`, and external storage such as S3/MinIO. Snapshots of the data volume and object storage are an alternative.
5. **Swap and start**. On every start Gitea checks the schema and runs migrations itself; on big databases the first launch is slow and the app unavailable.

Per install method:
- Docker: `docker pull` the release, stop, back up, start the new container (or compose pull/up).
- Package: stop, back up, upgrade through the package manager, start.
- Binary: download to a temp dir, stop, back up, replace the binary, start. `contrib/upgrade.sh` in the source tree automates this on Linux.

## Customised templates
Template structure and variables change between releases. Mismatched custom templates cause 50x errors, missing components or broken layout; update or remove them to recover.

## Checked
2026-11-03. Commands, flags, settings, numbers and behaviour were compared line by line with the Gitea docs source page named in `sources` (read in full from the docs repository raw file). Nothing else removed; no unconfirmed claim remained.
Method: documentation only; no commands were run.
