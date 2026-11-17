---
id: computing-software.cloud-infrastructure-engineering.docker.volume-backup-restore-and-migration
name: volume-backup-restore-and-migration
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, volume-backup, volume-restore, volume-migration, volumes, tar, volumes-from, backup-container, offen-docker-volume-backup, restic, consistent-backup, move-volume]
level: practitioner
status: docs-checked
description: "Backing up, restoring and moving named volumes with a throwaway tar container, getting a consistent snapshot of a live database volume, and migrating volumes between hosts or to a new volume name."
sources: ["https://docs.docker.com/engine/storage/volumes/#back-up-restore-or-migrate-data-volumes", "https://docs.docker.com/reference/cli/docker/volume/", "https://www.postgresql.org/docs/current/backup-dump.html", "https://www.postgresql.org/docs/current/backup-file.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Volume backup, restore and migration

**Goal:** a named volume can be restored to the byte on another host, and a running
database's volume is backed up without a torn copy.

## The pattern: a throwaway container that mounts the volume and a host dir
```bash
# backup  (volume "pgdata" -> ./backup/pgdata.tar.gz)
docker run --rm -v pgdata:/data:ro -v "$PWD/backup":/backup alpine \
  tar czf /backup/pgdata.tar.gz -C /data .

# restore (into a fresh or existing volume)
docker volume create pgdata
docker run --rm -v pgdata:/data -v "$PWD/backup":/backup alpine \
  sh -c 'cd /data && tar xzf /backup/pgdata.tar.gz'
```
- `-C /data .` keeps paths relative so the archive restores into any mount point.
- Check ownership and modes after a restore; the files must remain readable by the user the
  database container runs as.
- `--volumes-from <container>` is the form shown in the Docker docs: `docker run --rm
  --volumes-from dbstore -v $(pwd):/backup ubuntu tar cvf /backup/backup.tar /dbdata` backs up
  the container's volume, and the restore example un-tars into a new container's volume with
  `docker run --rm --volumes-from dbstore2 -v $(pwd):/backup ubuntu bash -c "cd /dbdata && tar
  xvf /backup/backup.tar --strip 1"`. It mounts the volumes of that container at their
  original paths; naming the volume is clearer.

## Never tar a live database
A file-level copy of a running database's data directory is not a safe backup unless the
database is stopped or the copy is a consistent snapshot. For PostgreSQL, the documentation says
the server must be shut down to get a usable file-system-level backup of the data directory
(filesystem snapshots are the documented alternative). Options:
1. **Logical dump** with the database's own tool, for example
   `docker exec db pg_dumpall -U postgres | gzip > all.sql.gz`; `pg_dumpall` emits SQL commands
   that you restore with `psql`. For other databases use that database's dump tool.
2. **Stop, tar, start**: `docker stop db && <tar backup> && docker start db`. Brief downtime and
   an exact copy of the data directory.
3. **Filesystem snapshot** of the storage under the volume, following your database's backup
   documentation (PostgreSQL documents `pg_backup_start` for backups taken while the server runs).

Backup tools that automate these patterns exist; check each tool's own documentation.

## Migrate between hosts
```bash
docker run --rm -v pgdata:/data:ro alpine tar czf - -C /data . \
  | ssh newhost 'docker volume create pgdata >/dev/null && docker run --rm -i -v pgdata:/data alpine tar xzf - -C /data'
```
Streams without a temp file. For many volumes, loop over `docker volume ls -q` with a filter.
Restore each volume under the **same** name on the new host so the Compose file or service
definition finds it instead of creating an empty one.

## Rename / copy a volume on the same host
Docker has no `volume rename`:
```bash
docker volume create newname
docker run --rm -v oldname:/from:ro -v newname:/to alpine sh -c 'cd /from && cp -a . /to'
```
`cp -a` preserves ownership, modes and symlinks (archive mode).

## Clone the volume's driver options too
`docker volume inspect pgdata` shows `Driver`, `Options` (e.g. an NFS `device=`) and
`Labels`. A plain tar restore into a volume with a different driver/options is a migration of
data only; recreate the volume with the same `-o` flags first if it was NFS/cloud-backed.

## Verify
```bash
docker run --rm -v pgdata:/data:ro alpine sh -c 'find /data | wc -l; du -sh /data'   # before
docker run --rm -v pgdata-restored:/data:ro alpine sh -c 'find /data | wc -l; du -sh /data'  # after: same counts
docker run --rm -v pgdata:/a:ro -v pgdata-restored:/b:ro alpine diff -rq /a /b && echo identical
```

## Checked

Date: 2026-10-24. Documentation release: Docker Engine volumes page (backup, restore, migrate section) and PostgreSQL backup documentation (docker/docs main, PostgreSQL current docs).
Confirmed: the `--volumes-from` backup and restore pattern with `tar cvf`/`tar xvf --strip 1`, read-only volume mounts,
that PostgreSQL file-system-level backups need the server shut down or a consistent snapshot, `pg_dumpall` emitting
SQL restored with `psql`, and `pg_backup_start` for running-server backups. Removed: UID values for images, tool-specific
claims for third-party backup tools, MySQL and MongoDB dump commands, Windows path workarounds, Compose
label and naming claims, and the version-compatibility trap, none of which a checked page states.

Method: documentation only; no commands were run.
