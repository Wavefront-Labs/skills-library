---
id: computing-software.web-development.node-express.dockerising-node-apps
name: dockerising-node-apps
category: computing-software
field: web-development
product: node-express
tags: [node-dockerfile, docker, multi-stage-builds, non-root-containers, node-env]
level: practitioner
status: docs-checked
description: "Dockerising Node.js apps: multi-stage builds, npm ci with cache mounts, NODE_ENV, non-root user, signals and PID 1, health checks and .dockerignore."
sources:
  - https://docs.docker.com/guides/nodejs/
  - https://github.com/nodejs/docker-node/blob/main/docs/BestPractices.md
  - https://docs.docker.com/build/building/best-practices/
  - https://docs.docker.com/build/building/variables/
  - https://docs.docker.com/build/cache/optimize/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dockerising Node apps

## 1. Multi-stage Dockerfile
```dockerfile
# syntax=docker/dockerfile:1
ARG NODE_VERSION=22
FROM node:${NODE_VERSION}-slim AS base
WORKDIR /app

FROM base AS deps
COPY package.json package-lock.json ./
RUN --mount=type=cache,target=/root/.npm npm ci

FROM deps AS build
COPY . .
RUN npm run build && npm prune --omit=dev

FROM base AS runtime
ENV NODE_ENV=production
COPY --from=build --chown=node:node /app/node_modules ./node_modules
COPY --from=build --chown=node:node /app/dist ./dist
COPY --chown=node:node package.json ./
USER node
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=3s CMD node -e "fetch('http://127.0.0.1:3000/healthz').then(r=>process.exit(r.ok?0:1)).catch(()=>process.exit(1))"
CMD ["node", "dist/server.js"]
```
- Copy lockfiles first so dependency layers cache across code changes.
- `npm ci` (not `npm install`) for reproducible installs; pnpm: `corepack enable && pnpm install --frozen-lockfile`.
- Run with `NODE_ENV=production` (docker-node best practices); set it in the runtime stage, not during the build if build tools are devDependencies.
- Alpine-based images need extra packages to build native modules with node-gyp; read the node-gyp alpine section of the docker-node best practices before choosing Alpine.

## 2. PID 1 and signals
- Use exec-form `CMD ["node", ...]`, not `npm start` (npm swallows exit signals such as SIGTERM and SIGINT, and adds a process).
- Handle SIGTERM: stop accepting connections, finish in-flight requests, close DB pools, exit:
```js
process.on("SIGTERM", () => { server.close(() => pool.end().then(() => process.exit(0))); setTimeout(() => process.exit(1), 10_000).unref(); });
```
- `docker run --init` wraps Node in tini, because Node was not designed to run as PID 1.

## 3. .dockerignore
```
node_modules
.git
.env*
dist
coverage
*.log
```
Keeps secrets and host `node_modules` (wrong platform binaries) out of the build context.

## 4. Runtime settings
- Memory: limit the container's memory (`-m` on `docker run`).
- Log to stdout as JSON; no log files in the container.
- Secrets via environment/secret mounts at runtime, never `ARG`/`ENV` (Docker documents build arguments and environment variables as inappropriate for secrets).
- Scan images (`docker scout cves`) and rebuild regularly for base image patches.

## Verify
- [ ] Image runs as non-root (`docker run --rm img id`); SIGTERM triggers graceful shutdown within the timeout; no devDependencies or secrets in the final image; rebuild after a code change reuses the dependency layer.

## Checked

2026-10-25 against the docker-node best practices (nodejs/docker-node main), the Docker docs (docker/docs, 2026-10) and the BuildKit Dockerfile reference. Confirmed: docker-node: run with NODE_ENV=production, Node as PID 1 ignores SIGINT so use --init (tini), CMD in exec form avoids npm swallowing SIGTERM and SIGINT, non-root node user, memory limits with -m; Docker docs: --mount=type=cache in the cache optimisation guide, docker scout cves, build arguments and environment variables are inappropriate for secrets; HEALTHCHECK instruction exists in the Dockerfile reference.

Method: documentation only; no commands were run.
