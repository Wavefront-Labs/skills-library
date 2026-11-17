---
id: computing-software.software-engineering.pnpm.docker-build-recipes
name: docker-build-recipes
category: computing-software
field: software-engineering
product: pnpm
tags: [docker-multi-stage, docker-monorepo, pnpm-fetch, prod-deps-stage, pnpm-runtime-set, docker-ci-build]
level: advanced
status: docs-checked
description: "Dockerfile patterns for pnpm: multi-stage prod-deps and build stages with cache mounts, per-app pnpm deploy in a monorepo, pnpm fetch with offline install without cache mounts."
sources:
  - https://pnpm.io/docker
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Single app, multi-stage with BuildKit cache mount (store kept at a separate path because mounting over `/pnpm/store` hides a managed runtime):

```dockerfile
FROM ghcr.io/pnpm/pnpm:12 AS base
RUN pnpm runtime set node 24 -g
FROM base AS prod-deps
RUN --mount=type=cache,id=pnpm,target=/var/cache/pnpm \
    pnpm install --store-dir /var/cache/pnpm --prod --frozen-lockfile
```

A `build` stage runs full install plus `pnpm run build`; the final stage copies `node_modules` from prod-deps and `dist` from build. Use a `.dockerignore` with `node_modules`, `.git`, `dist`.

Monorepo, one image per app: build once (`pnpm run -r build`), then `pnpm deploy --filter=app1 --prod /prod/app1` per app and copy each into its own final stage (`docker build . --target app1`). The example workspace sets `injectWorkspacePackages: true` and `syncInjectedDepsAfterScripts: [build]`.

No cache mounts (ephemeral CI): copy only `pnpm-lock.yaml` and `pnpm-workspace.yaml` (plus patches and files named by `include`), run `pnpm fetch` (fills the virtual store, `pnpm fetch --prod` for production), copy sources, then `pnpm install --offline --frozen-lockfile`. The layer cache is lost only when the lockfile or settings change.

## Checked

2026-11-04. Confirmed against pnpm.io/docker: BuildKit cache mount recipes, separate store path caution, multi-stage example 1, monorepo deploy example 2 with its workspace settings, example 3 pnpm fetch and offline install. Removed: the generic closing Check line (not stated on the page).
Method: documentation only; no commands were run.
