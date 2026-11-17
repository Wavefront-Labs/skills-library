---
id: computing-software.ai-ml-engineering.vercel-ai-sdk.set-server-message-ids-and-save-on-disconnect
name: set-server-message-ids-and-save-on-disconnect
category: computing-software
field: ai-ml-engineering
product: vercel-ai-sdk
tags: [message-persistence, message-ids, consumestream, disconnect, vercel-ai-sdk]
level: practitioner
status: docs-checked
description: "Give assistant messages stable server-side IDs and make sure the reply is saved even if the client disconnects mid-stream."
sources:
  - https://ai-sdk.dev/docs/ai-sdk-ui/chatbot-message-persistence
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Stable message IDs and disconnect-safe saving

Goal: persisted conversations keep consistent IDs and survive closed tabs or network drops.

## Who generates IDs

- User message ids come from `useChat` on the client before the request. Keep those when saving the incoming messages (or generate and persist your own before sending).
- Assistant message ids are client-generated unless the server sends one in the stream. For persistence, use server ids.

## Option 1: generateMessageId

```ts
import { createIdGenerator } from 'ai';
toUIMessageStream({
  stream: result.stream,
  originalMessages: messages,
  generateMessageId: createIdGenerator({ prefix: 'msg', size: 16 }),
  onEnd: ({ messages }) => { saveChat({ chatId, messages }); },
})
```

## Option 2: write the start part yourself

```ts
const stream = createUIMessageStream({
  execute: async ({ writer }) => {
    writer.write({ type: 'start', messageId: generateId() });
    const result = streamText({ model, messages: await convertToModelMessages(messages) });
    writer.merge(toUIMessageStream({ stream: result.stream, sendStart: false })); // omit second start
  },
  originalMessages: messages,
  onEnd: ({ responseMessage }) => { /* save chat */ },
});
return createUIMessageStreamResponse({ stream });
```

Client-only id format (no persistence): `useChat({ generateId: createIdGenerator({ prefix: 'msgc', size: 16 }) })`.

## Surviving client disconnects

`streamText` applies backpressure, so if the browser closes, the provider stream is aborted and the chat can end up broken. Call `result.consumeStream()` (no await) before returning the response; it removes the backpressure so the stream runs to completion and `onEnd` fires, so `saveChat` still runs.

```ts
const result = streamText({ model, messages: await convertToModelMessages(messages) });
result.consumeStream(); // no await
return createUIMessageStreamResponse({ stream: toUIMessageStream({ stream: result.stream, originalMessages: messages, onEnd: ({ messages }) => { saveChat({ chatId, messages }); } }) });
```

On reload the chat is restored from storage.

## Gotchas

- In production also record request state (in progress, complete) with the stored messages so a reload during unfinished streaming can be handled.
- For true reconnection to a live stream, use the resumable-streams skill instead.

## Checked

Date: 2026-11-07. Read the 1 cited page(s) in full from the vercel/ai docs source and confirmed the commands, parameters, defaults and error strings above. No content change needed.

Method: documentation only; no commands were run.
