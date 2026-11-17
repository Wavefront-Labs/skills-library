---
id: computing-software.cloud-infrastructure-engineering.docker.keeping-secrets-out-of-the-build-context
name: keeping-secrets-out-of-the-build-context
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, dockerignore, context-secrets-leak, dockerignore-secrets, build-context, secret-mount, image-security]
level: practitioner
status: docs-checked
description: "Stop .env, .git, cloud credentials and .npmrc tokens from entering images via COPY . .; ignore rules, secret mounts instead of files, and how to audit existing images."
sources: ["https://docs.docker.com/build/concepts/context/#dockerignore-files", "https://docs.docker.com/build/building/secrets/", "https://docs.docker.com/build/metadata/attestations/slsa-provenance/", "https://docs.docker.com/reference/compose-file/build/#secrets", "https://trivy.dev/latest/docs/scanner/secret/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Keeping secrets out of the build context

Anything in the context can end up in a layer via `COPY . .`, and a later `RUN rm` does not
remove it from the earlier layer. Anyone who can pull the image can read its layers.

## Ignore these in every repo
Use a `.dockerignore` file in the context root (the build client removes matching files from
the context before sending it to the builder; a per-Dockerfile `<name>.Dockerfile.dockerignore`
is also supported). Typical entries:
```gitignore
.git
.env
.env.*
!.env.example
*.pem
*.key
id_rsa*
.npmrc
.pypirc
.netrc
secrets/
```
`.git` can hold credentials in remote URLs and its churn is rarely wanted in a build context.

## Files the build legitimately needs: use secret mounts
```dockerfile
# syntax=docker/dockerfile:1
RUN --mount=type=secret,id=npmrc,target=/root/.npmrc npm ci
RUN --mount=type=secret,id=pip,target=/etc/pip.conf pip install -r requirements.txt
```
```bash
docker build --secret id=npmrc,src=$HOME/.npmrc --secret id=pip,src=./pip.conf .
```
Docker's secrets guide: build arguments and environment variables are inappropriate for
secrets because they persist in the final image; a secret mount exposes the file only to that
`RUN` step. (`--secret` format: `id=mysecret[,src=/local/secret]`.)

## Audit an existing image
```bash
trivy image myapp:latest        # secret scanning is enabled by default in Trivy
docker history --no-trunc myapp:latest
```
Also check intermediate layers: a file deleted later is still inside its original layer.

## If something leaked
1. Rotate the credential first. Removing the image does not un-leak it.
2. Rebuild without it and delete the affected tags and digests from every registry and mirror.
3. Purge CI build caches that may hold the layer (registry cache refs, GHA cache).

## Gotchas
- `--build-arg TOKEN=...` values persist in the image; provenance attestations at `mode=max`
  include build argument values (they are not included in `mode=min`). Never pass secrets as args.
- Compose `build.secrets` grants per-service build access to secrets defined at the top level;
  use it instead of `args`.

## Checked

2026-10-26 against Docker docs (docker/docs main, 2026-10-23), Compose file reference, tini, Trivy and metadata-action documentation. Confirmed: .dockerignore behaviour and per-Dockerfile ignore files (build context docs), secret mounts and --secret format (secrets guide and buildx build reference), build args and env persisting in the image, provenance mode=min versus mode=max content, Compose build.secrets, Trivy secret scanning enabled by default. Removed the long cloud-config ignore list, the find and grep audit commands, and the unconfirmed claim that secret mounts never affect the cache key.

Method: documentation only; no commands were run.
