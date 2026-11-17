---
id: computing-software.ai-ml-engineering.mastra.request-context-dynamic-config
name: request-context-dynamic-config
category: computing-software
field: ai-ml-engineering
product: mastra
tags: [mastra, requestcontext, dynamic-instructions, middleware, reserved-keys, schema-validation, zod]
level: practitioner
status: docs-checked
description: "Pass per-request values through Mastra RequestContext to agents, tools and workflows: dynamic instructions, reserved keys, typing and requestContextSchema validation."
sources:
  - https://mastra.ai/docs/server/request-context
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: change agent, tool and workflow behaviour per request without touching memory.

`RequestContext` carries runtime values (user tier, locale, model choice). It is separate from memory, which persists conversation state.

## Set and read
```typescript
import { RequestContext } from '@mastra/core/request-context'
const requestContext = new RequestContext<{ 'user-tier': 'enterprise' | 'pro' }>()
requestContext.set('user-tier', 'enterprise')
await agent.generate("What's the weather in London?", { requestContext })
```
Also accepted by `agent.network()`, `run.start()`, `run.resume()` and `tool.execute(input, { requestContext })`.

With a type or `requestContextSchema`, `get/set/has/delete` accept only declared keys. Use `getRaw/setRaw/hasRaw/deleteRaw` for infrastructure keys (values are `unknown`; narrow before use).

Populate it in `server.middleware`: `context.get('requestContext').set(...)` then `await next()`.

Read it in agent options (`instructions`, `model`, `tools`, `memory`, also `agents`, `workflows`, `scorers`, processors) via `({ requestContext })`, in workflow `execute: async ({ requestContext })`, and in tools via `context?.requestContext?.get(...)`.

## Dynamic instructions
Make `instructions` an async function returning a string to personalise, localise, A/B test, or fetch prompts from a registry without redeploying.

## Reserved keys
Server-read keys from `@mastra/core/request-context`:
- `MASTRA_RESOURCE_ID_KEY`: forces the memory resource ID; the server returns 403 for threads it doesn't own. Easiest to set via `mapUserToResourceId: user => user.id` in auth config; clients may then omit `memory.resource`. Memory use with no resource ID gives a 400.
- `MASTRA_THREAD_ID_KEY`: forces the thread ID.
- `MASTRA_SCOPES_KEY`: array of `<type>:<value>` scopes. Server ownership checks read only the resource and thread keys, so set those too when pinning identity via scopes.
- `MASTRA_MESSAGE_AUTHOR_KEY`: `{ id, name?, avatarUrl? }` author of a user message.

The same applies to a `thread:` scope: only `MASTRA_THREAD_ID_KEY` drives the server's thread checks, so set it as well when pinning a thread. Scopes combine with per-call `scopes`; the agent's `scopes` list adds to them and a `scopes` function replaces them. A `resource:` or `thread:` scope conflicting with another resource or thread value returns 400. Request-context scopes need a `@mastra/server` release that reserves them; older servers make agents throw `AGENT_SCOPES_SERVER_OUTDATED`.

## Schema validation
Add `requestContextSchema` (Zod, Valibot, ArkType, ...); read all values with `requestContext.all`.

| Component | Checked | On failure |
| - | - | - |
| Agent | start of `generate()`/`stream()` | throws `MastraError` |
| Tool | before `execute()` | returns `{ error: true, message }` |
| Workflow | start of `run.start()` | throws `Error` |
| Step | before step `execute()` | step fails |

Mirror the fields your middleware sets; use `.optional()` for conditional ones; check tool error objects when the tool matters.

Studio: `mastra dev --request-context-presets ./presets.json` adds a preset dropdown to the request context editor; editing the JSON by hand switches it back to "Custom". Steps can also declare their own `requestContextSchema`.

## Checked
Confirmed 2026-11-08 against the Mastra request context docs page (fetched as markdown, read in full): setting values, raw methods, middleware, accessors, dynamic instructions, reserved keys, typing and schema validation. Added scope-combination rules and the outdated-server error. Nothing removed.
Method: docs-only read of cited pages, 2026-11-08
