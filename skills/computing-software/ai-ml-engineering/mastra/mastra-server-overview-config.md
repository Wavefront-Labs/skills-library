---
id: computing-software.ai-ml-engineering.mastra.mastra-server-overview-config
name: mastra-server-overview-config
category: computing-software
field: ai-ml-engineering
product: mastra
tags: [mastra, server, rest, openai, responses-api, redaction, hono, openapi]
level: practitioner
status: docs-checked
description: "Configure the Mastra HTTP server: port/host, REST and OpenAPI/Swagger endpoints, the experimental Responses API, stream redaction and the required tsconfig."
sources:
  - https://mastra.ai/docs/server/overview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: set up and understand the Mastra server that exposes agents and workflows over HTTP.

## Configure
Pass a `server` object to the `Mastra` constructor (this covers those options; running your own HTTP server is the server-adapters topic).

```typescript
import { Mastra } from '@mastra/core'

export const mastra = new Mastra({
  server: {
    port: 3000, // Defaults to PORT env var or 4111
    host: '0.0.0.0', // Defaults to MASTRA_HOST env var or 'localhost'
  },
})
```

Mastra uses Hono underneath. `mastra build` generates a Hono-based server in the `.mastra` directory with endpoints for all registered agents and workflows, custom routes and middleware, auth, request context and stream data redaction.

## REST API explorer
- OpenAPI spec: `http://localhost:4111/api/openapi.json`
- Swagger UI: `http://localhost:4111/swagger-ui`
- Both are disabled in production by default; set `server.build.openAPIDocs` and `server.build.swaggerUI` to `true` to enable them.

## OpenAI Responses API (experimental)
Mastra exposes OpenAI-compatible Responses and Conversations routes backed by Mastra agents, memory and storage (not a raw provider proxy).
- `agent_id` selects the agent; follow-up turns use `previous_response_id`; threads use `conversation_id`.
- `model` overrides the agent's model for one request; omit it to use the agent's own.
- Supported: streaming, function calling (tools), `providerOptions` passthrough, JSON output via `text.format`.

## Stream data redaction
Streaming responses have system prompts, tool definitions, API keys and similar data redacted per chunk. On by default; it is configurable only through server adapters.

## TypeScript
Use `module`/`moduleResolution` compatible with modern Node.js (`CommonJS` and `node` are unsupported). The page's tsconfig uses `target: ES2022`, `module: ES2022`, `moduleResolution: bundler`, `strict: true`, `types: ["node"]` (needs `@types/node`, included by `create-mastra`).

## Checked

Date: 2026-11-07

Every cited page was read against the skill's claims. No claims removed. Large pages (agents/processors, workflows control-flow) were read only in the sections the skill covers; sections not covered by the skill were not read in full.

Method: documentation only; no commands were run.
