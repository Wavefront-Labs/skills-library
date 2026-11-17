---
id: computing-software.cloud-infrastructure-engineering.docker.compose-watch-actions-and-node-modules
name: compose-watch-actions-and-node-modules
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, compose, compose-watch, hot-reload, dev-workflow, watch-sync, watch-rebuild, sync-restart, node-modules-volume, anonymous-volume-exclude]
level: practitioner
status: docs-checked
description: "Set up docker compose watch with sync, rebuild, restart, sync+restart and sync+exec actions and ignore rules, and keep container node_modules from being clobbered by bind mounts."
sources: ["https://docs.docker.com/compose/how-tos/file-watch/", "https://docs.docker.com/reference/compose-file/develop/", "https://docs.docker.com/reference/compose-file/services/#volumes", "https://docs.docker.com/reference/cli/docker/compose/up/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---
# Compose watch actions and node_modules

## develop.watch
```yaml
services:
  web:
    build: .
    command: npm run dev
    develop:
      watch:
        - action: sync               # copy changed files into the container (hot reload handles the rest)
          path: ./src
          target: /app/src
          ignore: [node_modules/, "**/*.test.ts"]
        - action: rebuild            # rebuild the image and recreate the container
          path: package.json
        - action: sync+restart       # copy, then restart the container
          path: ./config
          target: /app/config
        - action: sync+exec          # copy, then run a command in the container
          path: ./schema
          target: /app/schema
          exec: { command: ["npm", "run", "codegen"] }
```
```sh
docker compose up --watch          # or: docker compose watch (keeps build and sync events out of the app logs)
```
Actions and the Compose version that introduced them (Compose file reference):
`rebuild` and `sync`; `sync+restart` from 2.23.0; `restart` and `sync+exec` from 2.32.0.
- Each rule needs a `path` and an `action`. Paths are relative to the project directory
  (except `ignore` patterns), directories are watched recursively, and glob patterns are
  not supported in `path`.
- For `sync`, the image must contain `stat`, `mkdir` and `rmdir`, and the container's
  `USER` must be able to write to the target path (the docs suggest `COPY --chown` in the
  Dockerfile).
- `ignore` patterns are relative to the rule's `path`, use `.dockerignore` syntax, and are
  appended to the patterns loaded from the build context's `.dockerignore`. Editor temporary
  files and `.git` directories are ignored automatically.
- Watch is designed for services built from local source with `build:`; it does not track
  services that only use a pre-built `image:`.
- `rebuild` behaves like `docker compose up --build <svc>`; superseded dangling images are
  removed after each rebuild unless you run `docker compose watch --prune=false`.
- Watch rules let you ignore specific files or directories within the watched tree, which a
  bind mount cannot do.

## node_modules: the bind-mount trap
With a bind mount of the project, the host's `node_modules` (built for another OS or
architecture) shadows the one built in the image. Docker's watch guide recommends not
syncing `node_modules/`, because npm packages can contain native code that is not portable.
```yaml
services:
  web:
    build: .
    volumes:
      - ./:/app
      - /app/node_modules            # anonymous volume masks the bind for this path
```
- Compose copies image data into a new volume at creation, so the anonymous volume starts
  with the image's `/app/node_modules`; `up --renew-anon-volumes` (`-V`) recreates
  anonymous volumes instead of retrieving data from the previous containers, and
  `down -v` removes anonymous volumes attached to containers.
- With `watch` and `sync`, add `ignore: [node_modules/]` and use a `rebuild` rule on
  `package.json` so dependency changes rebuild the image.

## Verify
Run `docker compose up --watch`, edit a file under `src` and see it synchronised; edit
`package.json` and see the service rebuilt and recreated.

## Checked
Date 2026-10-23. Documentation release: Docker docs (docker/docs main), Compose v5.6.1.
Method: documentation only; no commands were run.
Confirmed in the "Use Compose Watch" guide and the `develop` reference: the action list and
version notes, path and ignore rules, prerequisites (`stat`, `mkdir`, `rmdir`; this corrects
an earlier claim of `rm`), `.dockerignore` handling, automatic ignores, rebuild behaviour and
`--prune`, `watch` command, and `up -V`/`down -v` descriptions. Removed: Docker Desktop
performance claims, the watch-output log message, and the claim that `node_modules/` is
ignored by default.
