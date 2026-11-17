---
id: computing-software.ai-ml-engineering.vercel-ai-sdk.pass-runtime-and-tool-context-with-contextschema
name: pass-runtime-and-tool-context-with-contextschema
category: computing-software
field: ai-ml-engineering
product: vercel-ai-sdk
tags: [runtime-and-tool-context, runtime-context, tools-context, context-schema, telemetry]
level: advanced
status: docs-checked
description: "Pass server-side state with runtimeContext and per-tool toolsContext validated by contextSchema, and limit what telemetry sees with includeRuntimeContext."
sources:
  - https://ai-sdk.dev/docs/ai-sdk-core/runtime-and-tool-context
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: give a generation or agent loop server-side state (tenant, keys, flags) without putting it in the prompt.

## Pick the right context
- `runtimeContext`: shared state for the whole generation or `ToolLoopAgent` loop. Set on `generateText` / `streamText` or in agent settings or `prepareCall`. Read in `prepareStep`, lifecycle callbacks, step results and telemetry. It is not added to the model prompt.
- `toolsContext`: a map keyed by tool name. Each entry is validated against that tool's `contextSchema` and handed to the tool as `context`.
- Prompt messages: use these for anything the model should reason about or mention.

## Runtime context
```ts
const result = await generateText({
  model,
  prompt: 'Help the user plan their trip.',
  runtimeContext: { tenantId: 'tenant_123', plan: 'enterprise', requestId: 'req_abc' },
  prepareStep: async ({ runtimeContext }) =>
    runtimeContext.plan === 'enterprise' ? { temperature: 0.2 } : {},
});
```
`prepareStep` may return a new `runtimeContext`; it applies to the current and all later steps, so use it to update agent state between turns.

## Tool context
```ts
const weatherTool = tool({
  description: 'Get the weather in a location',
  inputSchema: z.object({ location: z.string() }),
  contextSchema: z.object({ weatherApiKey: z.string(), defaultUnit: z.enum(['celsius', 'fahrenheit']) }),
  execute: async ({ location }, { context }) =>
    fetchWeather({ location, apiKey: context.weatherApiKey, unit: context.defaultUnit }),
});
await generateText({
  model, tools: { weather: weatherTool },
  toolsContext: { weather: { weatherApiKey: process.env.WEATHER_API_KEY!, defaultUnit: 'fahrenheit' } },
  prompt: 'What is the weather in San Francisco?',
});
```
A tool sees only its own context, never the full map. Tool description functions get the same typed `context` before each model call, so descriptions can vary with it. Treat tool context as immutable inside tools; to change it between steps, inspect the previous step in `prepareStep` and return an updated `toolsContext`. For `ToolLoopAgent`, set context in the constructor, or use `callOptionsSchema` plus `prepareCall` for per-invocation values.

## Filter telemetry
```ts
new ToolLoopAgent({
  model, tools: { customerLookup },
  runtimeContext: { requestId: 'req_abc', tenantId: 'tenant_123' },
  toolsContext: { customerLookup: { apiKey: process.env.CUSTOMER_API_KEY!, region: 'us' } },
  telemetry: {
    includeRuntimeContext: { requestId: true },
    includeToolsContext: { customerLookup: { region: true } },
  },
});
```
Telemetry then receives only `requestId` and the `region` entry.

## Gotchas
- Filtering is shallow (top-level properties only); if the option is omitted, no context properties are sent.
- Filters affect telemetry only. Tool execution, callbacks and results still get full values.
- When any tool declares `contextSchema`, `toolsContext` is required for the tools that need it.
- Filters reduce telemetry exposure; the docs say they are not a general security boundary.
- `execute` and tool description functions do not receive `runtimeContext` directly.

## Checked

Date: 2026-11-07. Read the 1 cited page(s) in full from the vercel/ai docs source and confirmed the commands, parameters, defaults and error strings above. Removed the invented Verify section.

Method: documentation only; no commands were run.
