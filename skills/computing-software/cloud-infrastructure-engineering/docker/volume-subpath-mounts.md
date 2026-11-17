---
id: computing-software.cloud-infrastructure-engineering.docker.volume-subpath-mounts
name: volume-subpath-mounts
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, volumes, volume-subpath, mount-flag, compose-volumes, multi-tenant, named-volume]
level: practitioner
status: docs-checked
description: "Mount only a subdirectory of a named volume with --mount volume-subpath (Engine 26+) and Compose volume.subpath: setup, prerequisites, and use cases like shared config volumes."
sources: ["https://docs.docker.com/engine/storage/volumes/#mount-a-volume-subdirectory", "https://docs.docker.com/reference/compose-file/services/#volumes"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Volume subpath mounts

Mount one directory of a volume instead of the whole thing: one volume, many tenants or
services, each seeing only its own slice.

## CLI (Engine 26.0+)
```bash
docker volume create shared
# create the subdirectories first: the subpath must exist
docker run --rm -v shared:/v alpine mkdir -p /v/app1 /v/app2

docker run -d --name app1 \
  --mount type=volume,src=shared,dst=/data,volume-subpath=app1 app:1.0
docker run -d --name app2 \
  --mount type=volume,src=shared,dst=/data,volume-subpath=app2,readonly app:1.0
```
Only the long `--mount` syntax supports it; `-v` has no subpath form.

## Compose
```yaml
services:
  app1:
    image: app:1.0
    volumes:
      - type: volume
        source: shared
        target: /data
        volume:
          subpath: app1
volumes:
  shared:
```

## Uses
- One volume (for example an NFS-backed `local` volume) split across services, avoiding one
  volume definition per service.
- Shared config volume where each service gets its own folder read-only.
- Separate data from logs inside one backed-up volume.

## Gotchas
- The subdirectory must exist in the volume before it is mounted; if it does not, the mount
  fails. Create it first.
- Isolation is by path only: a container with the full volume mounted elsewhere can read every
  subpath. Do not use it as a security boundary between untrusted tenants.

## Verify
```bash
docker inspect -f '{{json .Mounts}}' app1
docker exec app1 ls /data       # only app1's files
```

## Checked

Date: 2026-10-24. Documentation release: Docker Engine 26.0 release notes, Engine storage docs and Compose file reference (docker/docs main).
Confirmed: `volume-subpath` on `--mount` (added in Engine 26.0, per the 26.0 release notes), the subdirectory must
exist before mounting or the mount fails, `readonly`/`ro` mount options, and Compose long syntax `volume.subpath`
("Path inside a volume to mount instead of the volume root"). Removed: the driver-support claim, the pre-population
claim, the specific error text and the `jq` pipe, which no page covers.

Method: documentation only; no commands were run.
