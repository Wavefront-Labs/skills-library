---
id: computing-software.devops-ci-cd.build-systems.devcontainer-json-and-features
name: devcontainer-json-and-features
category: computing-software
field: devops-ci-cd
product: build-systems
tags: [build-systems, devcontainer-json, devcontainer-features, devcontainers]
level: practitioner
status: docs-checked
description: "Define reproducible development environments with devcontainer.json: base images, Features, lifecycle commands, pinned versions and prebuilt images for fast startup."
sources: ["https://containers.dev/implementors/json_reference/", "https://containers.dev/implementors/features/", "https://github.com/devcontainers/spec/blob/main/docs/specs/devcontainer-lockfile.md", "https://github.com/devcontainers/cli", "https://github.com/devcontainers/images/tree/main/src/base-ubuntu"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# devcontainer.json and Features

```jsonc
// .devcontainer/devcontainer.json
{
  "name": "api",
  "image": "mcr.microsoft.com/devcontainers/base:ubuntu24.04",
  "features": {
    "ghcr.io/devcontainers/features/node:2": { "version": "22" },
    "ghcr.io/devcontainers/features/python:1": { "version": "3.12" },
    "ghcr.io/devcontainers/features/docker-in-docker:4": {},
    "ghcr.io/devcontainers/features/terraform:1": { "version": "1.9.8" }
  },
  "postCreateCommand": "npm ci && pip install -r requirements-dev.txt",
  "forwardPorts": [3000, 5432],
  "remoteUser": "vscode",
  "customizations": { "vscode": { "extensions": ["dbaeumer.vscode-eslint", "ms-python.python"] } }
}
```
Published base image tags include `base:ubuntu` (latest LTS), `base:ubuntu24.04` (or `noble`) and `base:ubuntu22.04`. Each Feature has a `version` option; check a Feature's `devcontainer-feature.json` for its current major tag and options before pinning.

## Features
OCI-distributed install scripts (`ghcr.io/devcontainers/features/*` and community). Features are versioned with semver; the reference can carry a major, minor or full version tag. Pin exact tool versions in options and pin the Feature tag. The lockfile `devcontainer-lock.json` (next to `devcontainer.json`) records each Feature's resolved OCI reference with digest, version and integrity checksum; the CLI writes it on `devcontainer build` and `devcontainer up` (opt out with `--no-lockfile`, enforce with `--frozen-lockfile`) and offers `devcontainer outdated` and `devcontainer upgrade`.

## Lifecycle commands
`initializeCommand` runs on the host. Inside the container the order is `onCreateCommand` -> `updateContentCommand` -> `postCreateCommand` -> `postStartCommand` (every start) -> `postAttachCommand`. `onCreateCommand` can be used when caching or prebuilding a container (it normally has no access to user-scoped secrets), so put heavy installs there.

## Prebuilt images
```bash
npx @devcontainers/cli build --workspace-folder . --image-name ghcr.io/org/api-devcontainer:latest --push
```
Then reference `"image": "ghcr.io/org/api-devcontainer:latest"` in `devcontainer.json` so developers start from the prebuilt image.

## Gotchas
- Docker-in-Docker needs `privileged` (the Feature's metadata sets it); the documentation notes security implications on Linux hosts, so consider `docker-outside-of-docker` where acceptable.
- On Linux, `updateRemoteUserUID` (default true) aligns the container user's UID/GID with the host user for bind mounts.

## Verify
- [ ] `devcontainer up --workspace-folder .` from a clean machine yields a working `npm test`.

## Checked
Date: 2026-10-25. Documentation: devcontainers/spec (`devcontainerjson-reference.md`, `devcontainer-lockfile.md`, `devcontainer-features.md`), devcontainers/cli README and `devContainersSpecCLI.ts`, devcontainers/features `src/*/devcontainer-feature.json`, devcontainers/images `src/base-ubuntu`.
Confirmed: lifecycle properties and their order; `initializeCommand` on host; `privileged`, `updateRemoteUserUID` default, `forwardPorts`, `remoteUser`; Feature option names (`version`) and current majors in the repository (node 2.x, docker-in-docker 4.x, terraform 1.x, python 1.x); lockfile name and contents; CLI `build --image-name --push --cache-from`, `--no-lockfile`, `--frozen-lockfile`, `outdated`, `upgrade`; base image tags.
Fixed: the base image tag (`ubuntu24.04`, not `ubuntu-24.04`); Feature majors (node is `:2`; the docker-in-docker example used the older `:2` major, the repository's current major is 4); the lockfile was described via an `--experimental-lockfile` flag, which is hidden: the CLI now writes it by default.
Removed: "second-scale startup" and the Arm Mac note.
Method: documentation only; no commands were run.
