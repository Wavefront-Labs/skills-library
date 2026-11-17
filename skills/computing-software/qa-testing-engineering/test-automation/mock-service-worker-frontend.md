---
id: computing-software.qa-testing-engineering.test-automation.mock-service-worker-frontend
name: mock-service-worker-frontend
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [msw, mock-service-worker, service-virtualization, network-mocking, frontend-testing, jest, vitest, storybook]
level: practitioner
status: verified
description: "Mock network calls in front-end tests and development with Mock Service Worker: handlers shared by unit tests, Storybook and the browser, with per-test overrides."
sources:
  - https://mswjs.io/docs/
  - https://mswjs.io/docs/integrations/node
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mock Service Worker (MSW)

**Goal:** one set of API mocks reused across unit/component tests (Node), Storybook and local development (browser), intercepting at the network level so app code is untouched.

## Handlers (MSW 2.x and 3.x)
MSW 3.0 (released 2026-09-28) is ESM-only, needs Node 22+, and renames `onUnhandledRequest` to `onUnhandledFrame` (see the Node section); the handler code below ran unchanged on msw 3.0.3 with vitest.
```ts
// mocks/handlers.ts
import { http, HttpResponse, delay } from 'msw'
export const handlers = [
  http.get('/api/products', () => HttpResponse.json([{ id: 1, name: 'Coffee' }])),
  http.post('/api/orders', async ({ request }) => {
    const body = await request.json()
    return HttpResponse.json({ id: 99, ...body }, { status: 201 })
  }),
]
```

## Node (Vitest/Jest)
```ts
import { setupServer } from 'msw/node'
export const server = setupServer(...handlers)
beforeAll(() => server.listen({ onUnhandledFrame: 'error' }))   // MSW 2.x: onUnhandledRequest
afterEach(() => server.resetHandlers())
afterAll(() => server.close())

test('shows error when orders fail', async () => {
  server.use(http.post('/api/orders', () => new HttpResponse(null, { status: 500 })))
  // render, act, assert error message
})
```

## Browser
`npx msw init public/` then `setupWorker(...handlers).start()` in dev mode only; Storybook via `msw-storybook-addon`.

## Gotchas
- `onUnhandledFrame: 'error'` (MSW 3; `onUnhandledRequest` in 2.x) catches unmocked calls instead of silently hitting real servers. On msw 3.0.3, passing the old `onUnhandledRequest: 'error'` was silently ignored: an unmocked `fetch` to a local server returned the real response, while `onUnhandledFrame` made it throw `[MSW] Cannot bypass a request when using the "error" strategy`. After upgrading, check this with one deliberately unmocked request.
- In MSW 3 `request.headers.get('cookie')` is `null` in handlers (use the `cookies` argument) and fake timers are no longer bypassed (advance them for `delay()`); `msw/native` is gone (use `@msw/react-native`), per the v3.0.0 release notes.
- Jest with jsdom needs fetch/TextEncoder polyfills for MSW 2 (or use Vitest/`jest-fixed-jsdom`).
- Relative URLs in Node need a base URL: `fetch('/api/products')` throws `Failed to parse URL from /api/products` before MSW sees it; use absolute URLs in handlers and the client, or a jsdom/browser environment with a base URL.

## Verify
Tests pass with network disabled, and removing a handler makes the relevant test fail with an unhandled request error.
