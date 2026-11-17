---
id: computing-software.cloud-infrastructure-engineering.docker.buildkit-secret-mounts-file-vs-env
name: buildkit-secret-mounts-file-vs-env
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, buildkit, build-secrets, secret-mount, secret-env, secret-file-mount, dockerfile, npm-token, pip-index]
level: practitioner
description: "Pass build secrets with --secret and RUN --mount=type=secret as a file or env var (env=), with required=true, uid/mode, and checks that nothing lands in a layer."
sources: ["https://docs.docker.com/build/building/secrets/", "https://docs.docker.com/reference/dockerfile/#run---mounttypesecret", "https://docs.docker.com/reference/cli/docker/buildx/build/#secret", "https://docs.docker.com/reference/compose-file/build/#secrets"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# BuildKit secret mounts: file vs env

**Goal:** give one `RUN` step a token, credentials file or SSH-free auth without it
appearing in a layer, in `docker history`, or in the build cache key.

## Supplying the secret (CLI side)
```sh
# from a file
docker build --secret id=npmrc,src=$HOME/.npmrc .
# from an environment variable (explicit)
docker build --secret id=gh_token,env=GITHUB_TOKEN .
# shorthand: env var named like the id is mounted at /run/secrets/GITHUB_TOKEN
GITHUB_TOKEN=... docker build --secret id=GITHUB_TOKEN .
```
Compose: `build.secrets: [npmrc]` plus top-level `secrets: npmrc: {file: ~/.npmrc}` or `{environment: GITHUB_TOKEN}`.
Bake: `secret = ["id=npmrc,src=${HOME}/.npmrc"]` (declare `variable "HOME" { default = null }`
so Bake reads it from the environment).

## Consuming it (Dockerfile side)
```dockerfile
# syntax=docker/dockerfile:1
# As a file (default target /run/secrets/<id>)
RUN --mount=type=secret,id=npmrc,target=/root/.npmrc,required=true \
    npm ci --omit=dev

# As an env var only for this RUN (dockerfile frontend 1.10+)
RUN --mount=type=secret,id=gh_token,env=GITHUB_TOKEN,required=true \
    git clone https://x-access-token:${GITHUB_TOKEN}@github.com/org/private.git
```
| Option | Meaning |
|---|---|
| `id` | name passed on `--secret` (defaults to basename of target) |
| `target` | file path; default `/run/secrets/<id>` when `env` is not set |
| `env` | expose as env var instead of, or as well as, a file (Dockerfile 1.10.0 and later) |
| `required` | fail the build if the secret is unavailable (default **false**) |
| `mode`,`uid`,`gid` | file mode (default 0400), owner and group (default 0); set `uid`/`gid` when the step runs as a non-root `USER` |

## File or env?
- **File** for tools that read config files (`.npmrc`, `~/.aws/credentials`); the secret is
  available only for the duration of that build instruction.
- **env=** for CLIs that read token variables; the secret is mounted as an environment variable
  for that `RUN` step and is not baked into the image.
- Build arguments and `ENV` persist in the final image, so never pass secrets that way, and never
  copy a secret to a file outside the mount.

## Gotchas
- `required` defaults to `false`, so set `required=true` to make a missing secret fail the
  build.
- Secret contents are not part of the build cache, so changing the value does **not** bust it.
  To force invalidation pass a build argument with an arbitrary value that you change along
  with the secret (the Docker docs use `ARG CACHEBUST`), or use `--no-cache-filter <stage>`.
- Secret mounts are an option of `RUN --mount`; the consuming instruction is `RUN`.
- On Windows containers an explicit `target` is required, `mode`/`uid`/`gid` are ignored and the
  step must run as an administrator.

## Verify
```sh
docker history --no-trunc app:dev | grep -i token          # nothing
docker run --rm app:dev ls -la /run/secrets 2>&1           # no such directory
docker buildx build --secret id=wrong .                     # with required=true -> fails fast
```

## Checked

Checked 2026-10-23 against the Dockerfile reference (`RUN --mount=type=secret`, moby/buildkit main branch), the Docker docs "Build secrets" page, the compose-spec build and secrets pages, and the docker/buildx `build --secret` reference.

- Option table (`id`, `target`, `env` since Dockerfile v1.10.0, `required` default false, `mode` 0400, `uid`, `gid`), default path `/run/secrets/<id>`.
- `--secret id=...,src=...`, `id=...,env=...` and the `id=NAME` shorthand for an environment variable; Bake `secret` with `${HOME}`.
- Secret contents are excluded from the cache; `ARG CACHEBUST` forces invalidation.
- Compose `build.secrets` with top-level `secrets` whose source is `file` or `environment`.
- Removed the claims about tmpfs, the legacy builder, `ADD`/`COPY` and npm logging, which the docs do not state.

Method: documentation only; no commands were run.
