---
id: computing-software.ai-ml-engineering.vercel-ai-sdk.stream-text-and-handle-stream-parts
name: stream-text-and-handle-stream-parts
category: computing-software
field: ai-ml-engineering
product: vercel-ai-sdk
tags: [generate-text, stream-text, text-stream, on-error, on-chunk, ui-message-stream]
level: practitioner
status: docs-checked
description: "Stream with streamText, consume textStream and the full stream parts, log errors with onError, use onChunk, and return HTTP responses."
sources:
  - https://ai-sdk.dev/docs/ai-sdk-core/generating-text
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: stream text for interactive use and handle every event type safely.

```ts
import { streamText } from 'ai';
const result = streamText({ model, prompt: 'Invent a new holiday and describe its traditions.',
  onError({ error }) { console.error(error); } });
for await (const textPart of result.textStream) console.log(textPart);
```
`result.textStream` is both a `ReadableStream` and an `AsyncIterable`.

## Two behaviours to respect
- `streamText` starts immediately and **suppresses errors** (they become stream parts) so servers do not crash: always supply `onError`.
- It uses **backpressure**: tokens are only generated as requested, so you must consume the stream (or call the promises) for it to finish.

## Full event stream
`result.stream` yields every part. Types: `start`, `start-step`, `text-start`, `text-delta`, `text-end`, `reasoning-start`, `reasoning-delta`, `reasoning-end`, `custom`, `source`, `file`, `reasoning-file`, `tool-call`, `tool-input-start`, `tool-input-delta`, `tool-input-end`, `tool-result`, `tool-error`, `tool-output-denied`, `tool-approval-request`, `tool-approval-response`, `finish-step`, `finish`, `abort`, `error`, `raw`. Switch on `part.type`; for tool parts also switch on `part.toolName`. Text deltas carry `chunk.text`.

`onChunk({ chunk })` receives the same part types:
```ts
onChunk({ chunk }) { if (chunk.type === 'text-delta') console.log(chunk.text); }
```

## Completion
`onEnd({ text, finishReason, usage, responseMessages, steps, totalUsage })` fires when the stream finishes. Promises on the result: `content`, `text`, `finalStep`, `files`, `sources`, `toolCalls`, `toolResults`, `finishReason`, `rawFinishReason`, `usage` (`totalUsage` is deprecated), `warnings`, `steps`. Streaming steps add `timeToFirstOutputMs`, and `timeBetweenOutputChunksMs` with `min`, `p10`, `median`, `avg`, `p90`, `max` when at least two chunks arrive.

## HTTP helpers for UI
Pass `result.stream` to standalone helpers:
- `createUIMessageStreamResponse({ stream: toUIMessageStream({ stream: result.stream }) })` (Next.js App Router)
- `pipeUIMessageStreamToResponse({ stream: toUIMessageStream({ stream: result.stream }), response })` (Node response)
- `createTextStreamResponse({ stream: toTextStream({ stream: result.stream }) })` and `pipeTextStreamToResponse(...)` for plain text.

## Gotchas
- Forgetting `onError` hides failures completely.
- Not consuming the stream stalls the call.

## Checked

Date: 2026-11-07. Read the 1 cited page(s) in full from the vercel/ai docs source and confirmed the commands, parameters, defaults and error strings above. No content change needed.

Method: documentation only; no commands were run.
