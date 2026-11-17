---
id: computing-software.cloud-infrastructure-engineering.docker.read-only-root-filesystem-and-immutable-containers
name: read-only-root-filesystem-and-immutable-containers
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, read-only, read-only-rootfs, read-only-tmpfs, writable-paths, docker-diff-writable, writable-path-discovery, immutable-container, no-new-privileges]
level: advanced
description: "Run containers with --read-only plus tmpfs for the few writable paths, discover those paths with docker diff, and apply the immutable-container pattern end to end."
sources: ["https://docs.docker.com/reference/cli/docker/container/run/", "https://docs.docker.com/reference/cli/docker/container/diff/", "https://docs.docker.com/reference/compose-file/services/", "https://docs.docker.com/engine/storage/tmpfs/", "https://github.com/moby/moby/blob/master/api/swagger.yaml"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Read-only root filesystem and immutable containers

## Discover what the app writes
```sh
docker run -d --name probe app:1
# exercise it: requests, background jobs, a restart of the process if possible
docker diff probe
# C /tmp
# A /tmp/upload-1234
# C /var/run
# A /var/run/app.pid
# A /app/.cache/
```
`A` added, `C` changed, `D` deleted. Every A/C path outside volumes must become a tmpfs or a
volume (or the app must stop writing there).

## Run read-only
```sh
docker run -d --read-only \
  --tmpfs /tmp:rw,noexec,nosuid,size=64m \
  --tmpfs /var/run:rw,size=1m \
  -v app-uploads:/srv/uploads \
  --security-opt no-new-privileges --cap-drop ALL --user 10001 \
  app:1
```
Compose:
```yaml
read_only: true
tmpfs: ["/tmp", "/var/run"]
security_opt: ["no-new-privileges:true"]
```
The Compose `tmpfs` attribute documents the options `mode`, `uid` and `gid`; use `docker run --tmpfs ...:size=`
to cap the size. Typical writable needs: `/tmp`, PID files and per-application cache or runtime
directories; `docker diff` shows which for your image.

## The immutable container pattern
1. Everything the app runs is in the image (no installs/downloads at start).
2. Root FS read-only; state only in declared volumes; scratch only in tmpfs.
3. Config via env/secrets/config mounts, not by editing files in place.
4. Changes = new image + redeploy; never `docker exec` to patch.
5. Detect drift: `docker diff` shows files added, changed or deleted in a container's filesystem; compare image digests.
Benefits: an attacker can't drop binaries or modify code; restarts reset state; what you
scanned is what runs.

## Gotchas
- `--read-only` with an entrypoint that `chown`s or writes config templates fails - render
  into a tmpfs path instead.
- tmpfs counts toward memory limits; set sizes.
- `noexec` on /tmp breaks programs that execute files they extract there - give them their own
  exec-allowed tmpfs path.

## Verify
`docker inspect -f '{{.HostConfig.ReadonlyRootfs}}' app` is true; `docker exec app touch /app/x`
fails with `Read-only file system`; `docker diff app` shows changes only under tmpfs/volume paths (or none).

## Checked
Date: 2026-10-24. Documentation: Docker docs `docker run` reference (`--read-only`, `--tmpfs`, `--security-opt no-new-privileges`), `docker container diff` and tmpfs pages, Compose services reference (docker/docs main); Docker Engine API (HostConfig.ReadonlyRootfs).
- Confirmed `--read-only` together with volumes, `--tmpfs` with `rw,noexec,nosuid,size=` options, memory-limit accounting for tmpfs, the Compose `read_only`, `tmpfs` (options `mode`, `uid`, `gid`) and `security_opt` (`no-new-privileges:true`) attributes, `--cap-drop`, `--user`, and `docker diff` A/C/D markers.
- Removed per-language writable-path and runtime-flag claims, the Falco recommendation and JIT-library examples that no checked source covers.
Method: documentation only; no commands were run.
