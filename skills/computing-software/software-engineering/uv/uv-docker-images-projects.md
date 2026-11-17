---
id: computing-software.software-engineering.uv.uv-docker-images-projects
name: uv-docker-images-projects
category: computing-software
field: software-engineering
product: uv
tags: [uv, docker, container-images, dockerfile, dev-containers, docker-compose, uv-sync]
level: practitioner
status: docs-checked
description: "Pick an official uv Docker image, add uv to your own image, install a locked project, and set up bind-mount or compose watch development."
sources: [https://docs.astral.sh/uv/guides/integration/docker/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# uv in Docker: images, installing uv and projects

Goal: get uv into a container and install a uv project reproducibly.

## Method

Official images live at `ghcr.io/astral-sh/uv`. Distroless tags (`latest`, `{major}.{minor}.{patch}`, `{major}.{minor}`) contain only the uv binaries, for copying. Derived tags include an OS with uv installed (for example `alpine`, `debian`, `debian-slim`, `trixie-slim`, `python3.12-trixie-slim`); versioned forms look like `0.13.7-alpine`. From 0.8 derived images set `UV_TOOL_BIN_DIR=/usr/local/bin`.

```console
$ docker run --rm -it ghcr.io/astral-sh/uv:debian uv --help
```

Add uv to your own image by copying the binary (pin a version tag, or a sha256 digest for reproducible builds):

```dockerfile
FROM python:3.12-slim-trixie
COPY --from=ghcr.io/astral-sh/uv:0.13.7 /uv /uvx /bin/
```

Or use the installer (needs curl and ca-certificates): `ADD https://astral.sh/uv/install.sh /uv-installer.sh`, `RUN sh /uv-installer.sh && rm /uv-installer.sh`, `ENV PATH="/root/.local/bin/:$PATH"`. A versioned URL is `https://astral.sh/uv/0.13.7/install.sh`.

Install a project:

```dockerfile
COPY . /app
ENV UV_NO_DEV=1
WORKDIR /app
RUN uv sync --locked
CMD ["uv", "run", "my_app"]
```

Add `.venv` to `.dockerignore`; the environment is platform specific and should be built in the image.

Use the environment either with `ENV PATH="/app/.venv/bin:$PATH"` or `uv run` in `RUN` lines. Setting `UV_PROJECT_ENVIRONMENT` before syncing installs into the system Python instead.

Tools: put the tool bin directory on PATH (`ENV PATH=/root/.local/bin:$PATH`, then `RUN uv tool install cowsay`), find it with `uv tool dir --bin`, or set `UV_TOOL_BIN_DIR`.

### Developing in a container

Bind-mount the project directory at `/app` and add an anonymous volume at `/app/.venv` so the image's environment is kept:

```console
$ docker run --rm --volume .:/app --volume /app/.venv [...]
```

With Compose (2.22.0 or later) use `develop.watch`, then run `docker compose watch`:

```yaml
develop:
  watch:
    - action: sync
      path: .
      target: /app
      ignore:
        - .venv/
    - action: rebuild
      path: ./pyproject.toml
```

## Verify

Per the page, `docker build` then running the container with `cowsay -t hello` prints the cowsay output when the tool bin directory is on PATH.

## Checked

2026-11-07. Every command, flag, setting, default and example was read against the full text of the cited uv documentation pages (guides/integration/docker). Removed or changed: nothing needed removing.

Method: documentation only; no commands were run.
