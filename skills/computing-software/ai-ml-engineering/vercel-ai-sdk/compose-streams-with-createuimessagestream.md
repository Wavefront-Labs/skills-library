---
id: computing-software.ai-ml-engineering.vercel-ai-sdk.compose-streams-with-createuimessagestream
name: compose-streams-with-createuimessagestream
category: computing-software
field: ai-ml-engineering
product: vercel-ai-sdk
tags: [streaming-data, createuimessagestream, writer-merge, onend, outcome, vercel-ai-sdk]
level: advanced
status: docs-checked
description: "Compose a UI message stream by hand with createUIMessageStream: write chunks, merge streamText, set the outcome, handle errors and persist in onEnd."
sources:
  - https://ai-sdk.dev/docs/reference/ai-sdk-ui/create-ui-message-stream
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Compose streams with createUIMessageStream

Goal: build one response stream from hand-written chunks plus one or more `streamText` streams, with correct lifecycle, errors and end callback.

## Example

```ts
const stream = createUIMessageStream({
  async execute({ writer }) {
    writer.write({ type: 'start' });                              // outer stream owns the assistant message
    writer.write({ type: 'text-start', id: 'example-text' });     // same id across start/delta/end
    writer.write({ type: 'text-delta', id: 'example-text', delta: 'Hello' });
    writer.write({ type: 'text-end', id: 'example-text' });

    const result = streamText({ model, prompt: 'Write a haiku about AI' });
    writer.merge(toUIMessageStream({
      stream: result.stream,
      sendStart: false,
      onEnd: ({ outcome }) => writer.setOutcome(outcome),
    }));
  },
  onError: error => `Custom error: ${error instanceof Error ? error.message : String(error)}`,
  originalMessages: existingMessages,
  onEnd: ({ messages, isContinuation, outcome, responseMessage }) => { /* persist */ },
});
```

## Parameters

- `execute({ writer })`: `writer.write(chunk)`, `writer.merge(stream)`, `writer.setOutcome(outcome)`, `writer.onError`.
- `onError(error) => string`: default message is `"An error occurred."` so server details are not sent.
- `originalMessages`: if provided, persistence mode is assumed and the response message gets an ID.
- `generateId`: custom `IdGenerator`.
- `onEnd` options: `messages`, `isContinuation` (response extends the last original message), `isAborted`, `isCancelled` (true when the consumer cancelled before an outcome, e.g. client disconnect), `outcome`, `responseMessage`, `finishReason` (`stop`, `length`, `content-filter`, `tool-calls`, `error`, `interrupted`, `other`). `onFinish` is a deprecated alias.

## Outcome semantics

`outcome` is `{status:'completed'} | {status:'failed', error?} | {status:'aborted'} | {status:'unknown'}`. `setOutcome` records the composer's policy without writing a chunk or closing the stream; the first declared outcome is kept, but a fatal execution, merge, error-handling or downstream failure forces `failed`. Individual `error` chunks do not change the outcome. With several merged child streams, aggregate their outcomes and call `setOutcome` once. If the consumer cancels before an outcome is declared, it stays `unknown`; check `isCancelled`.

## Gotchas

- Returns `ReadableStream<UIMessageChunk>`.
- The docs example writes `start` itself (the outer stream owns the assistant message lifecycle) and sets `sendStart: false` on the merged `toUIMessageStream`.

## Checked

Date: 2026-11-07. Read the 1 cited page(s) in full from the vercel/ai docs source and confirmed the commands, parameters, defaults and error strings above. Removed the createUIMessageStreamResponse wrapping advice and the "always sendStart: false" rule; restated as what the docs example does.

Method: documentation only; no commands were run.
