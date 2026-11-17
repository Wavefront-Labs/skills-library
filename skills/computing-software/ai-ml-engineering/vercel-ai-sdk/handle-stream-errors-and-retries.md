---
id: computing-software.ai-ml-engineering.vercel-ai-sdk.handle-stream-errors-and-retries
name: handle-stream-errors-and-retries
category: computing-software
field: ai-ml-engineering
product: vercel-ai-sdk
tags: [error-handling-core, streamtext, streamretries, onabort, streamprovidererror]
level: practitioner
status: docs-checked
description: "Handle errors from generateText and streamText, read error and abort parts, enable streamRetries or onError-directed retry, and clean up with onAbort."
sources:
  - https://ai-sdk.dev/docs/ai-sdk-core/error-handling
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: make text generation fail safely, retry transient provider errors mid-stream, and clean up aborted streams.

1. Regular errors and streams without error chunks (`textStream`): wrap the call or the `for await` loop in `try/catch`.
2. Streams with error parts: iterate `stream` (docs use `const { stream } = streamText(...)`) and switch on `part.type`: `'error'` (`part.error`; check `StreamProviderError.isInstance(error)` for `type`, `code`, `statusCode`, `isRetryable`), `'abort'`, `'tool-error'` (`part.error`). Still keep an outer try/catch for failures outside the stream.
3. Retry after streaming started: `maxRetries` only covers failures while starting a call. For well-formed provider error events received mid-stream set `streamRetries: 2`.
4. Callback-directed retry: set `streamRetries: 0` (it must be set explicitly to enable recovery) and in `onError: ({ error }) => { if (isTransientProviderError(error)) return { retry: true }; }`.
5. Aborts: `onAbort: ({ steps }) => {...}` runs when the stream is aborted via `AbortSignal`; `onEnd` runs only on normal completion. You can also handle an `abort` part in the stream.

Semantics to remember:
- A stream retry reruns only the failed model step with the same accumulated context; earlier steps and their tool calls are not replayed. Tool input, calls, approval requests, callbacks and client-side tool execution from a failed attempt are discarded until an attempt reaches a successful model-call finish.
- Provider error events become `StreamProviderError` instances; the same instance goes to `onError` and, if not recovered, to the final `error` part. Use `isRetryable` to decide.
- A retry stays in the same step: `onStepStart` once, `onLanguageModelCallStart` per attempt, `onLanguageModelCallEnd` only for attempts that finish.
- Callback-directed recovery is one retry per step; if automatic retries are configured, `onError` may add one more, so the cap is `streamRetries + 1`.
- If `streamRetries` is omitted, all stream retry behavior is off and a logging-only `onError` keeps incremental tool streaming. Returning anything other than `{ retry: true }` does not request recovery.

Gotchas:
- Non-tool output already emitted cannot be retracted; consumers may see repeated or divergent partial text, reasoning, files or sources (open text and reasoning parts are ended before recovered output starts). Failed-attempt output is excluded from the step result, structured-output parsing, response messages and later steps.
- Provider-executed tools cannot be undone by retries; use idempotency controls. Retries add latency and cost.

## Checked

Date: 2026-11-07. Read the 1 cited page(s) in full from the vercel/ai docs source and confirmed the commands, parameters, defaults and error strings above. Corrected result.stream to stream.

Method: documentation only; no commands were run.
