---
id: computing-software.cloud-infrastructure-engineering.harbor.installer-rollback
name: installer-rollback
category: computing-software
field: cloud-infrastructure-engineering
product: harbor
tags: [rollback, upgrade-rollback, backup-restore, internal-tls, harbor-database]
level: practitioner
status: docs-checked
description: "Roll back an installer-based Harbor upgrade from your backups, and regenerate internal TLS certificates when required."
sources:
  - https://goharbor.io/docs/main/administration/upgrade/roll-back-upgrade/
  - https://goharbor.io/docs/main/administration/upgrade/helm-upgrade/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
You can roll back only if you backed up the previous Harbor directory and database before upgrading. Harbor supports restoring the pre-upgrade state, not downgrades.

Procedure:
1. Stop and remove the current service: `cd harbor` then `docker compose down`.
2. Remove the current instance: `rm -rf harbor`.
3. Restore the older version: `mv /my_backup_dir/harbor harbor`.
4. Restore the database by copying the data files from the backup directory back to your data volume, by default `/data/database`.
5. Restart with the previous configuration. If that version was installed from a release build: `cd harbor` then `./install.sh`.

Internal TLS gotcha: Harbor 2.2 is compiled with Go 1.15, which deprecated self-signed certificates without a SAN. If you enabled internal TLS and the prepare script generated the certificates, you must generate the internal certificates again with `docker run -v /:/hostfs goharbor/prepare:v2.2.0 gencert -p /path/to/internal/tls/cert`. Certificates made by older prepare scripts lack the SAN extension; if you manage the certificates yourself, make sure they include it.

For Helm deployments, `helm rollback` is not supported, because the database schema cannot be downgraded automatically (see the Helm upgrade page).

## Checked

2026-11-03. Rollback steps, the Go 1.15 and SAN note, the `gencert` command and the no-downgrade statement were read against the Harbor docs page Roll Back from an Upgrade; the Helm statement against Upgrading Harbor Deployed with Helm. Removed: the advice to restore the database backup and redeploy the older chart for Helm (not on either page); changed "rejects" to the page's "deprecated".

Method: documentation only; no commands were run.
