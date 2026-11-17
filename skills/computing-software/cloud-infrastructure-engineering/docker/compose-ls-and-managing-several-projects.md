---
id: computing-software.cloud-infrastructure-engineering.docker.compose-ls-and-managing-several-projects
name: compose-ls-and-managing-several-projects
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, compose, compose-ls, compose-project-name, project-name, labels, operations]
level: practitioner
status: docs-checked
description: "Operate many Compose projects on one host: compose ls, finding a project's files from container labels, acting on projects with -p, project naming rules and cleaning up orphans."
sources: ["https://docs.docker.com/reference/cli/docker/compose/ls/", "https://docs.docker.com/compose/how-tos/project-name/", "https://docs.docker.com/reference/cli/docker/compose/", "https://github.com/docker/compose/blob/main/pkg/api/labels.go"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# compose ls and managing several projects

## List projects
```bash
docker compose ls                      # running Compose projects
docker compose ls --all                # include stopped projects
docker compose ls --filter name=shop
docker compose ls --format json        # --format takes table (default) or json
docker compose ls -q                   # project names only
```
`docker compose ls` is described as listing running Compose projects; `-a`/`--all` adds
stopped ones.

## Where is a project's compose file?
Compose stamps containers with labels; the label names are defined in the Compose source
(`pkg/api/labels.go`):
```bash
docker inspect shop-web-1 --format '{{index .Config.Labels "com.docker.compose.project.config_files"}}'
docker inspect shop-web-1 --format '{{index .Config.Labels "com.docker.compose.project.working_dir"}}'
```
Other labels include `com.docker.compose.project`, `com.docker.compose.service` and
`com.docker.compose.config-hash`.

## Act on a project by name
```bash
docker compose -p shop ps
docker compose -p shop logs --tail 50 web
docker compose -p shop stop
docker compose -p shop down
```
Commands that need the Compose model (`up`, `build`, `config`) need the files: change into
the project directory or pass `-f` and `--project-directory`.

## Project names
The name comes from, in order of precedence: the `-p` flag, `COMPOSE_PROJECT_NAME`, the
top-level `name:` in the Compose file (the last one when several `-f` files are given),
the base name of the project directory (or of the first `-f` file), then the base name of
the current directory. A project name may contain only lowercase letters, digits, dashes
and underscores, and must begin with a lowercase letter or digit.

## Orphans
- `docker compose down --remove-orphans` (and `up --remove-orphans`) removes containers for
  services that are no longer defined in the Compose file.
- `COMPOSE_REMOVE_ORPHANS` and `COMPOSE_IGNORE_ORPHANS` are documented environment
  variables for the same behaviour.
- Add `-v` to `down` only when the named volumes are not needed (it removes named volumes
  declared in the file and anonymous volumes attached to containers).

## Conventions that help
- One directory per project (for example `/srv/<project>`), each with `name:` set in
  `compose.yaml`.
- A systemd unit or script per project that calls `docker compose -f <path>/compose.yaml`.
- Label everything with an owner using `labels:` on each service (an `x-` extension field
  with a YAML anchor keeps it in one place).

## Gotchas
- Two project directories with the same base name and no `name:` get the same project name
  and collide.
- Without `--all`, `compose ls` shows only running projects, so a stopped project is hidden.

## Checked
Date 2026-10-23. Documentation release: Compose v5.6.1 CLI reference, docker/docs main.
Method: documentation only; no commands were run.
Confirmed: `ls` options (`-a`, `--filter`, `--format table|json`, `-q`) and its description;
the container label names (Compose source `pkg/api/labels.go`); `down` and `up`
`--remove-orphans`, `down -v` semantics (Compose `down` reference); project name
precedence and character rules (project-name how-to); the existence of
`COMPOSE_REMOVE_ORPHANS` and `COMPOSE_IGNORE_ORPHANS` (Compose environment variables page).
Removed: JSON-processing pipelines, the host inventory script and the claim that `ls`
discovers projects from labels.
