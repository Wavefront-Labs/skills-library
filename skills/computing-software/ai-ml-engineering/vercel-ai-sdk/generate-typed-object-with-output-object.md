---
id: computing-software.ai-ml-engineering.vercel-ai-sdk.generate-typed-object-with-output-object
name: generate-typed-object-with-output-object
category: computing-software
field: ai-ml-engineering
product: vercel-ai-sdk
tags: [structured-data, output-object, zod, no-object-generated-error, schema-descriptions]
level: practitioner
status: docs-checked
description: "Generate a schema-validated object with generateText and Output.object, add property descriptions, name the output, and handle NoObjectGeneratedError."
sources:
  - https://ai-sdk.dev/docs/ai-sdk-core/generating-structured-data
  - https://ai-sdk.dev/docs/reference/ai-sdk-core/output
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: get a typed, validated object (not free text) from a model.

```ts
import { generateText, Output } from 'ai';
import { z } from 'zod';

const { output } = await generateText({
  model,
  output: Output.object({
    name: 'Recipe',                   // optional guidance for some providers
    description: 'A recipe for a dish.', // optional
    schema: z.object({
      name: z.string().describe('The name of the recipe'),
      ingredients: z.array(z.object({
        name: z.string(),
        amount: z.string().describe('The amount of the ingredient (grams or ml)'),
      })),
      steps: z.array(z.string()).describe('Step-by-step cooking instructions'),
    }),
  }),
  prompt: 'Generate a lasagna recipe.',
});
```
`schema` is a `FlexibleSchema`: Zod, Valibot, Standard JSON schema or custom JSON schema. Structured generation is part of the `generateText` / `streamText` flow, so it combines with tools.

## Tips
- `.describe('...')` on properties clarifies ambiguous names, expected formats and nested structures.
- `name` and `description` are used by some providers (e.g. via tool or schema name); they apply to `Output.object`, `array`, `choice` and `json`.
- Reasoning models: `result.reasoningText` holds the thought process if available.
- Raw provider response: `result.response.headers` / `result.response.body`.
- With tools, producing the structured output counts as a step; set `stopWhen: isStepCount(5)` (or similar) high enough for tool calls plus the output step.

## Errors
- `NoObjectGeneratedError` when the response cannot be parsed or validated. Check with `NoObjectGeneratedError.isInstance(error)`; it keeps `text` (raw text or tool-call text), `response` (id, timestamp, model), `usage` and `cause`.
- `NoOutputGeneratedError` when `result.output` is accessed but no output exists, for instance the final step finished with `tool-calls` rather than `stop`. `output` is a getter, so destructuring it also throws.

```ts
try { const r = await generateText({ model, output: Output.object({ schema }), prompt }); use(r.output); }
catch (e) { if (NoObjectGeneratedError.isInstance(e)) log(e.cause, e.text, e.usage); }
```

## Gotchas
- `Output.text()` is the default when `output` is omitted and returns a string.
- Streaming partials from `Output.object` are `DeepPartial` and cannot be validated against the schema.

## Checked

Date: 2026-11-07. Read the 2 cited page(s) in full from the vercel/ai docs source and confirmed the commands, parameters, defaults and error strings above. Removed "no separate object-generation function".

Method: documentation only; no commands were run.
