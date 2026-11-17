---
id: computing-software.ai-ml-engineering.vercel-ai-sdk.persist-and-reload-chat-messages
name: persist-and-reload-chat-messages
category: computing-software
field: ai-ml-engineering
product: vercel-ai-sdk
tags: [message-persistence, usechat, validateuimessages, onend, chat-store, vercel-ai-sdk]
level: practitioner
status: docs-checked
description: "Store UIMessage arrays when a stream ends, reload them into useChat, send only the last message, and validate stored messages with validateUIMessages."
sources:
  - https://ai-sdk.dev/docs/ai-sdk-ui/chatbot-message-persistence
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Persist chat messages and reload them into useChat

Goal: save each conversation after the model finishes and restore it on page load.

## Steps

1. Create a chat id server-side (`generateId()` from `ai`), store an empty `[]`, and redirect to `/chat/[id]`. Treat ids as opaque tokens: validate against `/^[A-Za-z0-9_-]+$/` and confirm the resolved file path stays inside the chat directory before using it in a path. (The docs example is file-based; use a database in production.)
2. `loadChat(id): Promise<UIMessage[]>` reads the stored JSON.
3. The page loads messages and passes them down:
   ```tsx
   const messages = await loadChat(id);
   return <Chat id={id} initialMessages={messages} />;
   ```
   In the client component: `useChat({ id, messages: initialMessages, transport: new DefaultChatTransport({ api: '/api/chat' }) })`.
4. Save in the route via `onEnd` on `toUIMessageStream`, passing `originalMessages` so the callback gets the full list including the new assistant reply:
   ```ts
   toUIMessageStream({
     stream: result.stream,
     originalMessages: messages,
     onEnd: ({ messages }) => { saveChat({ chatId, messages }); },
   })
   ```
   The docs recommend storing the `useChat` (`UIMessage`) format, not `ModelMessage`.

## Send only the last message

Client transport: `prepareSendMessagesRequest({ messages, id }) { return { body: { message: messages[messages.length - 1], id } }; }`. Server: `const previousMessages = await loadChat(id);` then validate `[...previousMessages, message]`.

## Validate stored messages

```ts
const validatedMessages = await validateUIMessages({
  messages: [...previousMessages, message],
  tools,            // tool calls must match current schemas
  metadataSchema,   // custom metadata
  dataSchemas,      // custom data parts
});
const result = streamText({ model, messages: await convertToModelMessages(validatedMessages), tools });
```

Catch `TypeValidationError` (from `ai`) when stored data no longer matches schemas; log it and migrate, filter, or start with empty history.

## Gotchas

- Persist the complete UI message including `rawInput` on `input-streaming` tool parts so a resumed stream can append later deltas.
- `rawInput` on `output-error` tool parts is deprecated; `validateUIMessages`, `safeValidateUIMessages` and `convertToModelMessages` warn. Migrate by moving it to `input` when `input` is null or undefined, then drop `rawInput` (use `isToolUIPart(part)` to narrow).
- The guide states it does not cover authorization or error handling.

## Checked

Date: 2026-11-07. Read the 1 cited page(s) in full from the vercel/ai docs source and confirmed the commands, parameters, defaults and error strings above. Reworded the storage-format and authorization notes to the page wording.

Method: documentation only; no commands were run.
