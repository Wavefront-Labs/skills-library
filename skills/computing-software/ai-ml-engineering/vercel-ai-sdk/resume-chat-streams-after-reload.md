---
id: computing-software.ai-ml-engineering.vercel-ai-sdk.resume-chat-streams-after-reload
name: resume-chat-streams-after-reload
category: computing-software
field: ai-ml-engineering
product: vercel-ai-sdk
tags: [resume-streams, resumable-stream, redis, usechat, consumesse-stream, vercel-ai-sdk]
level: advanced
status: docs-checked
description: "Reconnect useChat to an in-flight generation after a reload using the resume option, consumeSseStream, the resumable-stream package, Redis and a GET resume route."
sources:
  - https://ai-sdk.dev/docs/ai-sdk-ui/chatbot-resume-streams
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Resume chat streams after a reload

Goal: a long generation continues and replays when the user refreshes or returns to the tab.

## What you need

The `resumable-stream` npm package, a Redis instance, and a persistence layer that records an `activeStreamId` per chat. The SDK supplies the `resume` option, the `consumeSseStream` callback and automatic GET requests.

## 1. Client

```tsx
useChat({
  id: chatData.id,
  messages: chatData.messages,
  resume,   // true: GET /api/chat/[id]/stream on mount
  transport: new DefaultChatTransport({
    prepareSendMessagesRequest: ({ id, messages }) => ({ body: { id, message: messages[messages.length - 1] } }), // chat id is required
  }),
});
```

The hook also reconnects when a backgrounded page becomes visible again, only if a network disconnect interrupted the stream. Resumed streams are treated as full replays by default (the client resets the interrupted response on the first `start` chunk). If your endpoint sends only remaining chunks, set `new DefaultChatTransport({ resumeStreamIsReplay: false })`. Continuing active text across a page reload is impossible; use full replay for reloads. Chat ids `.` and `..` are rejected with `InvalidArgumentError`.

## 2. POST route

Clear the previous active stream and save the user message (`saveChat({ id, messages, activeStreamId: null })`), then:

```ts
return createUIMessageStreamResponse({
  stream: toUIMessageStream({ stream: result.stream, originalMessages: messages, generateMessageId: generateId,
    onEnd: ({ messages }) => { saveChat({ id, messages, activeStreamId: null }); } }),
  async consumeSseStream({ stream }) {
    const streamId = generateId();
    const streamContext = createResumableStreamContext({ waitUntil: after }); // after from next/server
    await streamContext.createNewResumableStream(streamId, () => stream);
    saveChat({ id, activeStreamId: streamId });
  },
});
```

## 3. GET route `app/api/chat/[id]/stream/route.ts`

Read the chat; if `activeStreamId == null` return `new Response(null, { status: 204 })`; else `new Response(await streamContext.resumeExistingStream(chat.activeStreamId), { headers: UI_MESSAGE_STREAM_HEADERS })`.

## Custom resume URL

`prepareReconnectToStreamRequest: ({ id }) => ({ api: `/api/chat/${encodeURIComponent(id)}/stream`, credentials: 'include', headers: {...} })`. The callback gets the unencoded id and its `api` is used verbatim, so encode and validate it yourself.

## Gotchas

- Redis streams expire after a configurable time; several clients can attach to one stream.
- Authenticate both creation and resume; clear `activeStreamId` when starting a new stream to avoid resuming stale ones.
- `stop()` is a disconnect here, not a cancel; see the stop-endpoint skill.

## Checked

Date: 2026-11-07. Read the 1 cited page(s) in full from the vercel/ai docs source and confirmed the commands, parameters, defaults and error strings above. No content change needed.

Method: documentation only; no commands were run.
