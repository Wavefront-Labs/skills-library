---
id: computing-software.software-engineering.typescript.mocking-the-network-with-msw
name: mocking-the-network-with-msw
category: computing-software
field: software-engineering
product: typescript
tags: [typescript, msw, mock-service-worker, api-mocking, vitest, network-mocking, testing-library]
level: practitioner
status: docs-checked
description: "Mock HTTP at the network layer with Mock Service Worker: shared handlers for Node tests and browser, per-test overrides, error and delay cases, unhandled-request policy."
sources:
  - https://github.com/mswjs/mswjs.io/blob/main/src/content/docs/migrations/2.x-to-3.x.md
  - https://github.com/mswjs/mswjs.io/blob/main/src/content/api/setup-server/listen.md
  - https://github.com/mswjs/mswjs.io/blob/main/src/content/api/setup-server/use.md
  - https://github.com/mswjs/mswjs.io/blob/main/src/content/api/setup-worker/start.md
  - https://github.com/mswjs/mswjs.io/blob/main/src/content/api/cli/init.md
  - https://github.com/mswjs/mswjs.io/blob/main/src/content/api/http.md
  - https://github.com/mswjs/mswjs.io/blob/main/src/content/api/delay.md
  - https://github.com/mswjs/mswjs.io/blob/main/src/content/docs/http/mocking-responses/network-errors.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mocking the network with MSW

**Goal:** tests and local dev that exercise your real fetch/axios code paths against
controlled responses, instead of mocking the HTTP client module.

## Handlers (shared)
```ts
// src/mocks/handlers.ts
import { http, HttpResponse } from "msw/http";   // MSW 3.x entrypoints (2.x: everything from "msw")
import { delay } from "msw/utils/delay";          // used in the per-test examples below
export const handlers = [
  http.get("/api/users/:id", ({ params }) => HttpResponse.json({ id: params.id, name: "Ada" })),
  http.post("/api/orders", async ({ request }) => {
    const body = (await request.json()) as { items: unknown[] };
    if (!body.items.length) return HttpResponse.json({ title: "empty order" }, { status: 422 });
    return HttpResponse.json({ id: "o-1" }, { status: 201 });
  }),
];
```

## Node (Vitest/Jest)
```ts
// test/setup.ts
import { setupServer } from "msw/node";
export const server = setupServer(...handlers);
beforeAll(() => server.listen({ onUnhandledFrame: "error" }));   // unhandled requests fail tests (3.x name; 2.x: onUnhandledRequest)
afterEach(() => server.resetHandlers());                           // drop per-test overrides
afterAll(() => server.close());
```
`setupServer` configures the interception of requests in a Node.js process; MSW 3.x requires Node.js 22 or newer.

## Per-test scenarios
```ts
test("shows error banner on 500", async () => {
  server.use(http.get("/api/users/:id", () => HttpResponse.json({}, { status: 500 })));
  render(<Profile id="1" />);
  expect(await screen.findByRole("alert")).toHaveTextContent(/try again/i);
});
server.use(http.get("/api/slow", async () => { await delay(2000); return HttpResponse.json({}); }));
server.use(http.get("/api/down", () => HttpResponse.error()));      // network failure
server.use(http.get("/api/once", () => HttpResponse.json({ a: 1 }), { once: true }));
```

## Browser (dev and Storybook)
```bash
npx msw init public/ --save          # copies mockServiceWorker.js
```
```ts
if (import.meta.env.DEV && import.meta.env.VITE_MOCKS === "1") {
  const { setupWorker } = await import("msw/browser");
  await setupWorker(...handlers).start({ onUnhandledFrame: "bypass" });
}
```
## Practices
- Keep handlers close to the real API contracts and back them with contract tests.
- Assert on UI/behaviour, not that a handler was called; if you must, collect requests in the
  handler.
- Use absolute URLs in Node if your code does (`http.get("https://api.example.org/...")`).

## Verify
- [ ] `onUnhandledFrame: "error"` (2.x: `onUnhandledRequest`) in test setup.
- [ ] Handlers reset after each test; error, empty and slow states each have a test.

## Checked
Checked 2026-10-25 against the mswjs.io documentation repository (MSW 3.x; latest release 3.0.3). Confirmed: 3.x moved `http`/`HttpResponse` to `msw/http` and `delay` to `msw/utils/delay`; `setupServer` stays in `msw/node` and `setupWorker` in `msw/browser`; `onUnhandledRequest` was renamed `onUnhandledFrame` (default `"warn"`, also `"error"` and `"bypass"`) for both `server.listen()` and `worker.start()`; Node.js 22 is the minimum; the `once` handler option; `HttpResponse.error()` for network errors; `server.resetHandlers()` and `server.close()`; `npx msw init <dir> --save`. Removed the unconfirmed client-compatibility claim, the DevTools remark and the named OpenAPI generators. The skill previously used 2.x import paths and option names.
Method: documentation only; no commands were run.
