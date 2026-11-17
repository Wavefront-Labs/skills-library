---
id: computing-software.ai-ml-engineering.vercel-ai-sdk.improve-tool-and-schema-prompts-and-debug-requests
name: improve-tool-and-schema-prompts-and-debug-requests
category: computing-software
field: ai-ml-engineering
product: vercel-ai-sdk
tags: [prompt-engineering, zod-schema, nullable, warnings, request-body]
level: practitioner
status: docs-checked
description: "Make tool and structured-output prompts reliable with simpler Zod schemas, nullable optionals and date handling, then debug with warnings and request messages."
sources:
  - https://ai-sdk.dev/docs/ai-sdk-core/prompt-engineering
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: get models to call tools and fill schemas correctly, and see exactly what was sent when they do not.

## Tool prompt tips
1. Use a model that is strong at tool calling; weaker ones often fail to call tools flawlessly.
2. Keep tools few (the docs suggest 5 or fewer).
3. Keep parameter schemas simple; many nested or optional elements and unions are hard for models.
4. Use meaningful names for tools, parameters and properties.
5. Add `.describe('...')` to Zod properties as hints.
6. When a tool's output is unclear and tools depend on each other, say what it returns in the tool `description`.
7. Put JSON example inputs and outputs in the prompt, since tools work on JSON objects.

## Schema fixes
Dates: models return strings, Zod expects `Date`. Validate the string and transform:
```ts
output: Output.object({ schema: z.object({ events: z.array(z.object({
  event: z.string(),
  date: z.string().date().transform(value => new Date(value)),
})) }) })
```
(`z.string().datetime()` also works.)

Optional parameters can break providers with strict schema validation, notably OpenAI structured outputs in strict mode. Use `.nullable()` instead of `.optional()`:
```ts
inputSchema: z.object({ command: z.string(), workdir: z.string().nullable(), timeout: z.string().nullable() })
```

Temperature: for tool calls and object generation the docs recommend `temperature: 0` for consistent formats, precise parameters and strict schemas.

## Debug
```ts
const result = await generateText({ model, prompt: 'Hello, world!', include: { requestMessages: true } });
console.log(result.warnings);                       // unsupported features or settings
console.log(result.finalStep.request.messages);     // needs include.requestMessages: true
console.log(result.finalStep.request.body);         // raw HTTP body, for models that expose it
```
Providers either throw or return warnings for unsupported features, so check `warnings` first.

## Gotchas
- `request.messages` covers the final step only, and is absent unless `include.requestMessages` is true.
- Request bodies are only available for providers that expose them (OpenAI is the docs example).

## Checked

Date: 2026-11-07. Read the 1 cited page(s) in full from the vercel/ai docs source and confirmed the commands, parameters, defaults and error strings above. Removed the invented Verify section and the nullable-field execute gotcha.

Method: documentation only; no commands were run.
