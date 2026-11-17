---
id: computing-software.web-development.hono.hono-streaming-helper
name: hono-streaming-helper
category: computing-software
field: web-development
product: hono
tags: [hono, helper, streaming, sse]
level: practitioner
status: docs-checked
description: "Stream responses in Hono with stream, streamText and streamSSE, abort handling, per-stream error handlers and the Wrangler Identity encoding fix."
sources:
  - https://github.com/honojs/website/blob/main/docs/helpers/streaming.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Streaming helper

Import: `import { stream, streamText, streamSSE } from 'hono/streaming'`.

## stream
```ts
app.get('/stream', (c) =>
  stream(c, async (stream) => {
    stream.onAbort(() => console.log('Aborted!'))
    await stream.write(new Uint8Array([0x48, 0x65, 0x6c, 0x6c, 0x6f]))
    await stream.pipe(anotherReadableStream)
  })
)
```

## streamText
Sends `Content-Type: text/plain`, `Transfer-Encoding: chunked`, `X-Content-Type-Options: nosniff`.

```ts
streamText(c, async (stream) => {
  await stream.writeln('Hello') // with newline
  await stream.sleep(1000)
  await stream.write(`Hono!`)    // without newline
})
```

On Cloudflare Workers under Wrangler, if streaming misbehaves, call `c.header('Content-Encoding', 'Identity')` before `streamText`.

## streamSSE
```ts
app.get('/sse', (c) =>
  streamSSE(c, async (stream) => {
    while (!stream.aborted) {
      await stream.writeSSE({
        data: `It is ${new Date().toISOString()}`,
        event: 'time-update',
        id: String(id++),
      })
      await stream.sleep(1000)
    }
  })
)
```

## Error handling
The optional third argument is `(err, stream) => {...}`; without it the error goes to `console.error`:

```ts
stream(c, async (stream) => { /* ... */ }, (err, stream) => {
  stream.writeln('An error occurred!')
  console.error(err)
})
```
The stream closes automatically after callbacks.

## Gotcha
If the streaming callback throws, Hono's `app.onError` is NOT triggered: the stream has already started, so the response cannot be overwritten. Use the third-argument handler.

## Checked
2026-11-04: every claim left was read in the honojs/website docs page helpers/streaming.md. Removed: the invented Verify step.
Method: documentation only; no commands were run.
