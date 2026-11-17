---
id: computing-software.cloud-infrastructure-engineering.docker.docker-init-language-templates-and-existing-projects
name: docker-init-language-templates-and-existing-projects
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, docker-init, scaffolding, project-template, init-go, init-python, init-node, init-existing-project, init-java, init-rust, init-aspnet]
level: practitioner
description: "Use docker init to generate Dockerfile, compose.yaml and .dockerignore per language (Go, Python, Node, Rust, Java, .NET, PHP), and adopt it safely in existing repos."
sources: ["https://docs.docker.com/reference/cli/docker/init/", "https://docs.docker.com/reference/dockerfile/"]
status: docs-checked
licence: Apache-2.0
version: 4
updated: 2026-11-17
---
# docker init: language templates and existing projects

## What it generates
```sh
cd my-service && docker init
```
Interactive prompts pick a template and ask a few questions; output:
- `Dockerfile`
- `compose.yaml`
- `.dockerignore`
- `README.Docker.md`

`docker init` is provided by Docker Desktop. If `docker-compose.yaml` already exists instead of `compose.yaml`, it can overwrite that file under the same name.

| Template | Prompts shown in Docker's examples |
|---|---|
| Go | Go version, relative directory of the main package, server port |
| Python | Python version, port, command to run the app |
| Node | Node version, package manager, whether to run a build step and its output directory, start command, port |
| Rust | Rust version, port |
| Java (Maven, packaged as an uber jar) | Java version, relative app directory, port |
| ASP.NET Core | main project name, .NET version, local port |
| PHP with Apache | PHP version, relative app directory, local port |
| Other | general purpose starting point |

The project platform is offered with a `(detected)` marker when Docker recognises it. The only documented flag of `docker init` is `--version`; there is no documented non-interactive mode.

## Running in an existing project
- If any of the files exist, `docker init` shows a warning and offers to overwrite them; overwritten files cannot be recovered, so rename or copy them first (or commit and review with `git diff`).
- Run it in the directory of the project you are containerising.
- Always review the generated files and tailor them to your project, as Docker advises.

## Review checklist for generated files
- Check the base image versions and pin tags (and digests) to what you support.
- Add a `HEALTHCHECK` if the app needs one and confirm the real port.
- Check `.dockerignore` excludes `.env`, `.git`, local build output and secrets.
- Tidy `compose.yaml` for your services.
- Build and run with `docker compose up --build`, as `docker init` itself suggests.

## Verify
`docker build .` succeeds and `docker compose up --build` serves on the expected port; check the `USER` the generated Dockerfile sets rather than assuming one.

## Checked

Checked against the `docker init` reference in docker/docs (`data/cli/init/docker_init.yaml`: description, templates, examples, options) (docker/docs latest commit 2026-10-23).

- Generated files (`.dockerignore`, `Dockerfile`, `compose.yaml`, `README.Docker.md`), overwrite warning and non-recoverable overwrite, template list (ASP.NET Core, Go, Java with Maven as uber jar, Node, PHP with Apache, Python, Rust, Other), per-template prompts, `(detected)` marker, `--version` as the only option.
- Removed as unconfirmed: per-template Dockerfile defaults (cache mounts, `CGO_ENABLED`, UIDs, `USER node`), file-based language detection rules, Gradle support, the non-interactive mode claim and the `docker scout` step.

Method: documentation only; no commands were run.
