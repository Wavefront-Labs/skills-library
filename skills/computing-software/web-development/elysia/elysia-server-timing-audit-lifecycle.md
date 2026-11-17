---
id: computing-software.web-development.elysia.elysia-server-timing-audit-lifecycle
name: elysia-server-timing-audit-lifecycle
category: computing-software
field: web-development
product: elysia
tags: [server-timing, performance, plugin, lifecycle]
level: intro
status: docs-checked
description: "Add the Server-Timing header to Elysia responses with @elysia/server-timing to find slow lifecycle stages, with enabled, trace and allow options."
sources:
  - https://elysiajs.com/plugins/server-timing.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: see how long each lifecycle stage takes in the browser's Network > Timing tab.

1. Install: `bun add @elysia/server-timing`
2. Use it:

```typescript
import { Elysia } from 'elysia'
import { serverTiming } from '@elysia/server-timing'

new Elysia()
    .use(serverTiming())
    .get('/', () => 'hello')
    .listen(3000)
```

The plugin appends a `Server-Timing` header holding duration, function name and detail for each lifecycle function. Inspect via browser developer tools > Network > select the request > Timing.

Config:
- `enabled` (default `NODE_ENV !== 'production'`): off in production by default.
- `allow` (default undefined): a condition deciding whether timing is logged for a request.
- `trace` (default undefined): choose which events to log. Keys: `request`, `parse`, `transform`, `beforeHandle`, `handle`, `afterHandle`, `total` (start to finish).

Disable timing on one path with `allow`:

```ts
serverTiming({
    allow: ({ request }) => new URL(request.url).pathname !== '/no-trace'
})
```

Gotchas:
- Because `enabled` defaults to non-production only, you will not see the header in a production build unless you set `enabled: true`.

## Checked

Checked 2026-11-07 against the Elysia documentation source (plugins/server-timing.html); each claim, option name and default was compared with the page text. Removed the invented Verify step.

Method: documentation only; no commands were run.
