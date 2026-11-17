---
id: computing-software.ai-ml-engineering.vercel-ai-sdk.handle-errors-and-warnings-in-ai-sdk-ui
name: handle-errors-and-warnings-in-ai-sdk-ui
category: computing-software
field: ai-ml-engineering
product: vercel-ai-sdk
tags: [error-handling, warnings, usechat, onerror, deprecation, vercel-ai-sdk]
level: practitioner
status: docs-checked
description: "Classify useChat errors with the exported SDK error classes, show safe retry UI, forward server messages, and route or silence AI SDK warnings."
sources:
  - https://ai-sdk.dev/docs/ai-sdk-ui/error-handling
  - https://ai-sdk.dev/docs/ai-sdk-ui/chatbot
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Handle errors and warnings in AI SDK UI

Goal: show helpful but non-leaky errors in the UI, branch on error type, and manage SDK warnings.

## Error state and retry

Each UI hook returns `error`. Show a generic message ("Something went wrong") to avoid leaking server information, a Retry button calling `regenerate()`, and `disabled={error != null}` on the input.

Replace a failed turn instead of retrying: before `sendMessage`, call `setMessages(m => m.at(-1)?.role === 'assistant' ? m.slice(0, -2) : m.slice(0, -1))` (removes the partial assistant reply and its user message, or just the user message).

## onError and error classes

`useChat` and `useCompletion` accept `onError`. Use the marker-based `.isInstance()` guards from `ai`:

| Class | Cause |
| --- | --- |
| `APICallError` | non-successful HTTP response (`error.statusCode`) |
| `EmptyResponseBodyError` | successful response without a body |
| `UIMessageStreamError` | completion data stream error or invalid UI message stream chunks |
| `InvalidArgumentError` | invalid stream protocol or message ID |
| `UnsupportedFunctionalityError` | `FileList` in an unsupported environment |

`APICallError.requestBodyValues` is `undefined` in UI requests so prompts are not copied into client-visible errors; `message` and `responseBody` still hold the response text. Errors from custom `fetch`, callbacks and stream parsers propagate unchanged.

## Forward server errors

By default the stream masks errors as "An error occurred." Pass `onError` to `toUIMessageStream({ stream: result.stream, onError })` returning a string (`error.message` for `Error`, the string itself, `JSON.stringify` otherwise, `'unknown error'` for null). Tool execution errors with `providerExecuted: true` bypass that callback, so it cannot redact them.

## Testing

Throw in the route handler: `throw new Error('This is a test error')`.

## Warnings

Warnings start with "AI SDK Warning", are emitted via `process.emitWarning` where available and `console.warn` in browser/edge.
- Disable: `globalThis.AI_SDK_LOG_WARNINGS = false;`
- Custom: `globalThis.AI_SDK_LOG_WARNINGS = ({ warnings, provider, model }) => { ... }` (receives every warning, including repeated deprecations).
- Multiple SDK versions share that global; type the handler as a union of each version's `LogWarningsFunction` parameters (import under package aliases such as `npm:ai@6`).
- Deprecations log once per code per SDK instance with codes like `AISDK_DEP_GENERATE_OBJECT` (use `generateText` with `output`), `AISDK_DEP_STREAM_OBJECT`, `AISDK_DEP_UI_MESSAGE_RAW_INPUT` (use `input` not `rawInput`), `AISDK_DEP_IMAGE_CONTENT_PART` (use `file` parts). Node flags `--throw-deprecation`, `--no-deprecation`, `--trace-deprecation` apply to all DeprecationWarnings.

## Checked

Date: 2026-11-07. Read the 2 cited page(s) in full from the vercel/ai docs source and confirmed the commands, parameters, defaults and error strings above. No content change needed.

Method: documentation only; no commands were run.
