---
id: computing-software.ai-ml-engineering.vercel-ai-sdk.transform-text-streams-with-smoothstream-and-custom-transforms
name: transform-text-streams-with-smoothstream-and-custom-transforms
category: computing-software
field: ai-ml-engineering
product: vercel-ai-sdk
tags: [generate-text, experimental-transform, smooth-stream, stop-stream, guardrails]
level: advanced
status: docs-checked
description: "Apply experimental_transform to streamText for smoothing or custom TransformStreams, and stop a stream safely with stopStream and simulated finish events."
sources:
  - https://ai-sdk.dev/docs/ai-sdk-core/generating-text
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: modify or halt the `streamText` part stream before callbacks and promises see it.

## Basics
`experimental_transform` takes one transform or an array applied in order. Transforms run **before** callbacks fire and promises resolve, so `onEnd` receives the transformed text (an uppercase transform yields uppercase `text`).

Smoothing text and reasoning streaming:
```ts
import { smoothStream, streamText } from 'ai';
const result = streamText({ model, prompt, experimental_transform: smoothStream() });
```
Multiple: `experimental_transform: [firstTransform, secondTransform]`.

## Custom transform
A transform is a function that receives the tools available to the model and returns a function taking `{ tools, stopStream }`, which returns a `TransformStream<TextStreamPart<TOOLS>, TextStreamPart<TOOLS>>`:
```ts
import { type TextStreamPart, type ToolSet } from 'ai';
const upperCaseTransform = <TOOLS extends ToolSet>() =>
  (options: { tools: TOOLS; stopStream: () => void }) =>
    new TransformStream<TextStreamPart<TOOLS>, TextStreamPart<TOOLS>>({
      transform(chunk, controller) {
        controller.enqueue(chunk.type === 'text-delta' ? { ...chunk, text: chunk.text.toUpperCase() } : chunk);
      },
    });
```
Text deltas expose `chunk.text`.

## Stopping the stream
Call `stopStream()` (for example when a guardrail is violated, such as a stop word). You must then enqueue simulated `finish-step` and `finish` events to keep the stream well-formed and invoke all callbacks. The docs example enqueues:
- `finish-step` with `finishReason: 'stop'`, `rawFinishReason: 'stop'`, a `usage` object (`inputTokens`, `inputTokenDetails: { cacheReadTokens, cacheWriteTokens, noCacheTokens }`, `outputTokens`, `outputTokenDetails: { reasoningTokens, textTokens }`, `totalTokens`, all `undefined`), a `performance` object (zeros and `undefined`, with `toolExecutionMs: {}`), a `response` (`id`, `modelId`, `timestamp`) and `providerMetadata`.
- `finish` with `finishReason`, `rawFinishReason` and `totalUsage` of the same shape.
Then `return` without enqueuing the offending chunk.

## Gotchas
- The docs' stop-word example is simplified: real versions must buffer and scan across chunk boundaries to emit earlier text and detect all occurrences.

## Checked

Date: 2026-11-07. Read the 1 cited page(s) in full from the vercel/ai docs source and confirmed the commands, parameters, defaults and error strings above. Removed "experimental_transform may change between releases" (the docs warning covers experimental callbacks), and corrected the transform signature and performance object description.

Method: documentation only; no commands were run.
