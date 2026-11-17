---
id: computing-software.web-development.hono.hono-server-timing
name: hono-server-timing
category: computing-software
field: web-development
product: hono
tags: [hono, middleware, performance, server-timing]
level: practitioner
status: docs-checked
description: "Emit Server-Timing headers in Hono with timing, setMetric, startTime, endTime and wrapTime, plus enabled and crossOrigin options."
sources:
  - https://github.com/honojs/website/blob/main/docs/middleware/builtin/timing.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Server-Timing middleware

Import: `import { timing, setMetric, startTime, endTime, wrapTime } from 'hono/timing'` and `import type { TimingVariables } from 'hono/timing'`.

```ts
const app = new Hono<{ Variables: TimingVariables }>()
app.use(timing())

app.get('/', async (c) => {
  setMetric(c, 'region', 'europe-west3')
  setMetric(c, 'custom', 23.8, 'My custom Metric') // value in milliseconds
  startTime(c, 'db')
  const data = await db.findMany(...)
  endTime(c, 'db')
  // or: const data = await wrapTime(c, 'db', db.findMany(...))
  return c.json({ response: data })
})
```

## Conditional
```ts
app.use('*', timing({ enabled: (c) => c.req.method === 'POST' }))
```

## Options
- `total: boolean`: show total time, default `true`; `totalDescription` default `Total Response Time`.
- `enabled: boolean | (c) => boolean`, default `true`.
- `autoEnd: boolean`: end `startTime()` timers at request end; if disabled, timers not manually ended are not shown.
- `crossOrigin: boolean | string | (c) => boolean | string`: the origin the timings header is readable from. `false` (default) same origin only; `true` all; a string lists domains separated with commas.

## Gotcha
On Cloudflare Workers timers only advance on I/O, so timings may be inaccurate. `setMetric` custom timings must be in milliseconds.

## Checked
2026-11-04: every claim left was read in the honojs/website docs page middleware/builtin/timing.md. Removed: the invented Verify step and the Timing-Allow-Origin header name.
Method: documentation only; no commands were run.
