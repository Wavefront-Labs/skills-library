---
id: computing-software.web-development.elysia.elysia-ai-sdk-stream-responses
name: elysia-ai-sdk-stream-responses
category: computing-software
field: web-development
product: elysia
tags: [integrations-ai-sdk, ai-sdk, streaming, sse, llm]
level: practitioner
status: docs-checked
description: "Stream Vercel AI SDK output from Elysia routes as ReadableStream, Server-Sent Events, Response helpers, generator functions or proxied fetch."
sources:
  - https://elysiajs.com/integrations/ai-sdk.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: return model output to a client progressively.

Elysia streams any `ReadableStream` or `Response` you return. Pick one pattern:

1. Return the stream directly:

```ts
import { Elysia } from 'elysia'
import { streamText } from 'ai'
import { openai } from '@ai-sdk/openai'

new Elysia().get('/', () => {
    const stream = streamText({ model: openai('gpt-5'), system: '...', prompt: 'Hi!' })
    return stream.textStream            // or stream.toUIMessageStream()
})
```

2. Server-Sent Events: import `sse` from `elysia` and wrap: `return sse(stream.textStream)` (or `sse(stream.toUIMessageStream())`); each chunk becomes one SSE message.

3. As a Response: `return stream.toTextStreamResponse()` or `stream.toUIMessageStreamResponse()` (the UI message variant uses SSE). Use this when you do not need the typed stream for Eden.

4. Manual control with a generator:

```ts
new Elysia().get('/', async function* () {
    const stream = streamText({ model: openai('gpt-5'), prompt: 'Hi!' })
    for await (const data of stream.textStream)
        yield sse({ data, event: 'message' })
    yield sse({ event: 'done' })
})
```

5. Model not supported by the SDK: import `fetch` from `elysia` and return the upstream response; Elysia proxies it with streaming:

```ts
import { Elysia, fetch } from 'elysia'
new Elysia().get('/', () => fetch('https://api.openai.com/v1/chat/completions', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${process.env.OPENAI_API_KEY}` },
    body: JSON.stringify({ model: 'gpt-5', stream: true, messages: [{ role: 'user', content: 'Hi!' }] })
}))
```

Gotchas:
- The docs' "As Response" and "Manual Streaming" samples import `{ ai } from 'ai'` but call `streamText`; import `streamText` as in sample 1.
- Keep API keys in environment variables.

## Checked

Checked 2026-11-07 against the Elysia documentation source (integrations/ai-sdk.html); each claim, option name and default was compared with the page text. Removed an invented curl Verify step.

Method: documentation only; no commands were run.
