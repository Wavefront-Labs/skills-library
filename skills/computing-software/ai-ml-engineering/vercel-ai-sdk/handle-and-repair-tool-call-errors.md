---
id: computing-software.ai-ml-engineering.vercel-ai-sdk.handle-and-repair-tool-call-errors
name: handle-and-repair-tool-call-errors
category: computing-software
field: ai-ml-engineering
product: vercel-ai-sdk
tags: [tool-calling, error-handling, repair-tool-call, tool-error, no-such-tool-error]
level: advanced
status: docs-checked
description: "Catch NoSuchToolError and InvalidToolInputError, read tool-error parts, forward friendly stream errors, and fix bad calls with repairToolCall."
sources:
  - https://ai-sdk.dev/docs/ai-sdk-core/tools-and-tool-calling
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: survive invalid or failing tool calls without losing the run.

## Error kinds
- `NoSuchToolError`: model called an undefined tool.
- `InvalidToolInputError`: input does not match the tool's `inputSchema`.
- `ToolCallRepairError`: failure during repair.
- `ToolChoiceViolationError`: response violates a required or specific `toolChoice`.
- Errors thrown inside your `execute` become `tool-error` content parts (so multi-step loops can continue), not exceptions.

## generateText
Validation errors throw; catch with `.isInstance`:
```ts
try { await generateText({ /* ... */ }); }
catch (error) {
  if (NoSuchToolError.isInstance(error)) { /* ... */ }
  else if (InvalidToolInputError.isInstance(error)) { /* ... */ }
}
```
Execution errors are in the steps:
```ts
const toolErrors = steps.flatMap(s => s.content.filter(p => p.type === 'tool-error'));
toolErrors.forEach(e => console.log(e.toolName, e.input, e.error));
```

## streamText
Errors are stream parts: `tool-error` for execution failures, `error` for others. When building a UI response pass an error mapper:
```ts
createUIMessageStreamResponse({
  stream: toUIMessageStream({
    stream: result.stream,
    onError: error => NoSuchToolError.isInstance(error) ? 'The model tried to call a unknown tool.'
      : InvalidToolInputError.isInstance(error) ? 'The model called a tool with invalid inputs.'
      : 'An unknown error occurred.',
  }),
});
```

## Repair without extra steps
In multi-step runs a failed call is sent back to the model next step, which pollutes history. `repairToolCall` fixes it in place and receives `{ toolCall, tools, inputSchema, error, messages, instructions }`; return a corrected call (`{ ...toolCall, input: JSON.stringify(repaired) }`) or `null` to give up.
- Strategy 1 (structured output): call `generateText` with `output: Output.object({ schema: tool.inputSchema })` and a prompt showing the bad input and `JSON.stringify(await inputSchema({ toolName }))`.
- Strategy 2 (re-ask): call a model again with `messages` plus an assistant `tool-call` and a `tool` result whose `output` is `error.message`, then find the new call in `result.toolCalls`.
- Return `null` for `NoSuchToolError` rather than guessing names.

## Gotchas
- Execution errors are added as `tool-error` parts to enable automated LLM roundtrips in multi-step runs.

## Checked

Date: 2026-11-07. Read the 1 cited page(s) in full from the vercel/ai docs source and confirmed the commands, parameters, defaults and error strings above. Replaced an inferred gotcha with the docs statement about tool-error parts.

Method: documentation only; no commands were run.
