---
id: computing-software.web-development.elysia.call-eden-treaty-with-parameters-and-handle-responses
name: call-eden-treaty-with-parameters-and-handle-responses
category: computing-software
field: web-development
product: elysia
tags: [elysia, eden-treaty-parameters, eden-treaty-response, eden-treaty-websocket, file-upload, stream]
level: practitioner
status: docs-checked
description: "Send body, query, headers and files with Eden Treaty, narrow data and error from the response, consume streams and use subscribe for WebSocket routes."
sources:
  - https://elysiajs.com/eden/treaty/parameters.html
  - https://elysiajs.com/eden/treaty/response.html
  - https://elysiajs.com/eden/treaty/websocket.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: call Elysia routes from a typed client and handle every outcome.

## Parameters

Methods take (1) body, (2) additional options `{ query, headers, fetch }`, all type-checked.

```typescript
api.user.post({ name: 'Elysia' }, { headers: { authorization: 'Bearer 12345' }, query: { id: 2 } })
```

GET and HEAD have no body: the only argument is the options object (`api.hello.get({ headers: { hello: 'world' } })`). If the body is not needed but query or headers are, pass `null` or `undefined`: `api.user.post(null, { query: { name: 'Ely' } })`. Fetch settings go under `fetch`, e.g. `{ fetch: { signal: controller.signal } }` for cancellation.

## File upload

Pass `File`, `File[]`, `FileList` or `Blob`; content-type becomes `multipart/form-data`:

```typescript
await api.image.post({ title: 'Misono Mika', image: input.files! })   // server: image: t.Files()
```

## Response

Each call resolves to `{ data, error, response, status, headers }`. `data` holds a 2xx body; `error` holds a response with status 300 or above (then `data` is `null`). Until you handle `error`, `data` is nullable.

```typescript
const { data, error } = await api.user.post({ name })
if (error) switch (error.status) { case 400: throw error.value; default: throw error.value }
return data   // narrowed to string
```

Types: `Treaty.Data<typeof api.user.post>` and `Treaty.Error<typeof api.user.post>` (or pass a response).

## Streams and SSE

A generator or SSE route comes back as an `AsyncGenerator`: `for await (const chunk of data) ...`.

## WebSocket

For an `.ws('/chat', {...})` route use `subscribe` (same params as `get`/`head`):

```typescript
const chat = api.chat.subscribe()
chat.subscribe((message) => console.log('got', message))
chat.on('open', () => chat.send('hello from client'))
```

It returns EdenWS, which extends the WebSocket API; `.raw` exposes the native WebSocket.

## Gotchas

- Check `error` before using `data`; in the docs example the server returns `status(400)`, and Eden narrows the error type from the server's declared responses.

## Checked

Checked 2026-11-07 against the Elysia documentation source (eden/treaty/parameters.html, eden/treaty/response.html, eden/treaty/websocket.html); each claim, option name and default was compared with the page text. Reworded the error-narrowing gotcha to what the page shows.

Method: documentation only; no commands were run.
