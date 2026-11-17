---
id: computing-software.ai-ml-engineering.mastra.deploy-mastra-server
name: deploy-mastra-server
category: computing-software
field: ai-ml-engineering
product: mastra
tags: [mastra, deploy, build, monorepo, mastra-build, server, graceful-shutdown, bundler]
level: practitioner
status: docs-checked
description: "Build and run a standalone Mastra server with mastra build and mastra start, understand build output and build-time options, drain on shutdown, and deploy from monorepos."
sources:
  - https://mastra.ai/docs/deployment/mastra-server
  - https://mastra.ai/docs/deployment/monorepo
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: produce and run a self-contained Mastra server (Node.js, Bun or Deno), including from a monorepo. To embed Mastra in an existing Express/Hono app use Server Adapters instead.

## Build and run
```bash
mastra build          # creates .mastra/
mastra start          # or: node .mastra/output/index.mjs
```
`mastra start` also loads `.env.production` and `.env`, gives helpful messages for missing modules, and handles signals for graceful shutdown.

`.mastra/output/` is self-contained (copy it to any server): `index.mjs` (entry), `mastra.mjs` (bundled config), `tools.mjs` and `tools/`, `package.json`, `node_modules/`, `.npmrc` (if present), static assets from `src/mastra/public` merged into the root, `playground/` (Studio, only with `--studio`). `.mastra/.build/` holds intermediate artifacts.

Build steps: locate `index.ts|js`; discover `{mastraDir}/tools/**/*.{js,ts}` (not tests); decide bundle vs external deps; Rollup bundle with tree-shaking; generate a Hono server; run `npm install` in output; copy `public` and `.npmrc`.

## Build-time options
`bundler`, `deployer` and `server` are read at build time and must be direct properties of the object passed to `new Mastra()` (values may come from variables, imports or calls):
```typescript
export const mastra = new Mastra({ bundler: { externals: ['sharp'] }, server: { port: 4111 } })
```
`new Mastra(createMastraOptions())` and `new Mastra({ ...options })` prevent extraction; the default build behavior is then used.

## Gotchas
- Do not keep a SQLite database file in `src/mastra/public`: build copies it into output (overwriting same names), and `file:./mastra.db` resolves relative to the running directory, so changes are lost on the next build.
- `JavaScript heap out of memory` during build: `NODE_OPTIONS="--max-old-space-size=4096" mastra build`.

## Environment and endpoints
`PORT` (default 4111), `MASTRA_STUDIO_PATH` (default `./playground`), `MASTRA_SKIP_DOTENV`, `NODE_OPTIONS`. Endpoints: `GET /health` (200), `GET /api/openapi.json` (if `server.build.openAPIDocs`), `GET /swagger-ui` (if `server.build.swaggerUI`); run `mastra dev` and open `http://localhost:4111/swagger-ui` for the full list.

## Graceful shutdown
The server handles `SIGINT`/`SIGTERM`: stops accepting connections, waits up to `server.drainTimeout` (default 5 s) for requests and streams, then `mastra.shutdown()` gives in-flight workflow runs (including durable agent runs) the same window. HTTP and workflow drains run sequentially. A second signal terminates immediately. `server.handleShutdownSignals` lets you manage signals. Manual: `await mastra.shutdown({ drainTimeout: 30_000 })`; config: `server: { drainTimeout: 240_000 }`. A plain `agent.stream()` cannot resume after process exit; use durable agents (needs shared persistent run storage and idempotent tools; replay needs a shared cache such as Redis).

## Monorepo
Supported: npm, pnpm, Yarn workspaces, Turborepo. Bun workspaces partial/known issues. Nx needs `package.json` in workspace packages.
- The app package's script is `"build": "mastra build"`; run it with your tool: `npm run build --workspace=apps/api`, `pnpm --filter api run build`, `yarn workspace api build`, `turbo run build --filter=api`.
- Workspace packages: precompiled ones are imported as JS; uncompiled TypeScript is transpiled. If problems, `bundler: { transpilePackages: ['@my-org/utils'] }` (keep `bundler` a direct property). Prefer building the package first for faster builds.
- Keep `.env` in the app directory (e.g. `apps/api/.env`), not the repo root. Set the cloud deploy target to the app directory, not the monorepo root.
- Use a single root lockfile and align shared library versions.
- `mastra build` copies the lockfile into output and updates/installs (also in CI); without a lockfile it uses npm and generates `package-lock.json`. `MASTRA_BUILD_SKIP_INSTALL=1 mastra build` skips this (for hermetic systems like Bazel); you must then provide `node_modules` in the output.
- "Workspace package not found": check it is in dependencies, the lockfile is current, and its `package.json` has a valid `main` or `exports`.

## Checked

Date: 2026-11-07

Every cited page was read against the skill's claims. No claims removed. Large pages (agents/processors, workflows control-flow) were read only in the sections the skill covers; sections not covered by the skill were not read in full.

Method: documentation only; no commands were run.
