---
id: computing-software.web-development.elysia.stream-responses-and-server-sent-events
name: stream-responses-and-server-sent-events
category: computing-software
field: web-development
product: elysia
tags: [elysia, handler, stream, sse, generator, formdata, file]
level: practitioner
status: docs-checked
description: "Stream an Elysia response with generator functions, emit Server-Sent Events with sse, return files and FormData, and consume streams through Eden."
sources:
  - https://elysiajs.com/essential/handler.html
  - https://elysiajs.com/eden/treaty/response.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: stream data to the client, send SSE events, or return files and multipart bodies.

## Stream with yield

A generator handler streams out of the box:

```typescript
new Elysia().get('/ok', function* () {
	yield 1
	yield 2
	yield 3
})
```

## Server-Sent Events

Wrap values in `sse`; Elysia sets `text/event-stream` and formats the event.

```typescript
import { Elysia, sse } from 'elysia'

new Elysia().get('/sse', function* () {
	yield sse('hello world')
	yield sse({ event: 'message', data: { message: 'hi', timestamp: new Date().toISOString() } })
})
```

## Rules

- Headers can be set only before the first chunk is yielded (`set.headers['x-name'] = 'Elysia'` before `yield 1` works; after it does nothing).
- Conditional stream: if the function returns without yielding (`if (Math.random() > 0.5) return 'ok'`), Elysia sends a normal response.
- If the client cancels mid-stream, Elysia stops the generator automatically.

## Files and FormData

```typescript
import { Elysia, form, file } from 'elysia'

new Elysia()
	.get('/', () => form({ name: 'Tea Party', images: [file('nagi.web'), file('mika.webp')] }))
	.get('/single', file('nagi.web'))
```

`form()` returns a FormData; `file()` returns one file directly without `form`.

## Consume with Eden Treaty

Eden types a stream or SSE response as an `AsyncGenerator`:

```typescript
const { data, error } = await treaty(app).ok.get()
if (error) throw error
for await (const chunk of data) console.log(chunk)
```

For SSE, a final `sse({ event: 'end' })` can mark the end of the stream.

## Checked

2026-11-07. Read in full: essential/handler (Formdata, Return a file, Stream, SSE, Headers in SSE, Conditional Stream, Automatic cancellation, Eden) and eden/treaty/response (Stream response). Confirmed generator streaming, `sse`, `text/event-stream`, header timing, conditional stream, cancellation, `form` and `file`, and the Treaty `AsyncGenerator` handling. Nothing removed.

Method: documentation only; no commands were run.
