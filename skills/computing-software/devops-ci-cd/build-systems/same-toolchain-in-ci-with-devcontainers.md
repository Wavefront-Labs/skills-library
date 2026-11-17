---
id: computing-software.devops-ci-cd.build-systems.same-toolchain-in-ci-with-devcontainers
name: same-toolchain-in-ci-with-devcontainers
category: computing-software
field: devops-ci-cd
product: build-systems
tags: [build-systems, devcontainers-ci, devcontainer, devcontainers-cli, toolchain-parity, codespaces, reproducible-environment]
level: practitioner
status: docs-checked
description: "Run CI inside the same dev container developers use: devcontainer.json, prebuilt images, devcontainers/ci action and CLI, caching, and keeping local and CI toolchains identical."
sources: ["https://github.com/devcontainers/ci", "https://github.com/devcontainers/ci/blob/main/docs/github-action.md", "https://github.com/devcontainers/cli", "https://containers.dev/implementors/json_reference/", "https://containers.dev/guide/prebuild"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Same toolchain in CI via devcontainers/ci

"Works on my machine" usually means a different compiler, SDK or tool version. If developers use a dev container, run CI in that same container image.

## devcontainer.json
```json
{
  "name": "app",
  "build": { "dockerfile": "Dockerfile", "context": ".." },
  "features": {
    "ghcr.io/devcontainers/features/node:2": { "version": "20" },
    "ghcr.io/devcontainers/features/terraform:1": { "version": "1.9.5" }
  },
  "postCreateCommand": "npm ci",
  "remoteUser": "vscode"
}
```
Pin versions in Feature options and the base image (by digest for strictness); a floating `latest` defeats the point.

## Prebuild the image
Building Features on every CI run is slow. Publish an image:
```yaml
- uses: devcontainers/ci@v0.3
  with:
    imageName: ghcr.io/org/app-devcontainer
    cacheFrom: ghcr.io/org/app-devcontainer
    push: filter
    refFilterForPush: refs/heads/main
    runCmd: npm test
```
`push` accepts `never`, `filter` (the default: push when `refFilterForPush` and `eventFilterForPush` match) or `always`. On main it builds and pushes; on PRs it reuses the cache and runs `runCmd` inside the container. Then reference the prebuilt image from devcontainer.json (`"image": "ghcr.io/org/app-devcontainer:latest"`) so developers start fast too. The action needs a registry login (for example `docker/login-action`) to push.

## devcontainers CLI (any CI)
```bash
npm install -g @devcontainers/cli
devcontainer build --workspace-folder . --image-name app-dev --cache-from ghcr.io/org/app-devcontainer
devcontainer up --workspace-folder .
devcontainer exec --workspace-folder . make test
```
`devcontainer build`, `up` and `exec` are the CLI's documented commands for building, starting and running commands in a dev container; it only needs Docker, so it is not tied to GitHub Actions.

## Alternatives for parity
- Run CI jobs with `container: ghcr.io/org/app-devcontainer:<tag>` directly (GitHub `jobs.<id>.container`, GitLab `image:`), skipping the CLI. Lifecycle commands such as `postCreateCommand` are executed by dev container tooling, so they will not run; put setup in the image.
- Version managers (`.tool-versions` with asdf/mise, `.nvmrc`, `global.json`, `rust-toolchain.toml`) honoured both locally and in CI setup actions - lighter-weight parity.
- Nix flakes for fully pinned toolchains.

## Pitfalls
- UID mismatch: `updateRemoteUserUID` (default true, Linux) aligns the container user's UID/GID with the host user; CI runners may need an explicit `--user`. The action has a `skipContainerUserIdUpdate` input.
- Docker-in-Docker needs `privileged`; prefer `docker-outside-of-docker` or service containers where acceptable.
- Image drift: rebuild regularly for security patches, but via a PR so toolchain bumps are visible.

## Verify
- [ ] `node --version`, compiler and CLI versions print identically in a local dev container and in CI logs.
- [ ] CI uses the prebuilt image on PRs (job time not dominated by Feature installs).

## Checked
Date: 2026-10-25. Documentation: devcontainers/ci `action.yml` and `docs/github-action.md`, devcontainers/cli README and source, devcontainers/spec `devcontainerjson-reference.md`, devcontainers/features metadata.
Confirmed: action inputs `imageName`, `cacheFrom`, `cacheTo`, `push` (never/filter/always, default filter), `refFilterForPush`, `eventFilterForPush`, `runCmd`, `skipContainerUserIdUpdate`; action tag `v0.3`; registry login requirement; CLI `build --image-name --cache-from`, `up`, `exec`; `updateRemoteUserUID` default; `privileged` for Docker-in-Docker; Feature majors (node 2, terraform 1).
Removed: the sentence that the CLI "works in GitLab, Jenkins, Azure Pipelines", the `--user` fix for CI as a stated rule, the "rebuild weekly" cadence, and the CI-job `container:` hook behaviour is now phrased from the spec's description of lifecycle commands.
Method: documentation only; no commands were run.
