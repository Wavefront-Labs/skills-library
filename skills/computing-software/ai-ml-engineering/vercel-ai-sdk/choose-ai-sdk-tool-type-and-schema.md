---
id: computing-software.ai-ml-engineering.vercel-ai-sdk.choose-ai-sdk-tool-type-and-schema
name: choose-ai-sdk-tool-type-and-schema
category: computing-software
field: ai-ml-engineering
product: vercel-ai-sdk
tags: [tools-foundations, function-tools, dynamic-tools, provider-executed-tools, schemas, refine-tool-input]
level: practitioner
status: docs-checked
description: "Decide between function, dynamic, provider-defined and provider-executed tools, pick a schema library, and normalise tool inputs across providers."
sources:
  - https://ai-sdk.dev/docs/foundations/tools
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: choose the right kind of tool for a capability and define its schema correctly.

## A tool has three properties
- `description` (optional): influences when the model picks the tool; for function and dynamic tools it can be a string or a function deriving it from tool context and the experimental sandbox.
- `inputSchema`: Zod schema or JSON schema; consumed by the model and used to validate calls.
- `execute` (optional): async function called with the arguments. Tools with `execute` run automatically; feed results back with multi-step calls (`stopWhen`).

## The four types
| Type | Who defines schema | Who executes | Use when |
|---|---|---|---|
| Function tool (`tool({...})`) | you | your code | full control, provider portability |
| Dynamic tool (`dynamicTool({...})`) | runtime | your code | types unknown at dev time (MCP, user-defined, DB); `execute` input is `unknown` |
| Provider-defined tool | provider | your `execute` | model trained on it, e.g. `anthropic.tools.bash_20250124({ execute })` |
| Provider-executed tool | provider | provider servers | e.g. `openai.tools.webSearch()`, no infrastructure |

```ts
import { tool } from 'ai';
import { z } from 'zod';
const weatherTool = tool({
  description: 'Get the weather in a location',
  inputSchema: z.object({ location: z.string().describe('The location to get the weather for') }),
  execute: async ({ location }) => ({ temperature: 72, conditions: 'sunny' }),
});
```

## Schema options
Zod v3 and v4 (directly or `zodSchema()`), Valibot via `valibotSchema()` from `@ai-sdk/valibot`, Standard JSON Schema compatible schemas, and raw JSON schema via `jsonSchema()`. The same schemas drive structured output through the `output` setting.

## Normalise provider differences
Different providers may produce `null` for an optional field where another gives an empty string. For tools you do not own, use `experimental_refineToolInput`, a map keyed by tool name, typed per tool and returning the same shape:
```ts
experimental_refineToolInput: {
  search: input => ({ ...input, category: input.category === '' ? null : input.category }),
}
```
It runs before execution and before the input appears in outputs, lifecycle callbacks and telemetry.

## Packaging
Tools are plain objects: export them from an npm package and pass them in `tools: { webSearch: searchTool }` with `stopWhen: isStepCount(10)`.

## Gotchas
- Provider-defined and provider-executed tools are documented on each provider page.
- `experimental_refineToolInput` is documented as experimental.

## Checked

Date: 2026-11-07. Read the 1 cited page(s) in full from the vercel/ai docs source and confirmed the commands, parameters, defaults and error strings above. Narrowed the "experimental_ options may change" line to experimental_refineToolInput.

Method: documentation only; no commands were run.
