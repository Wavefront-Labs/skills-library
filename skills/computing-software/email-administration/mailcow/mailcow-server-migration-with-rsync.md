---
id: computing-software.email-administration.mailcow.mailcow-server-migration-with-rsync
name: mailcow-server-migration-with-rsync
category: computing-software
field: email-administration
product: mailcow
tags: [migration, rsync, docker-volumes, rspamd-hyperscan, new-server, snat-to-source]
level: advanced
status: docs-checked
description: "Move a mailcow server to a new host by rsyncing the install directory and Docker volumes, with the special case of a different CPU architecture."
sources: ["https://docs.mailcow.email/maintenance/migration/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Migrating mailcow to a new server

The documented method assumes an empty target server and erases everything under `/var/lib/docker/volumes` there. An alternative is `./helper-scripts/backup_and_restore.sh` on the source, then a normal install on the target, copying `mailcow.conf` and restoring.

Procedure:
1. Install Docker and Compose on the target.
2. Stop Docker on the target (`systemctl stop docker.service`).
3. From the source, run `rsync -aHhP --numeric-ids --delete` for `/opt/mailcow-dockerized/` and for `/var/lib/docker/volumes/` to the target. Keep the trailing slashes on the source paths.
4. Run `docker compose down` and stop Docker on the source.
5. Repeat the rsync; it now only transfers differences.
6. Start Docker on the target, `docker compose pull`, then `docker compose up -d`.
7. Change DNS to the new server.

When migrating between architectures, add `--exclude '*rspamd-vol-1'` to the volumes rsync. That volume holds hyperscan cache files that are incompatible across platforms and make Rspamd fail to start; they are regenerated if missing.

If the public IP changed, check `SNAT_TO_SOURCE` in `mailcow.conf`, otherwise SOGo may not work.

## Checked

2026-11-09. Confirmed against the mailcow Migration page: erase warning, backup_and_restore.sh alternative, rsync flags and trailing slashes, repeat rsync after shutdown, pull and up, the rspamd-vol-1 exclusion for other architectures, DNS and SNAT_TO_SOURCE. Nothing removed.

Method: docs-checked 2026-11-09 against docs.mailcow.email/maintenance/migration/ (whole page).
