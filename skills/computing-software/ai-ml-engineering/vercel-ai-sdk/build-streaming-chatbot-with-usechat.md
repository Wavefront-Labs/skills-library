---
id: computing-software.ai-ml-engineering.vercel-ai-sdk.build-streaming-chatbot-with-usechat
name: build-streaming-chatbot-with-usechat
category: computing-software
field: ai-ml-engineering
product: vercel-ai-sdk
tags: [chatbot, usechat, streaming, ui-messages, status, vercel-ai-sdk]
level: practitioner
status: docs-checked
description: "Wire a streaming chat UI with useChat and a streamText route handler, then add status, stop, regenerate, error, throttle and callbacks."
sources:
  - https://ai-sdk.dev/docs/ai-sdk-ui/chatbot
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Build a streaming chatbot with useChat

Goal: a client component using `useChat` that streams assistant text from a `streamText` route and exposes status, stop, retry and message editing.

## Server route (`app/api/chat/route.ts`)

```ts
import { convertToModelMessages, createUIMessageStreamResponse, streamText, toUIMessageStream, UIMessage } from 'ai';

export const maxDuration = 30; // allow streaming up to 30 s

export async function POST(req: Request) {
  const { messages }: { messages: UIMessage[] } = await req.json();
  const result = streamText({
    model, // your provider model
    instructions: 'You are a helpful assistant.',
    messages: await convertToModelMessages(messages),
  });
  return createUIMessageStreamResponse({
    stream: toUIMessageStream({ stream: result.stream }),
  });
}
```

## Client (`app/page.tsx`)

```tsx
'use client';
import { useChat } from '@ai-sdk/react';
import { DefaultChatTransport } from 'ai';

const { messages, sendMessage, status, stop, regenerate, error, setMessages } = useChat({
  transport: new DefaultChatTransport({ api: '/api/chat' }),
});
```

- Send with `sendMessage({ text: input })`; keep `input` in your own `useState`.
- Render with `message.parts`, not `content`: `part.type === 'text' ? part.text : null`. Parts also carry tool invocations and results.

## State and controls

- `status` is `submitted` (request sent, no stream yet), `streaming`, `ready` (a new message may be sent) or `error`. Disable the input and submit button unless `status === 'ready'`; show a spinner on `submitted`; show Stop while `submitted` or `streaming`.
- `stop()` aborts the fetch. `regenerate()` reprocesses the last message and replaces it (enable on `ready` or `error`).
- `error` holds the fetch error: show a generic message ("Something went wrong") to avoid leaking server details, plus a Retry button calling `regenerate()`.
- `setMessages(messages.filter(m => m.id !== id))` deletes a message; `messages`/`setMessages` behave like React `state`/`setState`.

## Throttling and callbacks

- `useChat({ throttle: 50 })` throttles reactive message updates (React and Vue, from `@ai-sdk/vue`); stream processing and callbacks stay immediate, and the latest messages are published before `ready` or `error`.
- Callbacks: `onFinish({ message, messages, isAbort, isDisconnect, isError })`, `onError(error)`, `onData(data)` (any data part). Throwing inside `onData` triggers `onError` and stops the message being appended.

## Gotchas

- By default the server masks errors as "An error occurred."; see the error-handling skill to forward real messages.
- Plain-text backends need `TextStreamChatTransport` instead; tool calls, usage and finish reasons are then unavailable.

## Checked

Date: 2026-11-07. Read the 1 cited page(s) in full from the vercel/ai docs source and confirmed the commands, parameters, defaults and error strings above. No content change needed.

Method: documentation only; no commands were run.
