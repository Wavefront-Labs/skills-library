---
id: computing-software.cloud-infrastructure-engineering.docker.docker-init-project-templates
name: docker-init-project-templates
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, docker-init, project-template, scaffolding, dockerfile, compose, dockerignore, docker-desktop, bootstrap, starter, template-review, readme-docker, init-compose-yaml]
level: intro
status: docs-checked
description: "Bootstrapping a project with docker init: what it generates (Dockerfile, compose.yaml, .dockerignore, README.Docker.md) per language, the prompts, and the edits to make before trusting the scaffold."
sources: ["https://docs.docker.com/reference/cli/docker/init/", "https://docs.docker.com/desktop/release-notes/", "https://docs.docker.com/guides/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# docker init and project templating

**Goal:** go from "repo with no Docker files" to a starter Dockerfile, Compose file and
`.dockerignore`, then review the generated lines before trusting them.

## What it is
`docker init` is provided by **Docker Desktop**: Docker's reference says Docker Desktop provides
the `docker init` CLI command (it first appeared in Desktop 4.18). It is not part of the Linux
engine packages; on a server, copy the output from a workstation or write the files by hand
(see `language-specific-image-patterns`). Check with `docker init --version`.

## Run it
```bash
cd <PROJECT_ROOT>
docker init
```
It walks you through creating `.dockerignore`, `Dockerfile`, `compose.yaml` and
`README.Docker.md` with defaults for your project. Templates offered: ASP.NET Core, Go, Java
(Maven, packaged as an uber jar), Node, PHP with Apache, Python, Rust, and Other (a general
starting point). If any of the files already exist you get a prompt with a warning and the
option to overwrite all of them; overwritten files cannot be recovered, so rename or copy
existing files first. If `docker-compose.yaml` already exists instead of `compose.yaml`, init
can overwrite it using that name.

## Review before trusting it
1. **Dev vs prod**: treat the generated Dockerfile as a starting point; for hot reload add a
   `compose.override.yaml` or `develop: watch:` (see `docker-compose-for-local-dev`).
2. **Base image and runtime version**: confirm the generated base image tag suits your
   dependencies (for example native modules or glibc-only wheels) and pin it.
3. **Port and bind address**: check `EXPOSE` and the published port in `compose.yaml`; bind to
   `127.0.0.1:` for local-only services.
4. **User**: if the app writes files at runtime, check ownership of the target path.
5. **Healthcheck and labels**: add them if you need them.
6. **.dockerignore**: read it; remove entries your build needs.
7. **README.Docker.md**: keep it or fold it into the real README.

## Templating beyond docker init
For an organisation standard, keep a template repository (or a `cookiecutter` / `copier`
template) containing the reviewed Dockerfile, `compose.yaml`, `.dockerignore` and CI workflow
from `building-images-in-ci`; the `docker init` output is a good seed for it. The CLI reference
lists only the `--version` option for `docker init`, so scripted bootstrapping needs your own
template tooling.

## Verify
```bash
docker init                         # answer the prompts
docker compose up --build -d
docker compose exec <service> id    # not uid=0, if the generated Dockerfile sets a non-root user
```

## Checked

2026-10-26 against Docker CLI reference data (docker/docs main, 2026-10-23), containerd image store page, skopeo, containers-transports and crane documentation, Docker Desktop release notes. Confirmed in the docker init reference (data/cli/init) and Desktop release notes: provided by Docker Desktop (docker init first listed in 4.18.0), files created, template list, overwrite prompts and warning, docker-compose.yaml handling, --version as the only option. Removed the detailed claims about generated Dockerfile contents, .dockerignore entries, Compose service blocks, uid values, language-specific install lines and non-interactive support, none of which the reference documents.

Method: documentation only; no commands were run.
