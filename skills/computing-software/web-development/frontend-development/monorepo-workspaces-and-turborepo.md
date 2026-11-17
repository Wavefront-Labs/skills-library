---
id: computing-software.web-development.frontend-development.monorepo-workspaces-and-turborepo
name: monorepo-workspaces-and-turborepo
category: computing-software
field: web-development
product: frontend-development
tags: [build-tooling, pnpm-workspaces, turborepo, monorepo, npm-workspaces, nx]
level: practitioner
status: verified
description: "Setting up a JavaScript monorepo with pnpm/npm workspaces and Turborepo: workspace protocol, internal packages, task pipelines, caching, and filtered CI runs."
sources:
  - https://pnpm.io/workspaces
  - https://docs.npmjs.com/cli/using-npm/workspaces
  - https://turborepo.com/docs
  - https://turborepo.com/docs/crafting-your-repository/caching
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Monorepo workspaces and Turborepo

## 1. Layout
```
apps/web  apps/admin  packages/ui  packages/config-eslint  packages/tsconfig
pnpm-workspace.yaml   turbo.json   package.json (private: true)
```
```yaml
# pnpm-workspace.yaml
packages: ["apps/*", "packages/*"]
```
Internal dependency: `"@acme/ui": "workspace:*"` (pnpm/yarn/bun; npm uses `"*"` with workspaces). On publish, pnpm rewrites `workspace:` to real versions.

## 2. Internal packages
- "Just-in-time" packages: export TS source (`"exports": { ".": "./src/index.ts" }`) and let the app bundler compile it - no build step, but every consumer must transpile it (Next.js `transpilePackages: ["@acme/ui"]`).
- Compiled packages: build with tsup/tsc to `dist`, export types - required if published or consumed by Node directly.
- Declare every dependency in the package that imports it. pnpm's strict `node_modules` catches phantom dependencies npm hoisting hides.

## 3. Turborepo pipeline
```json
{ "$schema": "https://turborepo.com/schema.json",
  "tasks": {
    "build": { "dependsOn": ["^build"], "outputs": ["dist/**", ".next/**", "!.next/cache/**"] },
    "lint": {},
    "test": { "dependsOn": ["^build"], "outputs": ["coverage/**"] },
    "dev": { "cache": false, "persistent": true } } }
```
- `^build` = build dependencies first. Caching hashes inputs (files, lockfile, declared `env`). Turborepo 2 defaults to strict env mode (`"envMode": "strict"` in `--dry=json`): in a test an undeclared `FOO` was `undefined` inside the task, so undeclared vars cannot change output but also do not reach the build. List needed vars in `env`/`globalEnv` (they are then hashed and passed); `--env-mode=loose` passes the whole environment through, so undeclared vars can reach the build (confirm hashing behaviour in the Turborepo env docs).
- Remote cache (`turbo login && turbo link` or self-hosted) shares results across CI and laptops.
- CI on changed packages: `turbo run build test --filter=...[origin/main]`; pnpm alone: `pnpm -r --filter "...[origin/main]" test`.

## 4. Commands
`pnpm add react --filter @acme/web`, `pnpm -w add -D turbo` (root), `pnpm --filter @acme/ui build`, `pnpm -r exec ...`.

## 5. Pitfalls
- Multiple React copies (hooks errors) - keep versions aligned (`pnpm dedupe`, `catalog:` in pnpm-workspace.yaml for shared versions).
- Docker builds: `turbo prune @acme/web --docker` to copy only needed packages and keep layer caching.
- TS project references or path aliases must match package exports or the IDE and build disagree.

## Verify
`turbo run build --dry=json` shows the graph; a repeat `turbo run build` reports `>>> FULL TURBO` cache hits (without git, files like `out/` or fresh `dist/` change the hash, so the first repeat can still miss). `turbo` shells out to the package manager: it fails with "Unable to find package manager binary" if `pnpm` is not on PATH.
