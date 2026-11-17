---
id: computing-software.systems-network-administration.immich.backup-ordering
name: backup-ordering
category: computing-software
field: systems-network-administration
product: immich
tags: [3-2-1, consistency, restore-order, database, filesystem]
level: practitioner
status: docs-checked
description: "Keep Immich database and file backups consistent: stop the server during the backup, or back up the database first and the filesystem second."
sources:
  - https://docs.immich.app/administration/backup-and-restore
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: avoid broken assets after a restore caused by database and files drifting apart.

An Immich backup has two halves that must belong together: the database dump and the asset files. The docs recommend a 3-2-1 backup strategy and point out that Immich only prepares data; you still need a backup tool.

Method A, safest: stop the `immich-server` container while backing up. With nothing changing, the database and the files always agree.

```bash
docker compose stop immich-server
# run database dump and filesystem backup here
docker compose start immich-server
```

Method B, when stopping is not possible: back up the database first, then the filesystem. The worst case is that files exist on disk which the database does not know about. If necessary these can be (re)uploaded manually after a restore, which is far less harmful than database rows pointing at files that your backup does not contain.

The reverse order risks the opposite: database entries for assets that never made it into the file backup, which become broken assets after restore.

Pair this with the folder list from the filesystem layout skill.

The built-in automatic dump in `UPLOAD_LOCATION/backups` is covered by the filesystem backup if you include that folder.

## Checked

2026-11-03. Confirmed against the Immich docs (https://docs.immich.app/) by reading: administration/backup-and-restore (Backup ordering, Filesystem, Automatic Database Backups).
Removed or reworded: the expansion of 3-2-1; the claim that stray files appear in an integrity report; the `.immich` marker claim.
Method: documentation only; no commands were run.
