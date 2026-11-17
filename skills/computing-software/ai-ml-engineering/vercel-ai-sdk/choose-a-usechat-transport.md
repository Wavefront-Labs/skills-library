---
id: computing-software.ai-ml-engineering.vercel-ai-sdk.choose-a-usechat-transport
name: choose-a-usechat-transport
category: computing-software
field: ai-ml-engineering
product: vercel-ai-sdk
tags: [transport, usechat, websocket, directchattransport, workflowchattransport, vercel-ai-sdk]
level: advanced
status: docs-checked
description: "Pick and configure DefaultChatTransport, WebSocketChatTransport, DirectChatTransport, WorkflowChatTransport or the Chat SDK web adapter for a useChat app."
sources:
  - https://ai-sdk.dev/docs/ai-sdk-ui/transport
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Choose and configure a useChat transport

Goal: select how `useChat` talks to the backend and handle each transport's lifecycle.

## Options

1. `DefaultChatTransport` (HTTP POST to `/api/chat` by default, equal to calling `useChat()` bare). Options: `api`, `headers`, `body`, `credentials` (each may be a function for refreshed tokens), `prepareSendMessagesRequest({ id, messages, trigger, messageId })` returning `{ headers, body }`, for example `messages.slice(-10)` to cap payload.
2. `WebSocketChatTransport({ url, params: () => ({ token }) })`, one persistent socket for all turns. Create it with `useMemo(() => new ..., [])`.
   - Multiplexes by `requestId`, validates incoming `UIMessageChunk`s, forwards aborts; http/https URLs become ws/wss.
   - You own the lifecycle: React/Vue hooks do not close a supplied transport. Call `transport.close()` after the last consumer; call `chat.dispose()` for a directly managed `Chat` that exclusively owns it.
   - Your server must implement the documented wire protocol; type frames with `WebSocketChatTransportRequest`/`Response` and check untrusted frames with `safeValidateWebSocketChatTransportRequest`.
   - Browsers cannot set handshake headers, so `headers` travel inside each request frame; authenticate the handshake with cookies, a short-lived query param or a subprotocol, and validate origin and every frame.
   - If the socket closes mid-response the stream errors and nothing is replayed automatically (replay could duplicate output or tool effects). `reconnectToStream` asks for a complete replay from sequence zero, including the original `start` chunk `messageId`. `sendAutomaticallyWhen` starts a new turn; it does not inject tool results into a running generation.
3. `DirectChatTransport({ agent, options, sendReasoning, sendSources })` runs a `ToolLoopAgent` in-process (validates UI messages, `convertToModelMessages`, `agent.stream()`, `toUIMessageStream()`). For SSR, tests, desktop/CLI apps. `reconnectToStream()` always returns `null`.
4. `WorkflowChatTransport` from `@ai-sdk/workflow/client` (`api`, `maxConsecutiveErrors`, `initialStartIndex`, `onChatSendMessage`, `onChatEnd({ chatId, chunkIndex })`): detects a missing `finish` event and reconnects via GET to `{api}/{runId}/stream`. Negative `initialStartIndex` fetches only the tail when the durable stream stores `UIMessageChunk`s; raw `WorkflowAgent` streams need a non-negative cursor.
5. Chat SDK web adapter (`@chat-adapter/web`): the default transport works unchanged; `getUser` is the security boundary (return null for 401); history lives in the adapter's state, and `stop()` propagates the abort signal.

## Custom transports

Implement the `ChatTransport` interface (it includes `sendMessages`); read the source of `DefaultChatTransport` and `HttpChatTransport` in the AI SDK repo as templates.

## Checked

Date: 2026-11-07. Read the 1 cited page(s) in full from the vercel/ai docs source and confirmed the commands, parameters, defaults and error strings above. Removed the "reconnect" member of ChatTransport (not stated).

Method: documentation only; no commands were run.
