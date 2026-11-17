---
id: computing-software.cloud-infrastructure-engineering.docker.extracting-files-from-images-and-containers
name: extracting-files-from-images-and-containers
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, docker-cp, extract-files-image, docker-create-cp, crane-export, debugging, distroless]
level: practitioner
status: docs-checked
description: "Get files out of images and stopped or shell-less containers: docker create + cp, cp from exited containers, streaming tar, crane export and build --output."
sources: ["https://docs.docker.com/reference/cli/docker/container/cp/", "https://docs.docker.com/reference/cli/docker/container/export/", "https://docs.docker.com/reference/cli/docker/container/create/", "https://github.com/google/go-containerregistry/blob/main/cmd/crane/doc/crane_export.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Extracting files from images and containers

`docker cp` works on stopped containers and needs no shell or tools inside, which makes it
the main way to inspect distroless images and crashed containers.

## From an image (never run it)
```bash
id=$(docker create nginx:1.27)                     # creates, does not start
docker cp "$id":/etc/nginx/nginx.conf ./nginx.conf
docker cp "$id":/etc/nginx -                       # stream a directory as a tar archive to stdout
docker rm "$id"
```
`docker create` creates the container without starting it, so nothing from the image runs.
`docker create --platform` selects a platform variant.

## From a stopped or crashed container
```bash
docker ps -a --filter status=exited
docker cp crashed-app:/app/logs ./crash-logs        # files written before the crash
docker cp crashed-app:/tmp/heapdump.hprof .
docker diff crashed-app                              # what it changed versus the image
```

## Copy in (fix and retry without rebuilding)
```bash
docker cp ./fixed.conf web:/etc/nginx/conf.d/default.conf && docker restart web
```

## Whole filesystem
```bash
docker export crashed-app > rootfs.tar               # the container's filesystem as a tar archive
crane export nginx:1.27 rootfs.tar                    # straight from the registry (crane export IMAGE TARBALL, - for stdout)
```

## From a build stage
```bash
docker build --target build -o type=local,dest=./out .   # stage filesystem to disk
```

## Gotchas
- Symlinks: if `SRC_PATH` is a local symbolic link, the link itself is copied by default; use
  `-L` to copy the target.
- Ownership: files copied into a container are created with the root user's UID:GID, and files
  copied to the host get the invoking user's UID:GID; `-a` sets ownership to the user and
  primary group at the source.
- `docker cp` does not create missing parent directories for `DEST_PATH`.
- `docker export` does not include the contents of volumes attached to the container.
- A container started with `--rm` is deleted when it exits, so run crash investigations
  without `--rm`.

## Checked

2026-10-26 against Docker docs (docker/docs main, 2026-10-23), docker/cli system events reference, Compose and Scout CLI reference data, dive, uv and distroless READMEs, action repositories at their latest releases. Confirmed in the docker cp, docker export and docker create references and crane export docs: docker cp works on running or stopped containers, streaming with -, ownership rules and -a, -L and symlink behaviour, no parent directory creation, docker export excluding volume contents, docker diff, docker create --platform, crane export usage. Removed the unconfirmed claim that appending /. follows symlinks, the claim about volumes in docker cp, and the tar/grep pipelines.

Method: documentation only; no commands were run.
