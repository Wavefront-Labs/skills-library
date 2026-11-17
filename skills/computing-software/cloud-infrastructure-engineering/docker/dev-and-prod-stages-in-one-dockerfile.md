---
id: computing-software.cloud-infrastructure-engineering.docker.dev-and-prod-stages-in-one-dockerfile
name: dev-and-prod-stages-in-one-dockerfile
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, multi-stage, dev-prod-stages, build-target, compose-build, hot-reload, dockerfile]
level: practitioner
status: docs-checked
description: "Structure one Dockerfile with base, deps, dev, build and prod stages; target dev from Compose for hot reload and keep prod as the default last stage for CI."
sources: ["https://docs.docker.com/build/building/multi-stage/", "https://docs.docker.com/compose/how-tos/multiple-compose-files/merge/", "https://docs.docker.com/reference/compose-file/build/#target"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Dev and prod stages in one Dockerfile

One file, shared base, two endpoints. Dev gets tooling and dev dependencies; prod gets only
what runs. Keep prod **last** so a bare `docker build .` produces the shippable image (without
`--target` the build produces the last stage).

## Layout (Node example; same shape for other stacks)
```dockerfile
# syntax=docker/dockerfile:1
FROM node AS base
WORKDIR /app

FROM base AS deps
COPY package.json package-lock.json ./
RUN --mount=type=cache,target=/root/.npm npm ci --omit=dev

FROM base AS dev
ENV NODE_ENV=development
COPY package.json package-lock.json ./
RUN --mount=type=cache,target=/root/.npm npm ci
# source arrives via bind mount or Compose watch; CMD runs the watcher
CMD ["npm", "run", "dev"]

FROM dev AS build
COPY . .
RUN npm run build && npm test

FROM base AS prod
ENV NODE_ENV=production
COPY --from=deps  /app/node_modules ./node_modules
COPY --from=build /app/dist ./dist
CMD ["node", "dist/server.js"]
```

## Wiring
```yaml
# compose.yaml (prod defaults)
services:
  web:
    build: { context: ., target: prod }
```
```yaml
# compose.override.yaml (read automatically next to compose.yaml)
services:
  web:
    build: { target: dev }
    volumes: [".:/app"]
```
By default Compose reads `compose.yaml` and an optional `compose.override.yaml`, merging the
override over the base; with `-f` or `COMPOSE_FILE` you choose the files yourself.
CI: `docker build -t app:$SHA .` (last stage, prod) and `docker build --target build .` to run
only up to the build and test stage.

## Rules of thumb
- Build `prod` from `base` plus `COPY --from` of selected outputs, not from `dev`, so dev
  tooling does not end up in production.
- Run tests in a stage that has the source (`build`), not in `dev`, which expects a mount.
- Put dev-only settings in the stage (`ENV NODE_ENV=development`) rather than relying on runtime
  flags.
- With BuildKit only the stages the target depends on are built, so `--target dev` does not
  build `prod`.

## Gotchas
- When you bind-mount the source over `/app`, a host directory without `node_modules` hides the
  installed dependencies; mount the source narrowly or use Compose watch to sync files instead.
- Running with `-f compose.yaml` only skips the override file, so you get prod and no hot reload.
- Image size checks in CI should build the default (last) target, not `dev`.

## Verify
```bash
docker build -t app .                      # builds the last stage (prod)
docker build --target dev -t app:dev .
docker image ls app
```

## Checked

Checked 2026-10-23 against docker/docs "Multi-stage builds" (naming, `--target`, BuildKit versus legacy builder), the Compose "Merge" page (default `compose.yaml` plus `compose.override.yaml`) and the Compose build `target` reference.
Confirmed: last stage is the default output, `--target`, BuildKit builds only dependent stages, override file behaviour. Removed unconfirmed claims: the `USER node` image user, pinned Node image tag, the anonymous-volume recipe for `node_modules`, debug port mapping and the `ls node_modules | wc -l` check.

Method: documentation only; no commands were run.
