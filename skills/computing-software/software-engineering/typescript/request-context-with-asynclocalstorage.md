---
id: computing-software.software-engineering.typescript.request-context-with-asynclocalstorage
name: request-context-with-asynclocalstorage
category: computing-software
field: software-engineering
product: typescript
tags: [typescript, asynclocalstorage, request-context, correlation-id, async-hooks, nodejs, logging-context]
level: advanced
status: gated
description: "Carry request-scoped context (request ID, user, tenant) across async calls in Node with AsyncLocalStorage: middleware, logging integration and context-loss pitfalls."
sources: ["https://nodejs.org/api/async_context.html", "https://nodejs.org/api/async_context.html#class-asynclocalstorage", "https://getpino.io/#/docs/child-loggers"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Request context with AsyncLocalStorage

**Goal:** every log line and downstream call carries the request ID and tenant without
threading a `ctx` parameter through every function.

## Setup
```ts
import { AsyncLocalStorage } from "node:async_hooks";
import { randomUUID } from "node:crypto";

type Ctx = { requestId: string; userId?: string; tenant?: string };
export const als = new AsyncLocalStorage<Ctx>();
export const ctx = () => als.getStore();

// Express / Connect middleware
app.use((req, res, next) => {
  const requestId = req.get("x-request-id") ?? randomUUID();
  res.set("x-request-id", requestId);
  als.run({ requestId }, next);          // everything called from next() sees the store
});
```
Fastify: register in an `onRequest` hook with `als.enterWith` or use `@fastify/request-context` (the package exists on npm, v7.0.2; the Fastify integration itself was not run) (gated: unconfirmed, source is paywalled or blocked).

## Logging integration
```ts
import pino from "pino";
export const log = pino({
  mixin: () => ({ requestId: ctx()?.requestId, tenant: ctx()?.tenant }),   // evaluated per log call
});
```
Every `log.info(...)` anywhere in the request now carries the IDs, with no logger passed around.

## Propagating downstream
```ts
await fetch(url, { headers: { "x-request-id": ctx()?.requestId ?? "" } });
```
OpenTelemetry's Node SDK uses AsyncLocalStorage internally for trace context (the `@opentelemetry/context-async-hooks` README lists an `AsyncLocalStorageContextManager`); if you use OTel,
prefer its context/baggage APIs over a second store.

## Pitfalls
- **Context loss**: callbacks registered outside the request (connection-pool events, custom
  thenables, some old callback libraries) run in the context where they were created. Wrap with
  `AsyncResource.bind(fn)` or `AsyncLocalStorage.bind(fn)`.
- **Mutating shared objects**: the store object is shared by everything in that request
  context; set fields early, treat as read-mostly.
- `enterWith` changes the context for the rest of the synchronous execution and its async
  descendants - leaks into unrelated work if misused; prefer `run`.
- Event emitters: listeners run in the context of whoever calls `emit` (tested: a listener registered under `EMIT` saw `OTHER` when emitted from another context); use `EventEmitterAsyncResource` or `AsyncLocalStorage.bind`/`AsyncResource.bind` (both bound the creation-time store in a test).
- Overhead is small in modern Node (AsyncContextFrame in Node 24 lowered it further: it is the default in 24, `--no-async-context-frame` opts out per the CLI docs), but
  don't create stores per call.

## Testing
In an Express 5.3 test app with two concurrent requests, pino's `mixin` logged `A` and `B` with no cross-contamination.

```ts
await als.run({ requestId: "t-1" }, async () => {
  await handler();
  expect(logged[0].requestId).toBe("t-1");
});
```

## Verify
- [ ] Logs for one request (including from DB and HTTP client callbacks) all carry the same requestId.
- [ ] Concurrent load test shows no requestId cross-contamination.
