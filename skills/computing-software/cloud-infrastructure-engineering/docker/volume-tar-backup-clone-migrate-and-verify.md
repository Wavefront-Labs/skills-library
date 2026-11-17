---
id: computing-software.cloud-infrastructure-engineering.docker.volume-tar-backup-clone-migrate-and-verify
name: volume-tar-backup-clone-migrate-and-verify
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, volume-backup, volume-restore, volume-migration, tar-backup-container, volume-clone, volume-rename, rsync-migration, ssh-pipe, restore-test, restore-verification]
level: practitioner
description: "Back up and restore named volumes with a helper container and tar, clone or rename volumes, stream them to another host over ssh, and verify restores."
sources: ["https://docs.docker.com/engine/storage/volumes/#back-up-restore-or-migrate-data-volumes", "https://docs.docker.com/reference/cli/docker/volume/", "https://github.com/compose-spec/compose-spec/blob/main/07-volumes.md"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Volume backup, clone, migration and restore verification

## Backup with a helper container
```sh
docker stop app        # or use an app-consistent dump for databases
docker run --rm -v appdata:/src:ro -v "$PWD":/backup alpine \
  tar -C /src -czf /backup/appdata.tgz .
docker start app
```
Docker's volumes page documents the same idea with `--volumes-from <container>` and a bind
mount for the archive (`tar cvf /backup/backup.tar /dbdata`); mounting the volume by name, as
above, works without needing the original container. Back up databases with their own dump
tools or from a stopped container, since a live copy may be inconsistent.

## Restore
```sh
docker volume create appdata
docker run --rm -v appdata:/dst -v "$PWD":/backup:ro alpine \
  sh -c 'tar -C /dst -xzf /backup/appdata.tgz'
```

## Clone / rename
The `docker volume` subcommands are create, inspect, ls, prune, rm and update; there is no
rename. Copy into a new volume:
```sh
docker volume create appdata-new
docker run --rm -v appdata:/from:ro -v appdata-new:/to alpine sh -c 'cp -a /from/. /to/'
# then point the container/compose file at appdata-new and remove the old one later
```
Compose: a volume can set an explicit `name` (and `external: true` for one that already
exists), so renaming the project does not change which volume is used (compose-spec volumes).

## Cross-host migration
```sh
# stream the archive without a temp file
docker run --rm -v appdata:/src:ro alpine tar -C /src -cf - . \
  | ssh target 'docker volume create appdata >/dev/null && docker run --rm -i -v appdata:/dst alpine tar -C /dst -xf -'
```
This chains the documented tar-in-a-helper-container pattern over ssh; adapt it to your
tooling.

## Verify the restore (do this, not just the backup)
```sh
# compare a file listing of the original and the restored volume
docker run --rm -v appdata:/d:ro alpine ls -lnR /d > before.txt
docker run --rm -v appdata-restored:/d:ro alpine ls -lnR /d > after.txt
diff before.txt after.txt && echo identical
```
Then start the app against the restored volume in an isolated network and run a smoke test
(login, read a known record). Rehearse restores on a schedule and record time-to-restore.

## Verify
`tar -tzvf appdata.tgz` lists the files; the restored app passes its health check.

## Checked
Date: 2026-10-26. Documentation: docker/docs main (last commit 2026-10-23) volumes page (back up, restore, migrate) and `docker volume` CLI reference list; compose-spec volumes (`name`, `external`). Confirmed: helper-container tar backup and restore pattern, absence of `docker volume rename`, Compose volume `name`/`external`. Removed as unconfirmed: tar flag rationale (`--numeric-owner`, `-p`, `--exclude`), the rsync-to-mountpoint migration, sha256 checksum pipeline (replaced by a plain listing comparison), dated archive names.
Method: documentation only; no commands were run.
