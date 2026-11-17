---
id: computing-software.web-development.hono.hono-timeout-middleware
name: hono-timeout-middleware
category: computing-software
field: web-development
product: hono
tags: [hono, middleware, timeout, http-exception]
level: practitioner
status: docs-checked
description: "Enforce request time limits in Hono with timeout, custom HTTPException factories, and the workaround needed for streaming and SSE."
sources:
  - https://github.com/honojs/website/blob/main/docs/middleware/builtin/timeout.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Timeout middleware

Import: `import { timeout } from 'hono/timeout'`.

```ts
app.use('/api/*', timeout(5000)) // 5 seconds, milliseconds
app.get('/api/data', async (c) => c.json({ data: 'Your data here' }))
```

## Custom exception
Pass a second argument: an `HTTPException` instance or a factory function that receives the context.

```ts
import { HTTPException } from 'hono/http-exception'

const customTimeoutException = (context) =>
  new HTTPException(408, {
    message: `Request timeout after waiting ${context.req.header('Duration')} seconds. Please try again later.`,
  })

app.use('/api/long-process', timeout(60000, customTimeoutException))
```

Prefer a factory when errors go to an observability service, so each timeout has a fresh stack:

```ts
timeout(5000, () => new HTTPException(504, { message: 'Gateway Timeout' }))
```

Passing an instance reuses its construction-time stack for every timeout, which affects stack attribution and fingerprinting.

## Streaming gotcha
The timeout middleware cannot be used with streams. Combine `stream.close()` with `setTimeout`:

```ts
return streamSSE(c, async (stream) => {
  timer = setTimeout(() => stream.close(), 3000) as unknown as number
  stream.onAbort(async () => { running = false; clearTimeout(timer) })
  while (running) {
    await stream.writeSSE({ data: message, event: 'time-update', id: String(id++) })
    await stream.sleep(1000)
  }
})
```

## Ordering
Be careful with order relative to error-handling or other timing-related middleware.

## Checked
2026-11-04: every claim left was read in the honojs/website docs page middleware/builtin/timeout.md. Removed: the invented Verify step.
Method: documentation only; no commands were run.
