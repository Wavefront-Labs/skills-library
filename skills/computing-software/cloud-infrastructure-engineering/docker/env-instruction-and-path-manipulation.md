---
id: computing-software.cloud-infrastructure-engineering.docker.env-instruction-and-path-manipulation
name: env-instruction-and-path-manipulation
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, dockerfile, env-instruction, env-path, environment-variables, build-checks, legacy-key-value-format]
level: practitioner
status: docs-checked
description: "Use ENV correctly: key=value form, same-line expansion order, prepending to PATH for venvs and toolchains, build-only values via ARG or RUN-scoped vars, and runtime overrides."
sources: ["https://docs.docker.com/reference/dockerfile/#env", "https://docs.docker.com/reference/dockerfile/#environment-replacement", "https://docs.docker.com/reference/build-checks/legacy-key-value-format/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ENV and PATH manipulation

## Forms
```dockerfile
ENV APP_HOME=/opt/app LOG_LEVEL=info          # preferred: key=value, several per line
ENV APP_HOME /opt/app                          # legacy space form: one var, build check LegacyKeyValueFormat warns
```
Quote values with spaces: `ENV GREETING="hello world"`.

## Expansion order on one line
```dockerfile
ENV abc=hello
ENV abc=bye def=$abc      # def=hello: expansion uses values from BEFORE this instruction
ENV ghi=$abc              # ghi=bye
```

## PATH
```dockerfile
# Python venv: activate by PATH instead of "source activate" (each RUN is a new shell)
ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Toolchains
ENV PATH="/usr/local/go/bin:/root/go/bin:$PATH"
ENV PATH="/usr/local/cargo/bin:$PATH"
```
- Prepend to `$PATH` rather than replacing it, so the base image's entries stay.
- Setting `PATH` explicitly is safest on minimal base images.
- `docker run -e PATH=...` overwrites the image's PATH for that container, so include the entries
  the image relies on.

## Build-only values
`ENV` persists into every child image and every container. For values only the build needs:
```dockerfile
ARG DEBIAN_FRONTEND=noninteractive               # not persisted
RUN apt-get update && apt-get install -y tzdata
RUN PIP_NO_CACHE_DIR=1 pip install -r req.txt    # scoped to one RUN
```
The reference warns that `ENV DEBIAN_FRONTEND=noninteractive` persists into containers, changes
the behaviour of `apt-get` and may confuse users of your image.

## Runtime override precedence
`docker run -e`, `--env` and `--env-file` set or overwrite variables defined in the image. In
Compose, when both `env_file` and `environment` are set, `environment` takes precedence.
Check the effective set with `docker exec <c> env` or
`docker inspect -f '{{json .Config.Env}}' <c>`.

## Gotchas
- Each `ENV` line is a metadata change; fine for caching, but changing a value near the top
  invalidates every later step.
- The `UndefinedVar` build check warns when you reference a variable that is never defined
  (typos like `$PAHT`).
- Secrets in `ENV` are visible in `docker inspect` and `docker history`.

## Checked

Checked 2026-10-23 against the Dockerfile reference (ENV, environment replacement; moby/buildkit docs main), the `docker run` reference, the Compose services reference and the BuildKit rule pages LegacyKeyValueFormat and UndefinedVar.
Confirmed: `key=value` form and the legacy space form warning; same-instruction expansion order (def=hello, ghi=bye); ENV persists in containers and the DEBIAN_FRONTEND ARG alternative; `-e`/`--env-file` overwrite image variables; Compose `environment` over `env_file`. Removed the unconfirmed precedence between `--env-file` and `-e` and the distroless PATH claim.

Method: documentation only; no commands were run.
