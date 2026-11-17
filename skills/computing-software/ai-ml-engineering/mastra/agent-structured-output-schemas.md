---
id: computing-software.ai-ml-engineering.mastra.agent-structured-output-schemas
name: agent-structured-output-schemas
category: computing-software
field: ai-ml-engineering
product: mastra
tags: [mastra, structuredoutput, schema, zod, json-schema, agent, generate, stream]
level: practitioner
status: docs-checked
description: "Make Mastra agents return typed objects with structuredOutput schemas, read response.object, stream results, and set an error strategy."
sources:
  - https://mastra.ai/docs/agents/structured-output
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: get a validated object from an agent instead of text.

## Define the schema
Pass `structuredOutput: { schema }` to `generate()`. Schema may be Standard JSON Schema (Zod, Valibot via `toStandardJsonSchema`, ArkType) or plain JSON Schema. Zod is recommended for type inference and runtime validation.
```typescript
import { z } from 'zod'

const response = await testAgent.generate('Help me plan my day.', {
  structuredOutput: {
    schema: z.array(z.object({ name: z.string(), activities: z.array(z.string()) })),
  },
})
console.log(response.object)
```
JSON Schema form: `schema: { type: 'array', items: { type: 'object', properties: {...}, required: [...] } }`.

## Read the result
`response.object` holds the parsed, schema-validated value; do not parse it yourself. Exception: with `errorStrategy: 'fallback'`, a validation failure makes `response.object` your `fallbackValue`, which was not validated; check `response.usedFallbackValue`.

## Streaming
With `agent.stream()` the final object is on `stream.fullStream` (chunk type `object-result`) and, after completion, `await stream.object`. Text chunks still arrive as natural language, not structured data.
```typescript
const stream = await testAgent.stream('Help me plan my day.', { structuredOutput: { schema } })
for await (const chunk of stream.fullStream) {
  if (chunk.type === 'object-result') console.log(JSON.stringify(chunk, null, 2))
}
console.log(await stream.object)
```

## Error handling
`errorStrategy` covers schema validation failure and failure of a separate structuring model: `strict` (default) throws, `warn` logs and continues, `fallback` returns `fallbackValue` and sets `usedFallbackValue: true`.
```typescript
structuredOutput: {
  schema: z.object({ summary: z.string(), keyFeatures: z.array(z.string()) }),
  errorStrategy: 'fallback',
  fallbackValue: { summary: 'TypeScript is a typed superset of JavaScript', keyFeatures: ['Static typing'] },
}
```

## Structuring agent
Give `structuredOutput` a `model` (string `provider/model`) when the main agent is poor at structured output: a second LLM call turns the main response into the object (extra latency and cost, can improve accuracy on complex schemas).

Related: computing-software.ai-ml-engineering.mastra.structured-output-with-tools-workarounds

## Checked

Date: 2026-11-07

Every cited page was read against the skill's claims. No claims removed. Large pages (agents/processors, workflows control-flow) were read only in the sections the skill covers; sections not covered by the skill were not read in full.

Method: documentation only; no commands were run.
