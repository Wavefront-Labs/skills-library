---
id: computing-software.ai-ml-engineering.mastra.define-tools-with-zod-schemas
name: define-tools-with-zod-schemas
category: computing-software
field: ai-ml-engineering
product: mastra
tags: [mastra, tool, createtool, zod, schema, inputschema, outputschema, agent]
level: practitioner
status: docs-checked
description: "Define Mastra tools with createTool and Standard JSON Schema input/output schemas, attach them to agents, and handle output validation failures."
sources:
  - https://mastra.ai/docs/agents/tools
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: write schema-validated Mastra tools and give them to an agent.

## createTool
Import `createTool` from `@mastra/core/tools`; define `id`, `description`, `inputSchema`, `outputSchema`, `execute`. `execute` has exactly one signature: `execute(inputData, context)`. The first argument is validated against `inputSchema` (destructure it directly); the runtime always supplies the second (`requestContext`, `tracingContext`, `abortSignal`, ...), which you may omit. Other shapes are outdated.
```typescript
import { createTool } from '@mastra/core/tools'
import { z } from 'zod'

export const weatherTool = createTool({
  id: 'weather-tool',
  description: 'Fetches weather for a location',
  inputSchema: z.object({ location: z.string() }),
  outputSchema: z.object({
    location: z.string(),
    temperatureCelsius: z.number(),
    conditions: z.string(),
  }),
  execute: async ({ location }, { abortSignal }) => {
    const response = await fetch(`https://wttr.in/${location}?format=j1`, { signal: abortSignal })
    const data = await response.json()
    return {
      location,
      temperatureCelsius: Number(data.current_condition[0].temp_C),
      conditions: data.current_condition[0].weatherDesc[0].value,
    }
  },
})
```
Keep descriptions concise and focused on the primary use case; descriptive schema names help the agent.

## Attach to an agent
Add to `tools: { weatherTool }` on the `Agent`, and mention the tools and their purpose in `instructions` so the agent knows when to call them. With several tools (`tools: { weatherTool, hazardsTool }`) the agent chooses using the user message, instructions, tool descriptions and schemas. Share a tool across agents by importing it in each.

## Schema libraries
Any library supporting Standard JSON Schema works: Zod, Valibot, ArkType. Valibot needs a wrapper: `toStandardJsonSchema(v.object({ location: v.string() }))` from `@valibot/to-json-schema`. ArkType: `type({ location: 'string' })`.

## Output validation failures
If a result does not match `outputSchema`, Mastra logs a warning and returns a validation error object instead of the result, so the model treats the call as failed and may retry. For tools whose side effects already happened (for example placing an order), set `outputValidation: 'warn'`: the mismatch is still logged but the real result is returned unchanged.

## Other options named on the page
- Key naming: the `toolName` in streams is the object key you used in `tools` (not the tool `id`); use `tools: { [weatherTool.id]: weatherTool }` to match the id.
- `toModelOutput` returns a smaller/multimodal representation to the model while the app keeps the full result.
- Without `execute` a tool is a client tool; the run ends with `finishReason: 'tool-calls'`.
- `hooks` (`beforeToolCall`, `afterToolCall`) on the agent or per `generate()`/`stream()` call; return `{ proceed: false, output }` from `beforeToolCall` to skip a call.
- `toolChoice` and `activeTools` on `generate()`/`stream()` control tool selection at runtime.
- To test: `npx mastra api tool execute weather-tool '{"location":"San Francisco"}'` against a running server (`npx mastra dev`, or `--url`).

Related: computing-software.ai-ml-engineering.mastra.require-tool-approval

## Checked

Date: 2026-11-07

Every cited page was read against the skill's claims. No claims removed. Large pages (agents/processors, workflows control-flow) were read only in the sections the skill covers; sections not covered by the skill were not read in full.

Method: documentation only; no commands were run.
