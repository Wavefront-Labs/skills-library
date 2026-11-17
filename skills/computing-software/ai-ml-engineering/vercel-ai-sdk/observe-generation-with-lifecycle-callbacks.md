---
id: computing-software.ai-ml-engineering.vercel-ai-sdk.observe-generation-with-lifecycle-callbacks
name: observe-generation-with-lifecycle-callbacks
category: computing-software
field: ai-ml-engineering
product: vercel-ai-sdk
tags: [generate-text, lifecycle-callbacks, observability, tool-execution, telemetry]
level: practitioner
status: docs-checked
description: "Hook onStart, onStepStart, onLanguageModelCall*, onToolExecution* and onStepEnd into generateText or streamText for logging and timing."
sources:
  - https://ai-sdk.dev/docs/ai-sdk-core/generating-text
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: log or time each phase of a (multi-step) generation without changing its behaviour.

Both `generateText` and `streamText` accept these experimental callbacks; they may break between incremental releases. Errors thrown inside them are silently caught and do not break generation.

```ts
const result = await generateText({
  model, prompt: 'What is the weather in San Francisco?', tools: { /* ... */ },
  onStart({ modelId }) { console.log('started', { modelId }); },
  onStepStart({ stepNumber, modelId, messages }) {},
  onLanguageModelCallStart({ modelId, messages }) {},
  onLanguageModelCallEnd({ modelId, finishReason, content }) {},
  onToolExecutionStart({ toolCall }) {},
  onToolExecutionEnd({ toolCall, toolExecutionMs, toolOutput }) {
    const ok = toolOutput.type === 'tool-result'; // else 'tool-error'
  },
  onStepEnd({ stepNumber, finishReason, usage, performance }) {},
});
```

## Order and payloads
- `onStart`: once, before any LLM call; model info, messages, settings, `runtimeContext` (streamText also passes `instructions`).
- `onStepStart`: before each LLM call; step number, model, messages, tools, prior steps.
- `onLanguageModelCallStart`: immediately before the provider call (observe the model call apart from tool work).
- `onLanguageModelCallEnd`: after the response is normalised and parsed, but before client-side tool execution; content parts, usage, finish reason, provider metadata.
- `onToolExecutionStart`: right before a tool `execute`; tool call, messages, `toolContext`.
- `onToolExecutionEnd`: after execute completes or errors; `toolCall`, `toolExecutionMs`, and `toolOutput`, a union of `{ type: 'tool-result', output }` or `{ type: 'tool-error', error }`.
- `onStepEnd`: after each step; `stepNumber` is the zero-based index of the completed step (generateText).

The non-experimental completion hook is `onEnd` (final step), covered in the result-fields skill.

## Gotchas
- Errors thrown inside these callbacks are silently caught, so they will not surface.
- Per-tool timing is `toolExecutionMs` on `onToolExecutionEnd`; step `performance.toolExecutionMs` is keyed by tool call ID.

## Checked

Date: 2026-11-07. Read the 1 cited page(s) in full from the vercel/ai docs source and confirmed the commands, parameters, defaults and error strings above. Reworded the gotchas to what the page states.

Method: documentation only; no commands were run.
