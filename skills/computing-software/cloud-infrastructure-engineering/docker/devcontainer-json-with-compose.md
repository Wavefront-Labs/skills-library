---
id: computing-software.cloud-infrastructure-engineering.docker.devcontainer-json-with-compose
name: devcontainer-json-with-compose
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, devcontainer-json, devcontainer-compose, dev-containers, vscode, devcontainer-cli, devcontainer-features, compose-override, remote-user]
level: practitioner
status: docs-checked
description: "Wire a Dev Container to an existing Compose stack: dockerComposeFile/service/workspaceFolder, an override that keeps the app container idle, features, UID mapping, and the CLI."
sources: ["https://containers.dev/implementors/json_reference/", "https://github.com/devcontainers/spec/blob/main/schemas/devContainer.base.schema.json", "https://docs.docker.com/compose/how-tos/multiple-compose-files/merge/", "https://github.com/devcontainers/cli", "https://github.com/devcontainers/features"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# devcontainer.json with Docker Compose

**Goal:** VS Code (or any Dev Containers client) opens the repo inside the `app` service of
the existing `compose.yaml`, with the DB and other services running beside it, and without
forking the Compose file.

## Layout
```
compose.yaml                         # the real stack (app, db, redis)
.devcontainer/
  devcontainer.json
  compose.devcontainer.yaml          # dev-only overrides for the app service
```

`.devcontainer/devcontainer.json`:
```jsonc
{
  "name": "shop",
  "dockerComposeFile": ["../compose.yaml", "compose.devcontainer.yaml"],
  "service": "app",
  "runServices": ["app", "db", "redis"],
  "workspaceFolder": "/workspace",
  "shutdownAction": "stopCompose",
  "remoteUser": "node",
  "features": {
    "ghcr.io/devcontainers/features/github-cli:1": {},
    "ghcr.io/devcontainers/features/docker-outside-of-docker:1": {}
  },
  "forwardPorts": [3000, "db:5432"],
  "postCreateCommand": "npm ci",
  "customizations": { "vscode": { "extensions": ["dbaeumer.vscode-eslint"] } }
}
```
`.devcontainer/compose.devcontainer.yaml`:
```yaml
services:
  app:
    build:
      target: dev                    # dev stage with tooling, not the slim runtime
    volumes:
      - .:/workspace:cached          # relative to the base file's directory (repo root), see below
    command: sleep infinity          # keep it alive; you run the app from the terminal/debugger
```
- `dockerComposeFile` is a string or an array of Compose files; `service` is the primary
  container your editor connects to; `runServices` lists the services started and stopped
  with the environment (omit it to start all); `workspaceFolder` is typically the target
  path of a volume mount in the Compose file.
- When several Compose files are merged, all relative paths (build contexts, env files,
  bind mounts) are resolved relative to the base file, the first one listed, not to the
  override's own directory (Compose merge guide). Here the base is `../compose.yaml`, so `.`
  is the repo root, not `.devcontainer/`. Inspect the result with
  `docker compose -f compose.yaml -f .devcontainer/compose.devcontainer.yaml config`.
- `command: sleep infinity` keeps the primary container running; if the service's normal
  command exits, the container stops with it.
- `shutdownAction` for Compose configurations accepts `none` or `stopCompose`; the default
  stops all of the Compose containers when you disconnect.

## Users and file ownership
- `remoteUser` is the user used to spawn processes in the container (lifecycle scripts and
  the editor server); `containerUser` is the user the container is started with (default:
  the image's user).
- `updateRemoteUserUID` controls whether, on Linux, the container user is updated with the
  local user's UID and GID; it is on by default when opening from a local folder.

## Features
Features are listed under `features` as `registry/path:version` keys with an options object;
browse the catalogue at containers.dev/features. Rebuild the container after changing them
("Dev Containers: Rebuild Container", or `devcontainer up --remove-existing-container`).

## CLI (CI and scripts)
```bash
npm install -g @devcontainers/cli
devcontainer up --workspace-folder .
devcontainer exec --workspace-folder . npm test
```
`--workspace-folder` is the path where `devcontainer.json` is looked up (default: the
current directory); `--remove-existing-container` removes an existing dev container first.

## Gotchas
- `forwardPorts` entries are a port number or a `name:port` string.
- `postCreateCommand` runs after the container is created: a string runs in a shell, an
  array runs as a single command without a shell, and an object runs its entries in
  parallel.

## Checked
Date 2026-10-23. Documentation release: devcontainers/spec `main` (JSON schema and
reference), devcontainers/cli `main` README and source, devcontainers/features `main`.
Method: documentation only; no commands were run.
Confirmed in the devcontainer JSON schema: `dockerComposeFile`, `service`, `runServices`,
`workspaceFolder`, `shutdownAction` enum `none | stopCompose` and its default,
`remoteUser`, `containerUser`, `updateRemoteUserUID`, `forwardPorts` pattern,
`postCreateCommand` semantics. Confirmed in the CLI repo: `up`, `exec`,
`--workspace-folder`, `--remove-existing-container`, and the npm install command. Confirmed
in the features repo: `github-cli` and `docker-outside-of-docker` exist and are at major
version 1. Confirmed in the Compose merge guide: relative paths resolve against the base (first)
file. Removed: the derived Compose project name, claims about how features are built
for Compose, the non-root restriction on UID mapping, Docker-in-Docker privilege remarks and
host filesystem performance advice.
