---
id: computing-software.networking-hardware-and-wireless.check-point.backup-snapshot-and-migrate-export
name: backup-snapshot-and-migrate-export
category: computing-software
field: networking-hardware-and-wireless
product: check-point
tags: [networking-hardware-and-wireless, check-point, backup, snapshot, migrate-export]
level: practitioner
status: draft
description: "Take backups with Gaia backup, full snapshots and migrate_server export before changes, and restore."
sources:
  - https://sc1.checkpoint.com/documents/R81.20/WebAdminGuides/EN/CP_R81.20_Installation_and_Upgrade_Guide/Default.htm
  - https://sc1.checkpoint.com/documents/R81.20/WebAdminGuides/EN/CP_R81.20_Gaia_AdminGuide/Default.htm
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Gaia backup, snapshot and migrate_server

```
clish -c "add backup local"                        # config only, /var/log/CPbackup/backups/
clish -c "add snapshot gw1_pre_upgrade desc 'before R81.20 JHF'"
clish -c "show snapshots"
clish -c "set snapshot revert gw1_pre_upgrade"
cd $FWDIR/scripts ; ./migrate_server export -v R81.20 /var/tmp/mgmt_export.tgz
./migrate_server import -v R81.20 /var/tmp/mgmt_export.tgz
```
- `backup`: Gaia OS configuration (a few MB), not product databases on a management server. `snapshot`: whole OS image, large, needs about the used space of the root volume free in `/var` and temporarily blocks traffic on a busy gateway.
- `migrate_server` (the Upgrade Tools) exports the management database and configuration for moving to a new server or upgrading by clean install; check the Release Notes for the supported source versions (confirm).
- Always copy backups off-box (`scp`) and keep a hash. Snapshots on the same disk do not protect against disk failure.
- On management servers a `mgmt_cli`-visible alternative is `migrate export` (newer versions). R81.20 also has `backup` extended with a management database (confirm on your version).
- Gotcha: a snapshot taken while on a hotfix includes it; reverting to a snapshot from another JHF level changes the version, so note the build.

Verify: `show snapshots` lists status and size; test restore of the export on a lab VM before relying on it; after revert, `cpstat fw` and `cphaprob stat` for sanity.
