---
id: computing-software.ai-ml-engineering.vercel-ai-sdk.stream-custom-data-parts-to-the-client
name: stream-custom-data-parts-to-the-client
category: computing-software
field: ai-ml-engineering
product: vercel-ai-sdk
tags: [streaming-data, data-parts, createuimessagestream, transient, ondata, vercel-ai-sdk]
level: practitioner
status: docs-checked
description: "Send typed data parts, sources and transient notifications alongside model text with createUIMessageStream and receive them via message parts or onData."
sources:
  - https://ai-sdk.dev/docs/ai-sdk-ui/streaming-data
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Stream custom data parts to the client

Goal: push status, sources or live widget data next to the assistant text, typed end to end.

## 1. Declare the message type

```ts
export type MyUIMessage = UIMessage<never /* metadata */, {
  weather: { city: string; weather?: string; status: 'loading' | 'success' };
  notification: { message: string; level: 'info' | 'warning' | 'error' };
}>;
```

Data part names become `data-<name>` (`data-weather`, `data-notification`).

## 2. Write from the server

```ts
const stream = createUIMessageStream<MyUIMessage>({
  execute: ({ writer }) => {
    writer.write({ type: 'start' }); // start the assistant message before any part
    writer.write({ type: 'data-notification', data: { message: 'Processing...', level: 'info' }, transient: true });
    writer.write({ type: 'source', value: { type: 'source', sourceType: 'url', id: 'source-1', url: 'https://weather.com', title: 'Weather Data Source' } });
    writer.write({ type: 'data-weather', id: 'weather-1', data: { city: 'San Francisco', status: 'loading' } });
    const result = streamText({ model, messages: await convertToModelMessages(messages),
      onEnd() { writer.write({ type: 'data-weather', id: 'weather-1', data: { city: 'San Francisco', weather: 'sunny', status: 'success' } }); } });
    writer.merge(toUIMessageStream({ stream: result.stream, sendStart: false })); // avoid a second start
  },
});
return createUIMessageStreamResponse({ stream });
```

Helpers: `createUIMessageStream`, `createUIMessageStreamResponse`, `pipeUIMessageStreamToResponse` (for Node response objects). Data travels as Server-Sent Events; non-JS backends can follow the stream protocol.

## Persistent vs transient vs reconciled

- Regular data parts land in `message.parts` and message history.
- `transient: true` parts are not added to history; they are visible only in `useChat({ onData })` (`onData: ({ data, type }) => { if (type === 'data-notification') showToast(...) }`).
- Writing again with the same `id` updates the existing part in place (reconciliation): loading state to result, progress bars, live artifacts.

## 3. Render

`message.parts.filter(p => p.type === 'data-weather')` then read `part.data.status`. Use `useChat<MyUIMessage>()` for typing.

## Data parts vs message metadata

Use `messageMetadata` (in `toUIMessageStream`) for message-level facts (timestamps, model, token usage, read as `message.metadata`). Use data parts for dynamic, arbitrary, updatable content.

## Checked

Date: 2026-11-07. Read the 1 cited page(s) in full from the vercel/ai docs source and confirmed the commands, parameters, defaults and error strings above. Removed the claim that execute must be async (not stated; the docs example awaits inside it).

Method: documentation only; no commands were run.
