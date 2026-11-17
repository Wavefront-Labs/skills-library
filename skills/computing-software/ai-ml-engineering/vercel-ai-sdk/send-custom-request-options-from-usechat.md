---
id: computing-software.ai-ml-engineering.vercel-ai-sdk.send-custom-request-options-from-usechat
name: send-custom-request-options-from-usechat
category: computing-software
field: ai-ml-engineering
product: vercel-ai-sdk
tags: [chatbot, usechat, transport, request-options, headers, body, vercel-ai-sdk]
level: practitioner
status: docs-checked
description: "Pass headers, body fields, credentials and a reshaped request payload from useChat to your API route, at hook level, per request, or via prepareSendMessagesRequest."
sources:
  - https://ai-sdk.dev/docs/ai-sdk-ui/chatbot
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Send custom request options from useChat

Goal: control what `useChat` sends to your backend (auth headers, extra body fields, a slimmed payload, trigger-specific requests).

## 1. Hook-level (all requests)

```tsx
useChat({
  transport: new DefaultChatTransport({
    api: '/api/custom-chat',
    headers: { Authorization: 'your_token' },
    body: { user_id: '123' },
    credentials: 'same-origin',
  }),
});
```

`headers`, `body` and `credentials` may also be functions (`headers: () => ({ Authorization: `Bearer ${getAuthToken()}` })`, `credentials: () => 'include'`) so tokens are read at send time. For changing component state, store the value in a `useRef` and read `ref.current` inside the function, or prefer request-level options.

## 2. Request-level (recommended)

Second argument of `sendMessage`; merged with hook-level options and takes precedence:

```tsx
sendMessage({ text: input }, {
  headers: { 'X-Custom-Header': 'custom-value' },
  body: { temperature: 0.7, user_id: '123' },
  metadata: { userId: 'user123' },
});
```

Server side: `const { messages, customKey } = await req.json();`.

## 3. Reshape the payload with prepareSendMessagesRequest

```tsx
new DefaultChatTransport({
  prepareSendMessagesRequest: ({ id, messages, trigger, messageId }) => {
    if (trigger === 'submit-user-message')
      return { body: { trigger, id, message: messages[messages.length - 1], messageId } };
    if (trigger === 'regenerate-assistant-message')
      return { body: { trigger, id, messageId } };
    throw new Error(`Unsupported trigger: ${trigger}`);
  },
})
```

The docs example sets `useChat({ id: 'my-chat' })`. On the server it loads stored messages by `id`; for regeneration it finds `messageId` with `findIndex` and keeps `messages.slice(0, messageIndex)` (removing the messages after `messageId`), then calls `convertToModelMessages` on the result.

## Gotchas

- Trigger values are exactly `submit-user-message` and `regenerate-assistant-message`.
- The docs example sends only the last message (`message: messages[messages.length - 1]`) and the route loads earlier messages from its own storage.
- For no-HTTP use (SSR, tests, single process) swap in `new DirectChatTransport({ agent })` with a `ToolLoopAgent`; it calls the agent's `stream()` directly.

## Checked

Date: 2026-11-07. Read the 1 cited page(s) in full from the vercel/ai docs source and confirmed the commands, parameters, defaults and error strings above. Restated the id and slice sentence and the last-message gotcha as what the docs example does.

Method: documentation only; no commands were run.
