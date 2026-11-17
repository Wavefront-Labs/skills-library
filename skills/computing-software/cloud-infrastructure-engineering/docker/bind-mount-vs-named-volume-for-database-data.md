---
id: computing-software.cloud-infrastructure-engineering.docker.bind-mount-vs-named-volume-for-database-data
name: bind-mount-vs-named-volume-for-database-data
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, db-bind-mount, named-volume, database-storage, pgdata, lost-found, volume-driver-opts, selinux-z, data-persistence]
level: practitioner
status: docs-checked
description: "Choose bind mount or named volume for database data: ownership and initdb errors, lost+found, Desktop performance, SELinux labels, backups, and named volumes pinned to a host path."
sources: ["https://docs.docker.com/engine/storage/volumes/", "https://docs.docker.com/engine/storage/bind-mounts/", "https://hub.docker.com/_/postgres", "https://docs.docker.com/reference/cli/docker/volume/create/#driver-specific-options", "https://docs.docker.com/reference/compose-file/services/#volumes"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bind mount vs named volume for database data

## Decision table
| Factor | Named volume | Bind mount |
|---|---|---|
| Who manages it | Docker (`docker volume create/rm/prune`), stored under `/var/lib/docker/volumes` on Linux | You: any host path |
| Backups and portability | Docker docs recommend volumes as the preferred mechanism for persisting data | Tied to the host directory layout |
| Missing source path | A missing named volume is created empty | `-v` creates a missing host directory automatically; `--mount` errors |
| Accidental deletion risk | `docker compose down -v`, `docker volume prune --all` | host `rm -rf`, cleanup scripts |
| Compose file portability | high | path must exist on each host |
| Existing content at the container path | copied into an empty volume | obscured by the mount |

Default: **named volume**. Use a bind mount on Linux servers when the data must sit on a
specific disk or dataset and host-level tooling owns it.

## Bind mount pitfalls and fixes
- **Ownership**: the host directory must be owned by the user the database process runs as. The
  postgres image documents that the server does not care which UID it runs as as long as the
  owner of `PGDATA` matches (and `initdb` needs the user to exist in `/etc/passwd`).
- **PGDATA path (postgres image)**: for PostgreSQL 17 and below, mount the data volume at
  `/var/lib/postgresql/data`, not `/var/lib/postgresql`; otherwise the image's declared volume
  creates an anonymous volume and data is lost when the container is re-created. From PostgreSQL 18
  the image's `PGDATA` is version specific (`/var/lib/postgresql/18/docker`) and the declared
  volume is `/var/lib/postgresql`, so mount there. Check the image page for your version.
- **SELinux** (RHEL/Fedora): add `z` (shared) or `Z` (private) to the bind option
  (`-v /srv/pg:/var/lib/postgresql/data:Z`). This relabels the host directory itself; bind-mounting a
  system directory such as `/home` or `/usr` with `Z` can render the host inoperable. Labels cannot be
  set with `--mount`.
- Short-syntax binds create a missing host path automatically, so a typo silently starts a fresh empty
  database. In Compose, use long syntax with `create_host_path: false`.

## Best of both: named volume on a chosen path
```yaml
volumes:
  pgdata:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: /srv/pg          # must already exist
```
Docker manages it as a named volume (`docker volume ls`) while the bytes live at the path you chose.

## Never
- Anonymous volumes for data (for example the image's declared `VOLUME` with nothing mounted
  there): unnamed, not reused across container re-creations.
- Sharing one data directory between two database containers at once.
- Copying a live data directory as the backup; use the database's dump tool, stop the database, or
  take a consistent filesystem snapshot (see `volume-backup-restore-and-migration`).

## Verify
```bash
docker inspect -f '{{range .Mounts}}{{.Type}} {{.Source}} -> {{.Destination}}{{"\n"}}{{end}}' $(docker compose ps -q db)
docker compose down && docker compose up -d && docker compose exec db psql -U app -c '\l'   # data survived
```

## Checked

Date: 2026-10-24. Documentation release: Docker Engine storage docs, Compose file reference and the Docker Official Image page for postgres (docker/docs, docker-library/docs main).
Confirmed: `-v` auto-creating a missing host directory versus `--mount` erroring, Compose `create_host_path`, SELinux `z`/`Z`
semantics and the system-directory warning, the postgres image PGDATA and VOLUME path change in PostgreSQL 18 and the
anonymous-volume behaviour for 17 and below, and the arbitrary `--user` note. Removed: Docker Desktop performance
and permission claims, fixed UID numbers, the lost+found and entrypoint chown claims, and statements about volume
removal that no checked page covers.

Method: documentation only; no commands were run.
