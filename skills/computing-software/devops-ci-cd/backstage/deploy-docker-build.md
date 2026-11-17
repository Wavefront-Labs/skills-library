---
id: computing-software.devops-ci-cd.backstage.deploy-docker-build
name: deploy-docker-build
category: computing-software
field: devops-ci-cd
product: backstage
tags: [docker-build, host-build, backend-dockerfile, backstage]
level: practitioner
status: docs-checked
description: "Build the Backstage backend into a Docker image using the host build and the packages/backend Dockerfile."
sources:
  - https://backstage.io/docs/deployment/docker
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Backstage provides tooling to build Docker images. The docs recommend a host build for its speed and simpler, more efficient caching: compile on the machine or CI runner, then package the result.

```bash
yarn install --immutable
yarn tsc
yarn build:backend
docker image build . -f packages/backend/Dockerfile --tag backstage
docker run -it -p 7007:7007 backstage
```

- `yarn tsc` outputs type definitions to `dist-types/` in the repo root for the build to consume.
- `yarn build:backend` bundles the backend into `packages/backend/dist`.
- The container listens on port 7007.

Key points in the supplied Dockerfile:

- It starts from a Node slim image and installs `libsqlite3-dev` only if you use sqlite3, in which case you move `better-sqlite3` to `devDependencies` otherwise.
- It switches to the least-privileged `node` user and sets `WORKDIR /app`; if the directory is created as root the `tar` extraction fails, which BuildKit (`DOCKER_BUILDKIT=1`) avoids.
- It sets `NODE_ENV=production` and copies the repo skeleton before sources so Docker layer caching works.

A multi-stage build, also documented, does the build inside Docker and suits environments without a prepared host. Add `--progress=plain --no-cache` when debugging a build.

At runtime the container is started with `--config` files for the app configuration.

## Checked

2026-11-03. Confirmed on the Docker deployment page: host build recommended for speed and caching, multi-stage build as the second option, the build commands and `dist-types`, `packages/backend/dist`, port 7007, the Dockerfile points on the `node` slim image, `libsqlite3-dev` and `better-sqlite3` in `devDependencies`, the least-privileged `node` user, `WORKDIR /app` with the `tar` failure and `DOCKER_BUILDKIT=1`, `NODE_ENV=production`, the repo skeleton copied first for layer caching, `--progress=plain`, and `--config` at startup. Removed: the secrets-as-environment-variables sentence and a sentence that belonged to the Kubernetes page.

Method: documentation only; no commands were run.
