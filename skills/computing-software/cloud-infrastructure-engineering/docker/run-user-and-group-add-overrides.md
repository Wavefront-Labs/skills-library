---
id: computing-software.cloud-infrastructure-engineering.docker.run-user-and-group-add-overrides
name: run-user-and-group-add-overrides
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, docker-run, non-root, user-flag, group-add, uid-gid, docker-socket-group]
level: practitioner
description: "Override the image user with docker run --user uid:gid and add supplementary groups with --group-add, e.g. for docker.sock, video devices or shared volumes."
sources: ["https://docs.docker.com/reference/cli/docker/container/run/", "https://github.com/moby/buildkit/blob/master/frontend/dockerfile/docs/reference.md", "https://github.com/compose-spec/compose-spec/blob/main/spec.md", "https://docs.docker.com/engine/security/userns-remap/"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# docker run --user and --group-add

## --user
```sh
docker run --user 1000:1000 app:1          # uid:gid
docker run --user "$(id -u):$(id -g)" -v "$PWD:/work" -w /work node:22 npm test
docker run --user app app:1                # a user name instead of a uid
docker run --user 0 app:1                  # force root for a debug session
```
- `--user` takes `<name|uid>[:<group|gid>]`.
- For a Dockerfile `USER`, a user without a primary group runs with the root group, and naming a group gives the user only that group's membership.
- Compose: `user: "1000:1000"`. `docker exec -u` overrides per command.

## --group-add
```sh
# let a container use the host's docker socket without being root
docker run --group-add "$(stat -c %g /var/run/docker.sock)" \
  -v /var/run/docker.sock:/var/run/docker.sock ci-agent:1
# GPU/video devices
docker run --device /dev/dri --group-add "$(getent group render | cut -d: -f3)" app
# a group name or number
docker run --group-add audio app
```
Compose: `group_add: ["999"]` (by name or number). `--group-add` adds groups to join, in addition to the user's own.

## Typical uses
- CI jobs writing to a bind-mounted workspace: run as the host UID so files are not root-owned.
- Socket/device access: match the **host** GID numerically; group names differ between host and image.
- Shared volume with setgid dir: `--group-add 2000` so several services can write.

## Gotchas
- Entrypoints that expect to run as root (for example to `chown`) fail under `--user`.
- Docker socket group = root equivalent. Prefer a socket proxy.
- With `userns-remap`, container UIDs map to a subordinate UID range on the host (`/etc/subuid`, `/etc/subgid`), so host ownership won't match what you expect.
- The image may set file perms for its own user only (0700); a different UID can't read them.

## Verify
`docker run --rm --user 1000:1000 --group-add 999 app:1 id` lists 999 among the groups.

## Checked
2026-10-25, against docker/docs engine pages (repository head 2026-10-23) and docker/cli docs/reference/commandline (master), the Dockerfile reference (USER), the Compose specification (`user`, `group_add`) and the userns-remap page. Confirmed: `--user` format `<name|uid>[:<group|gid>]`; `--group-add` "Add additional groups to join"; Compose `group_add` takes names or numbers; Dockerfile USER without a primary group uses the root group; named group means only that group; userns-remap maps to subordinate IDs via `/etc/subuid` and `/etc/subgid`; `docker exec -u` exists. Removed: HOME and `/etc/passwd` claims, rootless-mode mapping claim, entrypoint-bypass wording, exact `id` output.
Method: documentation only; no commands were run.
