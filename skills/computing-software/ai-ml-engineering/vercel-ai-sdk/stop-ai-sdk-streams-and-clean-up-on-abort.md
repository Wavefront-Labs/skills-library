---
id: computing-software.ai-ml-engineering.vercel-ai-sdk.stop-ai-sdk-streams-and-clean-up-on-abort
name: stop-ai-sdk-streams-and-clean-up-on-abort
category: computing-software
field: ai-ml-engineering
product: vercel-ai-sdk
tags: [advanced, abort, abortsignal, onabort, backpressure, vercel-ai-sdk]
level: advanced
status: docs-checked
description: "Cancel AI SDK streams from the client and server, forward req.signal, enable Vercel supportsCancellation, and save partial results with onAbort or onEnd."
sources:
  - https://ai-sdk.dev/docs/advanced/stopping-streams
  - https://ai-sdk.dev/docs/advanced/backpressure
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Stop streams and clean up on abort

Goal: a Stop button that really cancels the model request, plus saving whatever was generated before the abort.

## 1. Client

`useChat` and `useCompletion` return a `stop` helper. It aborts the client HTTP request only. Show the button while `status` is `submitted` or `streaming`.

## 2. Server: forward the signal

```ts
const result = streamText({
  model,
  messages: await convertToModelMessages(messages),
  abortSignal: req.signal,
  onAbort: ({ steps }) => { /* persist partial results */ },
});
```

Your runtime must propagate the client disconnect to `req.signal`, and the route must pass it as `abortSignal`. `onAbort` receives `steps` (all completed steps before the abort). `onEnd` fires only on normal completion. In a raw `result.stream` loop there is also an `abort` stream part.

## 3. UI message streams

Pass `consumeSseStream: consumeStream` to `createUIMessageStreamResponse`, and read `isAborted` in `toUIMessageStream({ stream, onEnd })`. The docs say `consumeStream` is needed for proper abort handling. A consumer cancel (client disconnect before an outcome is declared) gives `isCancelled: true`, `outcome.status` `'unknown'` and `isAborted: false`; an observed `abort` part gives `outcome.status` `'aborted'` and `isAborted: true`. Check both flags if the same cleanup applies.

## 4. Vercel

Cancellation works only on the Node.js runtime and must be enabled per function in `vercel.json`:

```json
{ "functions": { "app/api/chat/route.ts": { "supportsCancellation": true } } }
```

Without it `stop()` ends the client stream but server generation may continue.

## Why streams are lazy (backpressure)

The backpressure page shows that wrapping a generator in a `ReadableStream` with an eager `for await` inside `start` keeps enqueuing forever, even after the reader stops, until memory runs out. Using `pull` with manual `iterator.next()` ties production to the consumer, so a navigated-away user frees the provider connection. With the lazy approach, navigating away from the page frees the fetch connection and its resources.

## Gotchas

- Abort is not compatible with stream resumption: `resume: true` in `useChat` breaks when you also abort. Choose one.
- AI SDK RSC does not support stopping streams.

## Checked

Date: 2026-11-07. Read the 2 cited page(s) in full from the vercel/ai docs source and confirmed the commands, parameters, defaults and error strings above. Removed the claim that the persistence skill uses consumeStream() to opt out.

Method: documentation only; no commands were run.
