---
id: computing-software.ai-ml-engineering.vercel-ai-sdk.add-stop-endpoint-for-resumable-chat
name: add-stop-endpoint-for-resumable-chat
category: computing-software
field: ai-ml-engineering
product: vercel-ai-sdk
tags: [resume-streams, stop, activestreamid, abort, usechat, vercel-ai-sdk]
level: advanced
status: docs-checked
description: "Make a Stop button really cancel generation in a resumable useChat setup using a dedicated stop endpoint that saves the partial reply and clears activeStreamId."
sources:
  - https://ai-sdk.dev/docs/ai-sdk-ui/chatbot-resume-streams
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Add a stop endpoint for resumable chat

Goal: let users stop a generation in an app that uses `resume`, without a refresh or tab close also cancelling it.

## Why `stop()` is not enough

With resumable streams the server keeps producing after the client disconnects. `useChat().stop()` only aborts the local HTTP connection, so the model call or background job keeps running and the client can reconnect. Page refresh, tab close and navigation are disconnects, not stops.

## Client

Send the latest partial assistant message and the known stream id, then stop locally:

```tsx
const stop = () => {
  const last = chat.messages[chat.messages.length - 1];
  const assistantMessage = last?.role === 'assistant' ? last : undefined;
  void fetch(`/api/chat/${encodeURIComponent(chatData.id)}/stop`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(assistantMessage || chatData.activeStreamId
      ? { assistantMessage, activeStreamId: chatData.activeStreamId } : {}),
  });
  void chat.stop();
};
```

## Server (`app/api/chat/[id]/stop/route.ts`)

1. Read the chat; if `activeStreamId == null` return `{ success: true }`.
2. Parse the body with `.catch(() => ({}))`; if `body.activeStreamId` is set and differs from the stored one, return success (stale request for an older stream).
3. If `body.assistantMessage`, persist it as an insert or merge (never overwrite a newer server-written message with an older client snapshot).
4. `markStreamAsStopped(activeStreamId)` and `cancelActiveWork(activeStreamId)`: your backend specific functions (close the Redis stream and abort the model request, cancel the workflow run, or cancel the job / set a cancellation flag).
5. Re-read the chat and clear `activeStreamId` only if it still equals the one you stopped.

If replay state and producer state are separate, store enough with the chat to cancel the producer.

## Gotchas

- Never call the stop endpoint from route cleanup code; only from an explicit user action.
- After a user stop, do not auto-reconnect that chat until the user sends another message or retries, or the client may reconnect before cancellation completes.

## Checked

Date: 2026-11-07. Read the 1 cited page(s) in full from the vercel/ai docs source and confirmed the commands, parameters, defaults and error strings above. No content change needed.

Method: documentation only; no commands were run.
