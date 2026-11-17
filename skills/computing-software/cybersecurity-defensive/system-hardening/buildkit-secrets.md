---
id: computing-software.cybersecurity-defensive.system-hardening.buildkit-secrets
name: buildkit-secrets
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [buildkit-secrets, docker-build, secret-mounts, ssh-mounts, container-hardening, image-security]
level: practitioner
status: docs-checked
description: "Pass credentials into Docker builds without leaking them into layers: BuildKit secret and SSH mounts, CI usage, why ARG and ENV leak, and checking images for leftovers."
sources: ["https://docs.docker.com/build/building/secrets/", "https://docs.docker.com/reference/dockerfile/#run---mounttypesecret", "https://docs.docker.com/build/checks/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BuildKit build secrets

Builds often need credentials (private package registry tokens, Git deploy keys). Docker's guidance: build
arguments and environment variables are inappropriate for passing secrets because they persist in the final image.
Use secret mounts or SSH mounts, which expose the secret only for the duration of the build instruction.

## Secret mounts
Pass the secret on the build command, then consume it in a `RUN` step:
```bash
docker build --secret id=aws,src=$HOME/.aws/credentials .
docker build --secret id=API_KEY .          # source is the API_KEY environment variable
```
```dockerfile
# syntax=docker/dockerfile:1
FROM python:3
RUN --mount=type=secret,id=aws,target=/root/.aws/credentials \
    aws s3 cp s3://... ...
# or as an environment variable (since Dockerfile v1.10.0):
RUN --mount=type=secret,id=API_KEY,env=API_KEY \
    some-command --token-from-env $API_KEY
```
`--mount=type=secret` options: `id`, `target` (default `/run/secrets/<id>` when `env` is unset), `env`, `required`
(default false: set true to fail when the secret is missing), `mode` (default 0400), `uid`, `gid`. The source of a
`--secret` can be a file or an environment variable (`type=file` or `type=env`, detected automatically by the CLI).
On Windows containers the secret is a read-only bind mount, an explicit `target` is required, and `mode`, `uid`
and `gid` are ignored.

## SSH mounts
```dockerfile
# syntax=docker/dockerfile:1
FROM alpine
RUN apk add --no-cache openssh-client
RUN mkdir -p -m 0700 ~/.ssh && ssh-keyscan gitlab.com >> ~/.ssh/known_hosts
RUN --mount=type=ssh ssh -q -T git@gitlab.com
```
Build with `docker buildx build --ssh default .` to forward the host SSH agent. `--mount=type=ssh` options: `id`
(default `default`), `target` (default `/run/buildkit/ssh_agent.${N}`), `required` (default false), `mode` (default
0600), `uid`, `gid`. Populate `known_hosts` as above rather than accepting host keys blindly.

## CI
- Use short-lived tokens so a leaked value expires quickly.
- Check your CI action or builder documents how it passes `--secret` and `--ssh` before relying on it.

## Anti-patterns
- `ARG NPM_TOKEN` then writing it into `.npmrc` in a `RUN` step: build arguments and environment variables
  persist in the image.
- `ENV` secrets persist in the image config.
- Multi-stage builds reduce exposure only if the secret never touched the final stage; intermediate stages can
  still be pushed or cached.
`docker build --check` runs BuildKit build checks and exits non-zero if violations are reported; use it in CI.

## Check images
Review `docker history --no-trunc <image>` and `docker inspect <image>` (Env) for tokens, and run a secret scanner
of your choice over the image.

## Verify
Image history and config contain no tokens; the build works in CI only with the secret supplied.

## Checked
2026-10-31. Confirmed against Docker docs (Build secrets, Dockerfile reference RUN --mount=type=secret and
type=ssh, Build checks): secret and SSH mount options and defaults, `env` since Dockerfile v1.10.0, `--secret`
sources, `--ssh default`, `docker build --check` non-zero exit, ARG/ENV persistence. Removed unconfirmed: the
BuildKit 0.13 version gate, tmpfs claim, syntax 1.4 default claim, `--index-url`/`--omit` example flags, the
SecretsUsedInArgOrEnv check name, GitLab/Kaniko/Buildah/OIDC CI statements, and named scanner flags.
Method: documentation only; no commands were run.
