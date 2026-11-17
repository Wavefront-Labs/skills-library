---
id: computing-software.web-development.node-express.asynclocalstorage-context-propagation
name: asynclocalstorage-context-propagation
category: computing-software
field: web-development
product: node-express
tags: [asynclocalstorage-context, async-context-propagation, request-context, async-hooks, node]
level: advanced
status: verified
description: "Propagating request context in Node with AsyncLocalStorage: request ids and user context for logging, Express middleware setup, context loss pitfalls, performance and testing."
sources:
  - https://nodejs.org/api/async_context.html
  - https://nodejs.org/api/async_context.html#class-asynclocalstorage
  - https://github.com/tc39/proposal-async-context
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# AsyncLocalStorage context propagation

AsyncLocalStorage (stable, `node:async_hooks`) keeps a value available across `await`s, callbacks and promise chains started within a `run()` call - like thread-local storage for async code. Use it for request ids, tenant/user context in logs, and tracing; not as a hidden dependency-injection container for business logic.

## 1. Setup
```js
// context.js
import { AsyncLocalStorage } from "node:async_hooks";
export const als = new AsyncLocalStorage();
export const ctx = () => als.getStore() ?? {};

// app.js
import { randomUUID } from "node:crypto";
app.use((req, res, next) => {
  const requestId = req.get("x-request-id") ?? randomUUID();
  res.set("x-request-id", requestId);
  als.run({ requestId, userId: undefined }, next);      // everything downstream sees this store
});
app.use(authenticate, (req, res, next) => { ctx().userId = req.user?.id; next(); });  // mutate the same object
```
```js
// logger.js - pino mixin adds context to every line
export const logger = pino({ mixin: () => ({ requestId: ctx().requestId, userId: ctx().userId }) });
```

## 2. Context loss pitfalls
- Code started **outside** `run()` (module-level timers, connection pools created before the request, event emitters registered at startup) won't see the store when its callbacks fire (a plain callback queued inside `run()` and called later from outside returns `undefined`; wrapped with `AsyncResource.bind` it returns the captured store). An `EventEmitter` listener sees the context of whoever calls `emit`, not of whoever registered it. Libraries that queue work and call back later from a shared context lose it - wrap callbacks with `AsyncResource.bind(fn)` or `AsyncLocalStorage.bind(fn)`.
- `als.enterWith()` changes context for the rest of the synchronous execution and can leak into unrelated work; prefer `run()`.
- Middleware that calls `next()` from a different async context (some older body parsers) can break propagation; place the ALS middleware first and test.

## 3. Performance
Node 24 reimplemented AsyncLocalStorage on `AsyncContextFrame` and uses it by default (24.0.0 release notes; opt out with `--no-async-context-frame`); the semantics tested here were identical on Node 20 and 24. Node 22 has it only behind a flag. Overhead on older versions is a few percent in promise-heavy code - measure if hot.

## 4. Frameworks
- Fastify: `@fastify/request-context`. NestJS: `nestjs-cls`. Next.js uses ALS internally for `headers()`/`cookies()`.
- OpenTelemetry's Node context manager is built on ALS - your store and OTel context coexist.

## 5. Testing
```js
test("logs include request id", async () => {
  await als.run({ requestId: "t-1" }, async () => { await handler(); expect(lastLog().requestId).toBe("t-1"); });
});
```

## Verify
- [ ] Every log line within a request carries its request id, including lines from DB callbacks and after awaits; concurrent requests never see each other's ids (load test with parallel requests).
## Checked
Run on Windows with Node 20.20.2 and 24.22.0 (same output): store survives `await`, timers, `setImmediate` and `nextTick`; mutating the store object from later middleware is visible to earlier code; 50 concurrent HTTP requests each saw their own store (0 mismatches); `AsyncLocalStorage.bind` and `AsyncResource.bind` capture the store; `enterWith` in a function leaks to the rest of that async chain. Fetched: Node 24.0.0 release notes (AsyncContextFrame default) and the CLI docs for `--no-async-context-frame`. Not run: pino mixin, Fastify/Nest/OpenTelemetry integration, performance claims (not measured), the test snippet (uses a framework `expect`), Node 22.
Linux pass (Node 20.20.2 musl): identical output to Windows for every ALS check above.
