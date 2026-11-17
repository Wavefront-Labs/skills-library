---
id: computing-software.ai-ml-engineering.mastra.use-server-adapters
name: use-server-adapters
category: computing-software
field: ai-ml-engineering
product: mastra
tags: [mastra, server-adapters, adapter, hono, express, fastify, route-auth, openapi]
level: advanced
status: docs-checked
description: "Run Mastra inside Express, Hono, Fastify, Koa, NestJS, Elysia or Next.js with MastraServer: init flow, workers, prefixes, OpenAPI, redaction and per-route auth."
sources:
  - https://mastra.ai/docs/server/server-adapters
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: embed Mastra's endpoints in your own HTTP server instead of the Hono server from `mastra build`.

## Install and wire
Packages: `@mastra/elysia` (+ `elysia`), `@mastra/express`, `@mastra/hono`, `@mastra/fastify`, `@mastra/koa`, `@mastra/nestjs`, `@mastra/next` (+ `hono`), `@mastra/tanstack-start` (+ `hono`). Install with `npm install @mastra/<adapter>@latest`.

```typescript
const app = express()
app.use(express.json())
const server = new MastraServer({ app, mastra })
await server.init()
app.listen(4111)
```
NestJS uses `MastraModule.register({ mastra })` in `imports`. Koa needs `bodyParser()` before the server.

Adapters use the `mastra` instance you pass and do no file-based discovery; register agents in code.

## What `init()` does (in order)
1. `registerContextMiddleware()`: attaches Mastra, request context, tools and abort signal to each request.
2. `registerAuthMiddleware()`: auth hook; raw framework routes needing Mastra auth should use the adapter's exported `createAuthMiddleware()`.
3. `registerUserMiddleware()`: `server.middleware` and `setServerMiddleware()`; only Hono-based adapters run them, others log a warning.
4. `registerRoutes()`: all API routes, plus MCP routes if MCP servers exist.

Call these separately for custom ordering. Routes added before `init()` lack Mastra context; after it they have it. Prefer `registerApiRoute()` for Mastra-managed auth.

## Background workers
`init()` does not start workers. Call `mastra.startWorkers()` once after listening (idempotent) or scheduled workflows, agent schedules and event listeners never run. On shutdown call `mastra.shutdown()` (drain bounded by `drainTimeout`, default 5 seconds). Skip `startWorkers()` in the API process if workers run in a separate process.

## MastraServer options (constructor only)
- `prefix: '/api/v2'` changes the route prefix from `/api/...`; custom routes are unaffected.
- `openapiPath: '/openapi.json'` serves a spec generated from route Zod schemas.
- `streamOptions: { redact: true }` is the default; `false` only for internal services or debugging.
- `customRouteAuthConfig`: a `Map` of `METHOD:PATH` (GET/POST/PUT/DELETE/ALL, `*` wildcards) to `false` (public) or `true` (auth required).
- `bodyLimitOptions`, `mcpOptions` (e.g. `serverless: true` for stateless MCP; `setRequestAuth`).

## Config from `server` vs adapter
Adapters read `auth`, `apiRoutes` (custom `registerApiRoute()` routes, added to the OpenAPI spec when `openapiPath` is set; the constructor's `customApiRoutes` overrides the list), `bodySizeLimit` (overridable per adapter with `bodyLimitOptions`), `onError` and `middleware` from the Mastra `server` config. `port`, `host`, `cors` and `timeout` only apply to `mastra dev` or `mastra build`; configure them in your framework instead (for example CORS middleware and the framework's listen call). `server.getApp()` or `mastra.getServerApp()` returns the same framework app.

## MCP and streaming
When MCP servers are configured, `registerRoutes()` exposes each at `/api/mcp/:serverId/mcp` over Streamable HTTP; session state is kept by default. Redaction of stream chunks hides system prompts, tool definitions, credentials in request bodies and internal config at the HTTP boundary only; callbacks such as `onStepFinish` still see full data. Pass `mcpOptions.setRequestAuth` (in the adapter constructor, or `server.mcpOptions` with the deployer) to control how the authenticated principal reaches tools. For Studio with an adapter, run `mastra studio` to launch only the UI.

## Checked
Confirmed 2026-11-08 against the Mastra server adapters docs page (fetched as markdown, read in full): packages, init flow, manual initialization, workers, custom routes, prefixes, OpenAPI, redaction, route auth, app access, config split and MCP. Corrected one claim: the draft listed `apiRoutes` among options that only apply to `mastra build`, but the page says adapters read it. Added MCP and streaming details.
Method: docs-only read of cited pages, 2026-11-08
