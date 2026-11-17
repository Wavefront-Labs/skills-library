---
id: computing-software.ai-ml-engineering.vercel-ai-sdk.set-call-settings-retries-and-timeouts
name: set-call-settings-retries-and-timeouts
category: computing-software
field: ai-ml-engineering
product: vercel-ai-sdk
tags: [settings, temperature, max-retries, timeout, abort-signal]
level: practitioner
status: docs-checked
description: "Set sampling options, maxRetries, abortSignal, headers and the timeout object (totalMs, stepMs, firstChunkMs, chunkMs, toolMs, per-tool) on AI SDK calls."
sources:
  - https://ai-sdk.dev/docs/ai-sdk-core/settings
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: tune generation behavior and bound how long a call, step, stream or tool may run.

## Common settings
```ts
const result = await generateText({
  model, prompt: 'Invent a new holiday and describe its traditions.',
  maxOutputTokens: 512, temperature: 0.3, maxRetries: 5, timeout: 10000,
});
```
Language model call options (forwarded to the model): `maxOutputTokens`, `temperature`, `topP`, `topK`, `presencePenalty`, `frequencyPenalty`, `stopSequences`, `seed`, `reasoning`. Ranges depend on the provider; `0` usually means near-deterministic temperature and no penalty. Set `temperature` or `topP`, not both. `topK` is for advanced use. `seed` gives deterministic output only if the model supports it.

Request options (transport, not generation): `maxRetries` (default 2, `0` disables), `abortSignal`, `timeout`, `headers` (HTTP providers only; headers set on the provider config go on every request).

## Timeouts
`timeout` is milliseconds or an object. It combines with `abortSignal`; whichever fires first aborts.
```ts
timeout: 5000                          // whole call
timeout: { totalMs: 60000, stepMs: 10000 }
streamText({ model, prompt, timeout: { firstChunkMs: 10000, chunkMs: 5000 } })
generateText({ model, tools, prompt, timeout: { toolMs: 5000, tools: { weatherMs: 3000, slowApiMs: 10000 } } })
```
- `totalMs`: entire call, all steps.
- `stepMs`: each step including generation, retries and local tool execution, cumulative across provider attempts.
- `firstChunkMs` (streaming only): until the first content-bearing output of each step. Text, reasoning and tool-input deltas, files and tool calls count; metadata, stream start, empty deltas and raw chunks do not.
- `chunkMs` (streaming only): gap between meaningful chunks after output starts; does not limit the wait for the first.
- `toolMs`: default per tool execution; a timed-out tool aborts and returns a tool-error so the model can respond or retry.
- `tools`: per-tool overrides keyed `{toolName}Ms`, which beat `toolMs`; names are type-checked.

Cancel from a UI or a fixed deadline with `abortSignal: AbortSignal.timeout(5000)`.

## Unsupported settings
If a provider does not support a setting, a warning is generated; check the `warnings` property of the result.

## Gotchas
- Since AI SDK 5.0, temperature is no longer `0` by default.
- `firstChunkMs` and `chunkMs` timers stop when the response finishes, errors or is cancelled; each retry or later model call gets fresh budgets. Retry backoff and local tool execution sit outside them, while `stepMs` and `totalMs` stay active across both.
- Provider-executed tools stay inside the model response budget.

## Checked

Date: 2026-11-07. Read the 1 cited page(s) in full from the vercel/ai docs source and confirmed the commands, parameters, defaults and error strings above. Replaced the invented Verify section with the docs statement that unsupported settings generate a warning in the result warnings property.

Method: documentation only; no commands were run.
