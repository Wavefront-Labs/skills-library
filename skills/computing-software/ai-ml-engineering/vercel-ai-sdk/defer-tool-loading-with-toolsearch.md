---
id: computing-software.ai-ml-engineering.vercel-ai-sdk.defer-tool-loading-with-toolsearch
name: defer-tool-loading-with-toolsearch
category: computing-software
field: ai-ml-engineering
product: vercel-ai-sdk
tags: [tool-search, defer-loading, max-results, code-mode, mcp-tools]
level: advanced
status: docs-checked
description: "Hide large tool sets behind toolSearch with deferLoading, tune maxResults, supply a custom search callback, and combine with code mode to keep caches."
sources:
  - https://ai-sdk.dev/docs/ai-sdk-core/tool-search
  - https://ai-sdk.dev/docs/ai-sdk-core/code-mode
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: stop sending every tool definition up front; the model searches and gets matching tools on the next step.

## Direct calling
Mark tools `deferLoading: true` and add `toolSearch()`:
```ts
import { generateText, isStepCount, tool, toolSearch } from 'ai';
const weather = tool({
  deferLoading: true,
  description: 'Get the weather forecast for a city.',
  inputSchema: z.object({ city: z.string() }),
  execute: async ({ city }) => ({ city, forecast: 'Rain tomorrow.' }),
});
await generateText({
  model, tools: { search: toolSearch(), weather },
  stopWhen: isStepCount(5), prompt: 'Will it rain in Bangalore tomorrow?',
});
```
The model initially sees only `search`. Matches are added to the provider tool list for the next step, which changes the definitions and can invalidate the cached prompt prefix. Works with `generateText`, `streamText`, `ToolLoopAgent` and `WorkflowAgent` (`@ai-sdk/workflow`, direct calling only).

## Code mode, cache preserving
```ts
tools: { code: codeModeTool({ toolDiscovery: 'conversation' }), search: toolSearch(), weather },
experimental_toolCallers: { search: ['code'], weather: ['code'] },
```
The model runs `tools.search({ query: 'weather forecast' })`, then on the next step gets the updated catalog in a user message and can call `tools.weather(...)`. The provider-visible code tool stays unchanged. Actual cache reuse depends on the provider.

## Tuning
- `toolSearch({ maxResults: 10 })`: default is five loaded per search; must be a positive safe integer. It does not change matching or ranking and adds more definitions to context.
- Custom ranking: `toolSearch({ search: ({ query, tools }) => [...names] })`. It receives the query and the eligible deferred tool names and resolved descriptions, returns ranked names, and may be async. The SDK drops unknown names and duplicates, then keeps the first `maxResults`.
- MCP: add `deferLoading: true` to the tools returned by `client.tools()`.

## Gotchas
- Discovery always takes effect on the next model step, so allow enough steps in `stopWhen`.
- Search respects `activeTools` and caller routing; excluded tools stay unavailable.
- Discovered tools stay available for the rest of the generation.
- Without a `search` callback, default keyword matching on names and descriptions applies.

## Checked

Date: 2026-11-07. Read the 2 cited page(s) in full from the vercel/ai docs source and confirmed the commands, parameters, defaults and error strings above. No content change needed.

Method: documentation only; no commands were run.
