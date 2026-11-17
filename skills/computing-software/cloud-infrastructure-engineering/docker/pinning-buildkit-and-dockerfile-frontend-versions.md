---
id: computing-software.cloud-infrastructure-engineering.docker.pinning-buildkit-and-dockerfile-frontend-versions
name: pinning-buildkit-and-dockerfile-frontend-versions
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, reproducible-builds, pinned-frontend, syntax-directive, buildkit-version, setup-buildx-action, buildkitd]
level: advanced
status: docs-checked
description: "Make builds behave the same everywhere: pin the # syntax= frontend by version or digest, pin BuildKit in buildx builders and CI, and check versions with buildx inspect."
sources: ["https://docs.docker.com/build/buildkit/frontend/", "https://docs.docker.com/reference/dockerfile/#syntax", "https://github.com/docker/setup-buildx-action#inputs", "https://docs.docker.com/build/builders/drivers/docker-container/", "https://docs.docker.com/reference/cli/docker/buildx/build/#check"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pinning BuildKit and the Dockerfile frontend

Two moving parts decide how a Dockerfile is interpreted:
1. The **frontend** (Dockerfile parser/LLB generator), chosen by `# syntax=`.
2. The **BuildKit daemon** executing the LLB (embedded in dockerd for the `docker` driver,
   or the `moby/buildkit` image for `docker-container` builders).

## Frontend
```dockerfile
# syntax=docker/dockerfile:1                 # latest stable 1.x (minor and patch updates)
# syntax=docker/dockerfile:1.<minor>         # latest patch of that minor; stops at the next minor
# syntax=docker/dockerfile:1.<minor>.<patch> # immutable, never updated
# syntax=example.com/user/repo:tag@sha256:<digest>   # any frontend image pinned by digest
```
- Without a syntax line, BuildKit uses the Dockerfile frontend bundled with it, which differs
  between builders; Docker recommends an external image so all users get the same version.
- Early-access features need the `labs` channel (`docker/dockerfile:1-labs`, or a pinned labs
  version); labs releases follow the stable version pattern with a `-labs` suffix.
- You can also set the frontend on the command line with the predefined `BUILDKIT_SYNTAX`
  build argument (`--build-arg BUILDKIT_SYNTAX=docker/dockerfile:1`).

## BuildKit daemon
```bash
docker buildx create --name pinned --driver docker-container \
  --driver-opt image=moby/buildkit:<tag> --use
docker buildx inspect --bootstrap pinned
```
The `image` driver option sets the BuildKit image the `docker-container` driver uses (default
`moby/buildkit`). GitHub Actions:
```yaml
- uses: docker/setup-buildx-action@v4
  with:
    version: <buildx version>             # Buildx release, for example latest or a tag
    driver-opts: image=moby/buildkit:<tag>
```
The `docker` driver uses the BuildKit library bundled into the Docker daemon, so its version is
whatever ships with the Engine.

## Upgrade deliberately
- With a specific version such as `1.2` or `1.2.1` the Dockerfile must be updated by hand to keep
  receiving fixes and features; old frontend versions stay compatible with new builders.
- `docker buildx build --check` (shorthand for `--call=check`) runs the Dockerfile build checks
  without building; use it in CI to surface new warnings early.

## Verify
```bash
docker buildx ls                               # builders and their drivers
docker buildx inspect pinned --bootstrap       # boots the builder and shows its nodes
```

## Checked

Checked 2026-10-23 against the Docker docs "Dockerfile frontend" and Dockerfile `syntax` pages, the docker/buildx `build` and `create` references, the Docker docs docker-container driver page, the docker/setup-buildx-action README and the attestations page (main branches).

- Frontend channels and version semantics (`:1`, `:1.2`, `:1.2.1`, `-labs`, digest-pinned image reference), `BUILDKIT_SYNTAX`.
- `--driver-opt image=...` for the `docker-container` driver; setup-buildx-action inputs `version` (Buildx version) and `driver-opts`, current major v4; `--check` shorthand for `--call=check`; docker driver uses the BuildKit library bundled in the daemon.
- Removed the pinned moby/buildkit and buildx version numbers, the Renovate/Dependabot, frontend-mirroring and `DOCKER_BUILDKIT=0` claims, and the grep-based verification.

Method: documentation only; no commands were run.
