---
id: computing-software.ai-ml-engineering.mastra.call-mastra-with-client-sdk
name: call-mastra-with-client-sdk
category: computing-software
field: ai-ml-engineering
product: mastra
tags: [mastra, mastraclient, client-js, generate, stream, abort, client-tools, credentials]
level: practitioner
status: docs-checked
description: "Call a Mastra server with @mastra/client-js: init MastraClient, generate, stream, retries, cookies, abort signals, client-side tools and dynamic workflows."
sources:
  - https://mastra.ai/docs/server/mastra-client
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: call agents, workflows and tools on a Mastra server from browser or server code.

Prerequisites: Node.js v22.13.0 or later, TypeScript 4.7+, local Mastra server (typically port 4111). The SDK uses native `fetch`.

```bash
npm install @mastra/client-js@latest
```
```typescript
import { MastraClient } from '@mastra/client-js'
export const mastraClient = new MastraClient({
  baseUrl: process.env.MASTRA_API_URL || 'http://localhost:4111',
})
```

## Calls
```typescript
const agent = mastraClient.getAgent('testAgent')
const response = await agent.generate('Hello') // response.text
const stream = await agent.stream('Hello')
stream.processDataStream({ onTextPart: text => console.log(text) })
```
Both also accept an array of `{ role, content }` messages. In a server route, return `new Response(stream.body)`.

## Options
- `retries`, `backoffMs`, `maxBackoffMs`, `headers` control retry behaviour and diagnostic metadata.
- Cross-origin session cookies: set `credentials: 'include'`, otherwise expect `401`s even after login. The server needs a concrete `Access-Control-Allow-Origin` (not `*`) and `Access-Control-Allow-Credentials: true`. `@mastra/react`'s `MastraReactProvider` defaults to `credentials: 'include'`.
- Cancellation: pass `abortSignal: controller.signal` to the constructor; `controller.abort()` cancels in-flight requests.

## Client tools
Create tools in the browser with `createTool` from `@mastra/client-js` (id, description, `inputSchema`, `outputSchema`, `execute`) and pass them as `agent.generate(prompt, { clientTools: { colorChangeTool } })`. Tools then run in the user's environment (DOM, local storage) rather than on the server.

## Dynamic workflows
`client.upsertDynamicWorkflow(definition)` creates or replaces a persisted workflow (same `id` replaces). Then `client.getDynamicWorkflow(id).details()`; run via `client.getWorkflow(id).createRun()` and `run.startAsync({ inputData })`; delete with `.delete()`; `listDynamicWorkflows()` lists them.
- Needs a storage adapter supporting the `workflowDefinitions` domain to survive restarts.
- Definitions are declarative only (no closures); referenced agents, tools and nested workflows must already be registered.
- Authenticated servers need `stored-workflows:read` or `stored-workflows:write` for definitions and `workflows:execute` to run.

## Checked

Date: 2026-11-07

Every cited page was read against the skill's claims. No claims removed. Large pages (agents/processors, workflows control-flow) were read only in the sections the skill covers; sections not covered by the skill were not read in full.

Method: documentation only; no commands were run.
