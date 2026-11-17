---
id: computing-software.ai-ml-engineering.vercel-ai-sdk.stream-structured-output-partial-and-element-streams
name: stream-structured-output-partial-and-element-streams
category: computing-software
field: ai-ml-engineering
product: vercel-ai-sdk
tags: [structured-data, stream-text, partial-output-stream, element-stream, output-array]
level: practitioner
status: docs-checked
description: "Stream structured output with streamText using partialOutputStream for objects and elementStream for Output.array, including bounds and error behaviour."
sources:
  - https://ai-sdk.dev/docs/ai-sdk-core/generating-structured-data
  - https://ai-sdk.dev/docs/reference/ai-sdk-core/output
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: show structured data to the user while the model is still generating it.

## Objects: partialOutputStream
```ts
import { streamText, Output } from 'ai';
const { partialOutputStream } = streamText({
  model,
  output: Output.object({ schema: recipeSchema }),
  prompt: 'Generate a lasagna recipe.',
  onError({ error }) { console.error(error); },
});
for await (const partialObject of partialOutputStream) console.log(partialObject);
```
Partials are deep-partial values of the schema type and are **not validated** (incomplete data may not conform yet). Validate only the final `output`. On the client use the `useObject` hook.

## Arrays: elementStream
```ts
const { elementStream } = streamText({
  model,
  output: Output.array({
    element: z.object({ name: z.string(), class: z.string(), description: z.string() }),
    minItems: 3, maxItems: 3,
  }),
  prompt: 'Generate 3 hero descriptions for a fantasy role playing game.',
});
for await (const hero of elementStream) console.log(hero); // complete and validated
```
- `minItems` / `maxItems`: non-negative integers, `minItems <= maxItems`; equal values mean exact length. They are sent in the provider schema when supported, and the SDK validates the completed array itself.
- Each `elementStream` item is complete and validated. This differs from `partialOutputStream`, which streams the whole partial array including unfinished elements; for arrays the partial output contains only fully validated elements.
- If the model emits more than `maxItems`, `elementStream` errors before the first excess element; provider generation is not aborted automatically and the final `output` promise rejects.

## Error handling
`streamText` starts streaming immediately and errors become stream parts instead of exceptions. Always pass `onError`. For `generateText` use try/catch with `NoObjectGeneratedError`.

## Gotchas
- Streaming structured output with tools still counts the output as a step; give `stopWhen` enough steps.

## Checked

Date: 2026-11-07. Read the 2 cited page(s) in full from the vercel/ai docs source and confirmed the commands, parameters, defaults and error strings above. Removed the "must consume the stream (backpressure)" gotcha (not on the cited pages).

Method: documentation only; no commands were run.
