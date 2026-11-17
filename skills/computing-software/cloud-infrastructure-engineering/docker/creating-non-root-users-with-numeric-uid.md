---
id: computing-software.cloud-infrastructure-engineering.docker.creating-non-root-users-with-numeric-uid
name: creating-non-root-users-with-numeric-uid
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, dockerfile, non-root, user-instruction, numeric-uid, user-numeric, adduser, useradd-dockerfile, uid-gid]
level: practitioner
description: "Create a system user per distro (useradd, adduser -S, distroless nonroot) and end with USER 10001:10001 so Kubernetes runAsNonRoot can verify it."
sources: ["https://docs.docker.com/reference/dockerfile/#user", "https://docs.docker.com/build/building/best-practices/#user", "https://docs.docker.com/reference/dockerfile/#copy---chown", "https://github.com/GoogleContainerTools/distroless"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Creating non-root users with a numeric UID

`USER <user>[:<group>]` or `USER <UID>[:<GID>]` sets the default user (and optionally group) for
the rest of the current stage; the user is used for `RUN` instructions and at runtime for
`ENTRYPOINT` and `CMD`. A numeric UID works even where no `/etc/passwd` entry exists.

## Per-distro recipes
```dockerfile
# Debian/Ubuntu (shadow-utils): explicit IDs, no faillog bloat with large UIDs
RUN groupadd --system --gid 10001 app \
 && useradd --system --uid 10001 --gid app --no-log-init --no-create-home app

# Alpine (busybox adduser)
RUN addgroup -S -g 10001 app && adduser -S -D -H -u 10001 -G app app

# scratch: there is no useradd; use the numbers directly
USER 10001:10001
```
Distroless publishes `nonroot` tag variants (and `debug-nonroot`) of its images; see the
distroless README for the current tags.

## Why an explicit number
Users and groups created in an image get a non-deterministic "next" UID/GID, so the Docker
best-practices guide says to assign an explicit UID/GID when it matters (for example for
volume ownership). Consistent numbers across your images make that ownership predictable.

## Ownership before switching users
```dockerfile
COPY --chown=10001:10001 --from=build /out/app /app/app
RUN mkdir -p /var/cache/app && chown 10001:10001 /var/cache/app
USER 10001:10001
```
`COPY --chown=<user>:<group>` takes a name or a numeric ID.

## Gotchas
- Docker's guide notes a Go `archive/tar` bug: creating a user with a very large UID can fill
  `/var/log/faillog` with NULL bytes and exhaust disk; pass `--no-log-init` to `useradd`. The
  Debian/Ubuntu `adduser` wrapper does not support this flag.
- When `USER` gives a group, the user has only that group's membership; when the user has no
  primary group the process runs with the `root` group.
- `USER` affects subsequent `RUN`; put package installs before it.
- On Windows the user must be created first (for example with `net user`) unless it is built in.

## Verify
```sh
docker image inspect -f '{{.Config.User}}' app:1     # 10001:10001
docker run --rm app:1 id
```

## Checked

Checked 2026-10-23 against the Dockerfile reference (USER, COPY --chown) and docker/docs build best practices (USER: explicit UID/GID, `--no-log-init`).
Confirmed: USER forms and scope, non-deterministic auto-assigned IDs, the faillog/`--no-log-init` note, group-membership and root-group warnings, Windows note. Removed unconfirmed claims: Kubernetes `runAsNonRoot` named-user behaviour and its error text, the RHEL/UBI `-g 0` recipe, a distroless UID, UID-range advice and the `lastlog` remark.

Method: documentation only; no commands were run.
