---
id: computing-software.cloud-infrastructure-engineering.docker.compose-volume-long-syntax-tmpfs-and-read-only
name: compose-volume-long-syntax-tmpfs-and-read-only
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, compose, compose-volumes, volume-long-syntax, bind-create-host-path, compose-tmpfs, compose-read-only, read-only-compose-service, read-only]
level: practitioner
description: "Use Compose service volumes long syntax (bind create_host_path, propagation, nocopy, subpath), tmpfs mounts, and read_only root filesystems with the writable paths they need."
sources: ["https://docs.docker.com/reference/compose-file/services/#volumes", "https://docs.docker.com/reference/compose-file/services/#tmpfs", "https://docs.docker.com/reference/compose-file/services/#read_only"]
status: verified
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Compose volumes long syntax, tmpfs and read_only

## Long syntax
```yaml
services:
  app:
    volumes:
      - type: volume
        source: data
        target: /var/lib/app
        volume:
          nocopy: true            # don't seed from image content
          subpath: tenants/a      # mount a subdirectory of the volume (Engine 26+)
      - type: bind
        source: ./config
        target: /etc/app
        read_only: true
        bind:
          create_host_path: false # fail if ./config is missing instead of creating it
          propagation: rslave
          selinux: z
      - type: tmpfs
        target: /tmp
        tmpfs: { size: 67108864, mode: 1777 }   # size in bytes; config prints mode as the integer 1777 (YAML decimal): not verified against the engine, prefer the short form /tmp:size=64m,mode=1777
volumes:
  data: {}
```
- Short syntax `./config:/etc/app:ro` **creates** a missing host path as a root-owned empty
  dir (legacy behaviour; `config` shows `create_host_path: true` on short-syntax binds); long syntax with `create_host_path: false` catches typos (`config` omits the key when it is false). `~/cfg` is expanded to the home directory and `../up` to an absolute path by `config`.
- Relative bind paths resolve against the compose file's directory (or `--project-directory`).
- `nocopy` matters when the image has content at the target that you don't want copied into
  a fresh volume.

## tmpfs
```yaml
    tmpfs:
      - /run
      - /tmp:size=64m,mode=1777
```
tmpfs uses RAM and counts toward the memory limit; always set `size`.

## read_only with writable paths
```yaml
services:
  web:
    image: nginx:1.27
    read_only: true
    tmpfs:
      - /var/cache/nginx:size=32m
      - /var/run:size=1m
      - /tmp:size=16m
    volumes:
      - type: volume
        source: uploads
        target: /srv/uploads
```
Find required writable paths by running once without `read_only` and checking
`docker diff <container>` (A/C entries), then give each a tmpfs or volume.
Common: nginx `/var/cache/nginx`, `/var/run`; Postgres `/var/run/postgresql` + data volume;
Java `/tmp`; Python `__pycache__` (set `PYTHONDONTWRITEBYTECODE=1`).

## Verify
```sh
docker compose config | yq '.services.app.volumes'
docker compose exec web touch /etc/x          # Read-only file system
docker inspect -f '{{.HostConfig.ReadonlyRootfs}} {{json .HostConfig.Tmpfs}}' $(docker compose ps -q web)
```

## Checked
Run on Windows 11 with Docker Compose v2.39.1 (`docker compose config`, no daemon needed): the long-syntax example normalised without errors (volume with `nocopy` and `subpath`, bind with `read_only`, `propagation`, `selinux`, tmpfs with `size` and `mode`), short syntax forms (`./rel:/rel:z`, `~/cfg`, `/abs`, `../up:/up:rw`, named volume), service-level `tmpfs:` list with options, and `read_only: true` with tmpfs paths. Not run (the Docker daemon is not running here): creating networks and volumes, `docker network inspect`, `docker volume ls`, `docker diff`, runtime effects of `read_only`, `internal`, `tmpfs`, `nocopy`, `subpath`, and Linux.
