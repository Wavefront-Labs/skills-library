---
id: computing-software.ai-ml-engineering.vercel-ai-sdk.use-mcp-resources-prompts-completions-and-elicitation
name: use-mcp-resources-prompts-completions-and-elicitation
category: computing-software
field: ai-ml-engineering
product: vercel-ai-sdk
tags: [mcp-tools, mcp-resources, mcp-prompts, elicitation, completions]
level: advanced
status: docs-checked
description: "Read MCP resources and prompts, request argument completions, and answer server elicitation requests with onElicitationRequest and accept, decline or cancel."
sources:
  - https://ai-sdk.dev/docs/ai-sdk-core/mcp-tools
  - https://ai-sdk.dev/docs/reference/ai-sdk-core/create-mcp-client
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: use the non-tool parts of an MCP server through `createMCPClient`.

## Resources (application-driven)
Your app decides when to fetch them and pass as context.
```ts
const resources = await mcpClient.listResources();
const data = await mcpClient.readResource({ uri: 'file:///example/document.txt' });
const templates = await mcpClient.listResourceTemplates();
```
`listResources` accepts `{ params (cursor), options (signal, timeout) }`.

## Prompts (user-controlled templates)
```ts
const prompts = await mcpClient.listPrompts();
const prompt = await mcpClient.getPrompt({ name: 'code_review', arguments: { code: 'function add(a, b) { return a + b; }' } });
```

## Completions
Requires the server's `completions` capability, else `MCPClientError`.
```ts
const completion = await mcpClient.complete({
  ref: { type: 'ref/resource', uri: 'kubernetes://namespaced/{plural}/{namespace}' }, // or { type: 'ref/prompt', name }
  argument: { name: 'namespace', value: 'auth' },
  context: { arguments: { plural: 'deployments' } },   // already-resolved values
});
console.log(completion.completion.values);
```

## Elicitation (server asks for more input mid-run)
1. Advertise it: `createMCPClient({ transport, capabilities: { elicitation: {} } })`.
2. Register a handler:
```ts
import { ElicitationRequestSchema } from '@ai-sdk/mcp';
mcpClient.onElicitationRequest(ElicitationRequestSchema, async request => {
  const userInput = await getInputFromUser(request.params.message, request.params.requestedSchema);
  return { action: 'accept', content: userInput }; // 'decline' | 'cancel'; content only for accept
});
```
Actions: `accept` (must include `content`), `decline`, `cancel`. Your application is responsible for handling requests; the client only surfaces them.

On MCP `2026-07-28` connections the same handler answers form elicitation embedded in `input_required` results from tools, prompts and resource reads. The client retries the original request with the answers and the unchanged `requestState`, up to 10 retries; state-only retries are delayed 250 ms; each round respects `timeout` (including time awaiting the handler) and `maxTotalTimeout` bounds the whole exchange. Missing handlers or unsupported input requests reject the operation. Older connections use `elicitation/create` server requests.

## Gotchas
- On MCP `2026-07-28` connections, time spent awaiting the handler counts against `timeout`.
- The experimental events API (`client.experimental_events`) is separate from these methods.

## Checked

Date: 2026-11-07. Read the 2 cited page(s) in full from the vercel/ai docs source and confirmed the commands, parameters, defaults and error strings above. Scoped the timeout gotcha to MCP 2026-07-28 connections, as the page states.

Method: documentation only; no commands were run.
