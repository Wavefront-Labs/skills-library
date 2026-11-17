---
id: computing-software.ai-ml-engineering.mastra.structured-output-with-tools-workarounds
name: structured-output-with-tools-workarounds
category: computing-software
field: ai-ml-engineering
product: mastra
tags: [mastra, structuredoutput, schema, jsonpromptinjection, tools, prepare-step, gemini, zod]
level: advanced
status: docs-checked
description: "Fix Mastra agents whose model cannot combine tools with structured output: jsonPromptInjection modes, a separate structuring model, or prepareStep."
sources:
  - https://mastra.ai/docs/agents/structured-output
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: make tools and `structuredOutput` work together when the model API does not support both at once.

Symptom per the page: tools are not called when structured output is enabled, or an error appears when combining them. It is a limitation of some model APIs, not Mastra. Three options:

## 1. `jsonPromptInjection`
By default the schema goes to the provider via the `response_format` parameter. Modes:
- `false` or omitted: native structured output.
- `'inline'`: schema instructions added to the latest user message.
- `true` or `'system'`: added to the system message.
- `'auto'`: native when Mastra's model capability data says supported, otherwise inline injection.
```typescript
structuredOutput: { schema, jsonPromptInjection: 'auto' }
```
Gemini 2.5 cannot combine `response_format` with function calling; with tools present you must set `jsonPromptInjection: true` to avoid `Function calling with a response mime type: 'application/json' is unsupported`.

Reduce tokens: injection embeds the serialized schema on every model call. While injection is active, set `instructions` to a compact hand-written field description (keep the field list complete). The response is still validated against `schema`; with native structured output `instructions` has no effect.
```typescript
structuredOutput: {
  schema: ticketSchema,
  jsonPromptInjection: 'system',
  instructions: 'Reply with a JSON object: "summary" (one paragraph), "priority" ("low" | "high"), "tags" (up to 5 strings). No markdown.',
}
```

## 2. Separate structuring model
`structuredOutput: { schema, model: 'openai/<model>' }`: the main agent handles all steps including tool calls; the structuring model only generates the structured output. Add `useAgent: true` to let it see conversation history (Mastra reuses the parent agent with the structuring model and attaches read-only memory context when a thread is available); leave unset to work only from the current response.

## 3. `prepareStep`
Split into steps: tools first, structured output after.
```typescript
prepareStep: async ({ stepNumber }) => {
  if (stepNumber === 0) {
    return { model: 'openai/<model>', tools: { weatherTool }, toolChoice: 'required' }
  }
  return {
    model: 'openai/<model>',
    tools: undefined,
    structuredOutput: { schema: z.object({ temperature: z.number(), humidity: z.number(), windSpeed: z.number() }) },
  }
}
```
Passed as an option to `agent.stream(...)`.

Related: computing-software.ai-ml-engineering.mastra.agent-structured-output-schemas

## Checked
Method: 2026-11-08 read the cited Mastra structured-output page in full (served as markdown) and compared each claim. All claims matched; no content changes.
