---
id: computing-software.cloud-infrastructure-engineering.harbor.installer-upgrade-and-migration
name: installer-upgrade-and-migration
category: computing-software
field: cloud-infrastructure-engineering
product: harbor
tags: [upgrade, migrate, harbor-prepare, harbor-yml, docker-compose]
level: advanced
status: docs-checked
description: "Upgrade a Harbor installer deployment with the goharbor/prepare migrate tool, with the backups to take first and database schema behaviour."
sources:
  - https://goharbor.io/docs/main/administration/upgrade/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Always back up before any migration; it can alter the database schema and `harbor.yml`. The guide covers migration from v2.12.0 and later to v2.15.0 only. With an external database on Harbor v2.9 or later, PostgreSQL must be 12 or newer.

Steps:
1. Stop and remove the running instance: `cd harbor` then `docker compose down`.
2. Back up the Harbor files: `mv harbor /my_backup_dir/harbor`.
3. Back up the database, by default in `/data/database`: `cp -r /data/database /my_backup_dir/`.
4. Download and extract the new release package from the GitHub releases page.
5. Get the migration tool, which ships as a docker image: `docker pull goharbor/prepare:[tag]`, where tag is the new version. With the offline installer, load it from the bundled tarball: `docker image load -i harbor/harbor.[version].tar.gz`.
6. Copy the old `harbor.yml` into the new directory and migrate it:
`docker run -it --rm -v /:/hostfs goharbor/prepare:[tag] migrate -i ${path to harbor.yml}`
7. Run `./install.sh` in the new `./harbor` directory (add `--with-trivy` to include Trivy).

The database schema upgrade and data migration are performed by the core service when Harbor starts. If migration fails, read the core log.

Rolling back means restoring the backed-up directory and database; Harbor does not support downgrades.

## Checked

- 2026-11-03: concrete claims (parameter names, defaults, steps, limits, UI labels) read against the official Harbor docs: Upgrade Harbor and Migrate Data, Roll Back from an Upgrade.
Method: documentation only; no commands were run.
