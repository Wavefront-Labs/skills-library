---
id: computing-software.qa-testing-engineering.vitest.mock-network-msw
name: mock-network-msw
category: computing-software
field: qa-testing-engineering
product: vitest
tags: [msw, mock-service-worker, mock-network, on-unhandled-request]
level: practitioner
status: docs-checked
description: "Mock HTTP, GraphQL and WebSocket requests in Vitest with Mock Service Worker in a setup file, failing on unhandled requests and resetting handlers per test."
sources:
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/guide/mocking/requests.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Vitest recommends Mock Service Worker (MSW), which intercepts requests without changing application code. Put the server in a `setupFiles` entry.

```ts
import { afterAll, afterEach, beforeAll } from 'vitest'
import { setupServer } from 'msw/node'
import { http, HttpResponse } from 'msw'

const restHandlers = [
  http.get('https://rest-endpoint.example/path/to/posts', () => {
    return HttpResponse.json([{ id: 1, title: 'first post title' }])
  }),
]

const server = setupServer(...restHandlers)

beforeAll(() => server.listen({ onUnhandledRequest: 'error' }))
afterAll(() => server.close())
afterEach(() => server.resetHandlers())
```

- `onUnhandledRequest: 'error'` makes MSW throw an error whenever a request has no corresponding handler.
- `server.resetHandlers()` after each test gives test isolation.
- GraphQL uses `graphql.query('Name', ...)`; WebSockets use `ws.link(url)` with `addEventListener('connection', ...)`.
- In Node (and so Vitest) MSW relies on `@mswjs/interceptors`; in a real browser it uses a Service Worker.

## Checked

2026-11-04. Confirmed against guide/mocking/requests.md: MSW recommendation, setup-file placement, the HTTP, GraphQL and WebSocket setups, `onUnhandledRequest: 'error'`, resetHandlers per test, and the interceptors versus Service Worker note. Removed: a gotcha about mocking fetch by hand that the page does not state.

Method: documentation only; no commands were run.
