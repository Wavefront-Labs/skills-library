---
id: computing-software.cloud-infrastructure-engineering.docker.volume-create-inspect-and-ls-filters
name: volume-create-inspect-and-ls-filters
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, volumes, volume-create, volume-inspect, volume-ls, labels, volume-driver]
level: practitioner
status: docs-checked
description: "Manage volumes from the CLI: volume create with driver, -o options and labels, inspect mountpoint and options, ls filters (dangling, driver, label, name) and formatted output."
sources: ["https://docs.docker.com/reference/cli/docker/volume/create/", "https://docs.docker.com/reference/cli/docker/volume/inspect/", "https://docs.docker.com/reference/cli/docker/volume/ls/", "https://docs.docker.com/engine/storage/volumes/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# volume create, inspect and ls

## Create
```bash
docker volume create pgdata
docker volume create --label app=shop --label backup=daily pgdata
docker volume create --driver local \
  --opt type=nfs --opt o=addr=10.0.0.10,rw,nfsvers=4 --opt device=:/exports/shop \
  shop-nfs
docker volume create --driver local --opt type=tmpfs --opt device=tmpfs --opt o=size=256m scratch
```
Driver options are passed with `--opt` (`-o`). Test a driver-backed volume right after creating
it: `docker run --rm -v shop-nfs:/v alpine ls /v`.

## Inspect
```bash
docker volume inspect pgdata
docker volume inspect -f '{{.Mountpoint}}' pgdata          # the volume's mount point on the host
docker volume inspect -f '{{json .Options}} {{json .Labels}}' shop-nfs
docker system df -v                                         # per-volume size and links
```

## List and filter
```bash
docker volume ls --filter dangling=true          # not used by any container
docker volume ls --filter driver=local
docker volume ls --filter label=backup=daily
docker volume ls --filter name=pg                # matches all or part of the name
docker volume ls --format '{{.Name}}\t{{.Driver}}\t{{.Labels}}'
docker volume ls -q --filter label=backup=daily  # names only
```

## Labels as a control plane
Label volumes at creation with ownership and policy (`owner=team-x`, `backup=daily`,
`retention=30d`) and drive backup and prune scripts by label rather than name patterns.
Multiple `--filter label=` options combine as an AND search.

## Gotchas
- Creating a volume with a name already in use on the same driver reuses the existing volume
  without an error; the same name with a different driver is an error.
- `--filter dangling=true` matches volumes not referenced by any container.

## Checked

Date: 2026-10-24. Documentation release: Docker CLI reference and Engine storage docs (docker/cli and docker/docs main).
Confirmed against the volume create, ls and inspect references: `ls` filters (dangling, driver, label, name), multiple
label filters being an AND search, `--format` placeholders (`.Name`, `.Driver`, `.Labels`), reuse of an existing
volume name on the same driver and the error for a different driver, `-o/--opt` driver options and the NFS `device=:/path`
form. Removed: the claim about when options are applied, the immutability statement, Compose auto-label names,
Docker Desktop and rootless storage paths, and the example backup script, none of which the docs state.

Method: documentation only; no commands were run.
