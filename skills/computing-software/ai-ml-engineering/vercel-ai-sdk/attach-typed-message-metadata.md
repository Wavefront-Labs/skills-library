---
id: computing-software.ai-ml-engineering.vercel-ai-sdk.attach-typed-message-metadata
name: attach-typed-message-metadata
category: computing-software
field: ai-ml-engineering
product: vercel-ai-sdk
tags: [message-metadata, messagemetadata, uimessage, token-usage, zod, vercel-ai-sdk]
level: practitioner
status: docs-checked
description: "Send timestamps, model id and token usage as typed message-level metadata from toUIMessageStream and read message.metadata in useChat."
sources:
  - https://ai-sdk.dev/docs/ai-sdk-ui/message-metadata
  - https://ai-sdk.dev/docs/ai-sdk-ui/chatbot
  - https://ai-sdk.dev/docs/ai-sdk-ui/chatbot-message-persistence
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Attach typed message metadata

Goal: carry message-level facts (created time, model, tokens) from server to client with type safety.

## 1. Define the type

```ts
export const messageMetadataSchema = z.object({
  createdAt: z.number().optional(),
  model: z.string().optional(),
  totalTokens: z.number().optional(),
});
export type MessageMetadata = z.infer<typeof messageMetadataSchema>;
export type MyUIMessage = UIMessage<MessageMetadata>;
```

## 2. Send it

```ts
return createUIMessageStreamResponse({
  stream: toUIMessageStream({
    stream: result.stream,
    originalMessages: messages,   // typed MyUIMessage[]: gives type-safe return objects
    messageMetadata: ({ part }) => {
      if (part.type === 'start') return { createdAt: Date.now(), model: 'your-model-id' };
      if (part.type === 'finish') return { totalTokens: part.totalUsage.totalTokens };
    },
  }),
});
```

The callback runs per stream part; return an object for the stage you care about, nothing otherwise. `part.type === 'finish'` exposes `part.totalUsage` (a `LanguageModelUsage`).

## 3. Read it

```tsx
const { messages } = useChat<MyUIMessage>({ transport: new DefaultChatTransport({ api: '/api/chat' }) });
// message.metadata?.createdAt, message.metadata?.totalTokens
```

Metadata is also on the finished message in `onFinish: ({ message }) => message.metadata?.totalUsage`. A usage-only variant uses `type MyMetadata = { totalUsage: LanguageModelUsage }`.

## When to use something else

Metadata describes the message as a whole (timestamps, model, usage, user context, generation time, finish reason). For content that changes during generation use data parts instead. If the metadata must survive reloads, persist the UI messages (the persistence skill) and validate with `metadataSchema` in `validateUIMessages`.

## Checked

Date: 2026-11-07. Read the 3 cited page(s) in full from the vercel/ai docs source and confirmed the commands, parameters, defaults and error strings above. Removed as not stated on the cited pages: the part.response.modelId example and "data parts can be updated by id". Added the chatbot-message-persistence page (validateUIMessages and metadataSchema) after reading it.

Method: documentation only; no commands were run.
