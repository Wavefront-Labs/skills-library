---
id: computing-software.cloud-infrastructure-engineering.docker.pre-populating-volumes-from-image-content-and-nocopy
name: pre-populating-volumes-from-image-content-and-nocopy
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, volume-prepopulate, volume-nocopy, named-volume, volume-seeding, anonymous-volume, renew-anon-volumes, node-modules-volume, volume-ownership]
level: practitioner
status: docs-checked
description: "Control how Docker seeds an empty volume from the image's directory: when copying happens, ownership inheritance, nocopy, stale node_modules volumes, and seeding volumes explicitly."
sources: ["https://docs.docker.com/engine/storage/volumes/", "https://docs.docker.com/reference/compose-file/services/#volumes", "https://docs.docker.com/reference/cli/docker/compose/up/", "https://docs.docker.com/engine/storage/bind-mounts/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pre-populating volumes from image content (and nocopy)

## The rule
When an **empty volume** is mounted onto a directory that has files in the container, those
files are copied into the volume. If the volume is not empty, nothing is copied and the
volume's content is used instead. If you mount a volume name that does not exist, an empty
volume is created, which is a good way to pre-populate data another container needs.
- Applies to volumes (named or anonymous).
- Bind mounts do not copy: they obscure whatever was at the container path.
- Copying happens only while the volume is empty, so image updates do not flow into a volume
  that already has data; that is the source of "I rebuilt the image but the container still has
  old files".

## Using it on purpose
Ship default config or seed data in the image at the mount path; the first `up` seeds the
empty volume. Check ownership and permissions of the seeded files in your own environment
before relying on them for a non-root user.

## Turning it off: nocopy
```bash
docker run -v data:/app/data:volume-nocopy myimage
docker run --mount type=volume,src=data,dst=/app/data,volume-nocopy myimage
```
```yaml
services:
  app:
    volumes:
      - type: volume
        source: data
        target: /app/data
        volume: { nocopy: true }
```
Use it when the image's files at that path are placeholders you must not mix with real data,
or when copying a large directory slows every fresh environment.

## The node_modules trap
```yaml
volumes:
  - .:/app
  - /app/node_modules        # anonymous volume seeded from the image's node_modules
```
After adding a dependency and rebuilding, the anonymous volume still holds the old modules.
`docker compose up --build --renew-anon-volumes` (`-V`) recreates it; for named volumes,
`docker volume rm` it.

## Seeding a volume explicitly (no image change)
```bash
docker volume create data
docker run --rm -v data:/data -v "$PWD/seed":/seed:ro alpine cp -a /seed/. /data/
```

## Gotchas
- Seeding is per volume, not per container: mounting an already non-empty volume gets no copy.
- Compose long syntax uses `volume: { nocopy: true }`.

## Verify
```bash
docker volume rm -f seedtest && docker run --rm -v seedtest:/usr/share/nginx/html nginx ls /usr/share/nginx/html   # index.html copied
docker volume rm -f seedtest && docker run --rm -v seedtest:/usr/share/nginx/html:volume-nocopy nginx ls /usr/share/nginx/html   # empty
```

## Checked

Date: 2026-10-24. Documentation release: Docker Engine storage docs, Compose file reference and `docker compose up` reference (docker/docs and docker/compose main).
Confirmed: empty-volume copy-up and non-empty volume behaviour, `volume-nocopy` for `-v` and `--mount`, Compose
`volume.nocopy`, bind mounts obscuring existing files, and `docker compose up --renew-anon-volumes` (`-V`) recreating
anonymous volumes. Corrected: the `-v` option is documented as `volume-nocopy`. Removed: the ownership and permission
inheritance claims, the non-root volume recipe built on them, the `docker cp` seeding variant, the other-driver and
Kubernetes statements, none of which the documentation states.

Method: documentation only; no commands were run.
