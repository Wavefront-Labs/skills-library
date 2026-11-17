---
id: computing-software.cloud-infrastructure-engineering.docker.compose-watch-ignore-include-and-initial-sync
name: compose-watch-ignore-include-and-initial-sync
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, compose-watch, watch-ignore, initial-sync, sync-exec, dev-workflow, dockerignore]
level: practitioner
status: docs-checked
description: "Tune Compose watch rules: ignore and include patterns, .dockerignore effects, initial_sync on start, sync+exec hooks, and avoiding rebuild storms."
sources: ["https://docs.docker.com/compose/how-tos/file-watch/", "https://docs.docker.com/reference/compose-file/develop/", "https://github.com/docker/compose/releases/tag/v2.39.4"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Compose watch: ignore, include and initial sync

## Rule anatomy
```yaml
services:
  web:
    build: .
    develop:
      watch:
        - action: sync
          path: ./src
          target: /app/src
          ignore:
            - "**/*.test.ts"          # relative to path (./src)
            - generated/
          initial_sync: true          # needs Compose 2.39.4 or later
        - action: sync+exec
          path: ./templates
          target: /app/templates
          exec:
            command: app reload       # run in the container after the sync
        - action: rebuild
          path: package.json
        - action: sync+restart
          path: ./config
          target: /app/config
          include: ["*.yaml"]         # only matching files are considered
```
Start with `docker compose up --watch` or `docker compose watch`.

## How patterns apply
- `ignore` patterns are relative to the rule's `path`, not the project root. Syntax is the
  `.dockerignore` one: `*`, `?`, `*/*` and `**` (any depth).
- If the build context has a `.dockerignore`, its patterns are loaded as implicit `ignore`
  content and the values in the Compose model are appended.
- Editor temporary or backup files and `.git` directories are ignored automatically.
- `include` selects the files to watch instead of listing those to skip: only files that
  match are considered when applying the rule. Wrap patterns that start with `*` in quotes
  (a bare `*` is a YAML alias).
- Glob patterns are not supported in `path`.

## initial_sync
With `sync+x` actions, `initial_sync` makes Compose ensure that files inside existing
containers are up to date with `path` at the start of a watch session; it applies if
containers for the service already exist. The Compose 2.39.4 release notes list "Add support
of `develop.watch.initial_sync` attribute"; earlier releases do not know the key. Without it,
rebuild once (`up --build --watch`) after a branch switch.

## Avoiding rebuild storms
- Point `rebuild` rules at dependency manifests only (`package.json`, `requirements.txt`,
  `go.mod`), not whole source trees.
- Ignore build outputs written back by the application so they do not re-trigger syncs.
- Do not combine a bind mount and a sync rule for the same path.

## Gotchas
- `sync` requires the container user to be able to write to the target path, and the image to
  contain `stat`, `mkdir` and `rmdir`.
- Watch only helps services built from local source with `build:`; services that only use
  `image:` are not tracked.
- You do not need to enable watch for every service; services without `develop.watch` are
  started normally.

## Checked
Date 2026-10-23. Documentation release: Docker docs (docker/docs main), Compose v5.6.1;
GitHub release notes of docker/compose v2.39.4 for `initial_sync`.
Method: documentation only; no commands were run.
Confirmed in the Compose Watch guide and `develop` reference: `ignore` and `include`
semantics and syntax, `.dockerignore` loading, automatic ignores, `initial_sync` description,
`sync+exec` and its `exec` fields, prerequisites, and the build-only scope. Removed: the
claim that `node_modules/` is ignored by default, and "monorepo is slow on macOS/Windows"
remarks.
