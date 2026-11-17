---
id: computing-software.cloud-infrastructure-engineering.docker.compose-post-start-and-pre-stop-hooks
name: compose-post-start-and-pre-stop-hooks
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, compose, post-start, pre-stop, lifecycle-hooks, compose-file, graceful-shutdown]
level: practitioner
status: docs-checked
description: "Use Compose service lifecycle hooks: post_start to run privileged setup after start and pre_stop for backup or drain before stop, their fields, timing and when they do not run."
sources: ["https://docs.docker.com/compose/how-tos/lifecycle/", "https://docs.docker.com/reference/compose-file/services/#post_start", "https://docs.docker.com/reference/compose-file/services/#pre_stop"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Compose post_start and pre_stop hooks

Compose lifecycle hooks (Docker Compose 2.30.0 and later, per the Docker docs feature
banner) run commands inside a service container right after it starts (`post_start`) and
right before it is stopped (`pre_stop`). Hooks can have special privileges (such as running
as root) even when the container itself runs with lower privileges.

## Syntax
```yaml
services:
  app:
    image: app:1.0
    user: "1001"
    volumes: [data:/data]
    post_start:
      - command: chown -R 1001:1001 /data       # one-time fix as root, app itself runs non-root
        user: root
      - command: ["/app/bin/warm-cache"]
        environment: { CACHE_SIZE: "512" }
    pre_stop:
      - command: /app/bin/drain --timeout 20s
        working_dir: /app
volumes: { data: {} }
```
Hook fields: `command` (required; shell form or exec form), `user` (defaults to the service
command's user), `privileged`, `working_dir` (defaults to the service's) and `environment`
(added to or overriding the service environment).

## Semantics
- `post_start` runs after the container has started, but there is no guarantee when
  relative to the container's entrypoint. It suits tasks the application does not need
  completed before it begins, such as registering with an external system. Make hook
  commands idempotent.
- `pre_stop` runs before the container is stopped by a command such as `docker compose
  down` (or Ctrl+C on an attached `up`), before the stop signal is sent, so it suits actions
  that must finish while the application is still fully running (for example backing up a
  data file).
- `pre_stop` hooks do not run if the container stops by itself or is terminated suddenly.

## Good uses
- Fixing volume ownership as root while the service runs as non-root (avoids a root
  entrypoint). The lifecycle page notes that a Docker volume is created with root
  ownership.
- Registering with or deregistering from an external system.
- Copying or flushing data before shutdown.

## Not a replacement for
- Readiness: use `healthcheck` plus `depends_on` with `condition: service_healthy`.
- One-off jobs that must finish before a service starts: use a separate service with
  `condition: service_completed_successfully`.
- Signal handling: the application must still handle the stop signal within its
  `stop_grace_period`.

## Related: pre_start
Newer Compose releases (5.3.0 and later per the docs banner) add `pre_start`, which runs
each step in its own ephemeral container before the service container starts, unlike
`post_start` and `pre_stop`, which run inside the service container.

## Verify
`docker compose version` (hooks need Compose 2.30.0 or later), then start the service and
read the hook's effect (for example the ownership of `/data`).

## Gotchas
- Older Compose versions reject unknown keys; check `docker compose version` first.
- The Compose 2.38.0 release notes include "make sure the post_start hooks fails", so on
  2.38.0 and later a failing `post_start` hook fails the command; behaviour on earlier
  versions differed.

## Checked
Date 2026-10-23. Documentation release: Docker docs (docker/docs main), Compose v5.6.1.
Method: documentation only; no commands were run.
Confirmed in the Compose file reference and lifecycle how-to: hook fields and defaults,
`post_start` timing (no ordering guarantee), `pre_stop` timing and the cases where it does
not run, `pre_start` description; feature banners (2.30.0 hooks, 5.3.0 `pre_start`); Compose
release notes v2.30.0 ("Introduce service hooks") and v2.38.0 (post_start failure). Removed:
the claims that hooks never run on `docker stop` outside Compose, that they run "like
`docker compose exec`", and that a failing hook does not roll back.
