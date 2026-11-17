---
id: computing-software.web-development.node-express.express-routing-middleware-and-errors
name: express-routing-middleware-and-errors
category: computing-software
field: web-development
product: node-express
tags: [node, nodejs, express, express5, express4, middleware, router, routing, rest-api, async-errors, error-handling, error-middleware, express-async-errors, validation, zod, helmet, cors, body-parser, express-json, payload-limit, trust-proxy, rate-limiting, graceful-shutdown, sigterm, event-loop, worker-threads, fastify, javascript, web-development, express-router, express-error-handling, express-5]
level: practitioner
status: verified
description: "Express apps on Node: middleware order, Router, async error handling in Express 4 vs 5, 4-arg error middleware, validation, helmet/cors, body limits, trust proxy, graceful shutdown."
sources:
  - https://expressjs.com/en/guide/routing.html
  - https://expressjs.com/en/guide/error-handling.html
  - https://expressjs.com/en/advanced/best-practice-security.html
  - https://nodejs.org/en/learn
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Express routing, middleware and errors — order is the architecture

**Goal:** an Express service where every request passes through middleware in a
deliberate order, every error (sync or async) reaches one handler, and the process
shuts down without dropping requests.

## 1. Middleware order (top to bottom is execution order)
```js
import express from 'express';
import helmet from 'helmet';
import cors from 'cors';

const app = express();
app.set('trust proxy', 1);                       // behind exactly one proxy/load balancer
app.disable('x-powered-by');
app.use(helmet());                               // security headers
app.use(cors({ origin: ['https://app.example.com'], credentials: true }));
app.use(express.json({ limit: '100kb' }));       // explicit body limit
app.use(requestId);                              // logging context
app.get('/healthz', (req, res) => res.send('ok'));
app.use('/api/orders', authenticate, ordersRouter);
app.use((req, res) => res.status(404).json({ error: 'Not found' }));  // after all routes
app.use(errorHandler);                           // last, 4 arguments
app.listen(process.env.PORT ?? 3000);
```
- A middleware must call `next()` **or** send a response — never both, never neither (the request hangs).
- `trust proxy`: set the hop count (or the proxy subnet), not `true`; with `true`, any client can spoof `X-Forwarded-For` and defeat IP rate limiting. Without it, `req.ip` and `req.secure` are wrong behind a load balancer.
- `cors()` with no options allows every origin; `origin: '*'` with `credentials: true` makes the `cors` package send both headers (`Access-Control-Allow-Origin: *` and `Access-Control-Allow-Credentials: true`), which browsers reject for credentialed requests; list the origins instead.

## 2. Routers
```js
const router = express.Router({ mergeParams: true });
router.param('id', loadOrder);                   // runs once for routes using :id
router.get('/', listOrders);
router.get('/:id', getOrder);
router.post('/', validate(orderSchema), createOrder);
export default router;
```
Express 5 changed path syntax (path-to-regexp v8): wildcards must be named (`/*splat`), the
optional `?` suffix became braces (`/:file{.:ext}`), and inline regex in paths is gone. Old
Express 4 patterns throw at startup.

## 3. Async errors: Express 4 vs 5
**Express 5** (5.0.0, September 2024): a handler returning a rejected promise is forwarded to
`next(err)` automatically.

**Express 4**: a rejected promise is an unhandled rejection: on Node 15+ it crashes the process by default, and if you install an `unhandledRejection` handler the request hangs. Wrap:
```js
const ah = fn => (req, res, next) => Promise.resolve(fn(req, res, next)).catch(next);
router.get('/:id', ah(async (req, res) => {
  const order = await db.orders.find(req.params.id);
  if (!order) throw new HttpError(404, 'Order not found');
  res.json(order);
}));
```
(or `import 'express-async-errors'` once). Errors thrown in callbacks/timers after the
handler returns are not caught by either version — promisify them.

## 4. The error handler
```js
function errorHandler(err, req, res, next) {      // MUST declare 4 params
  if (res.headersSent) return next(err);          // delegate to Express default
  const status = err.status ?? err.statusCode ?? 500;
  req.log?.error({ err }, 'request failed');
  res.status(status).json({
    error: status < 500 ? err.message : 'Internal server error',   // no stack traces to clients
  });
}
```
Express identifies error middleware by `fn.length === 4` — dropping the unused `next`
turns it into normal middleware. `express.json()` errors arrive here with `status` 400 or 413.

## 5. Validate at the edge
```js
const validate = schema => (req, res, next) => {
  const r = schema.safeParse(req.body);
  if (!r.success) return res.status(400).json({ errors: r.error.issues });
  req.body = r.data; next();
};
```
Validate `params` and `query` too; in Express 5 `req.query` is a getter, so store parsed
values elsewhere (e.g. `res.locals`) rather than reassigning it.

## 6. Don't block the event loop
One CPU-bound request stalls every other request. Avoid sync APIs in handlers
(`fs.readFileSync`, `crypto.pbkdf2Sync`, giant `JSON.parse`), catastrophic regexes on user
input, and unbounded loops. Move heavy work to `worker_threads` or a job queue; stream large
files. Monitor event-loop lag (`perf_hooks.monitorEventLoopDelay`).

## 7. Graceful shutdown
```js
const server = app.listen(port);
server.keepAliveTimeout = 65_000;   // above the load balancer's idle timeout (check yours)
process.on('SIGTERM', () => {
  server.close(async () => { await db.end(); process.exit(0); });  // stop accepting, finish in-flight
  server.closeIdleConnections?.();
  setTimeout(() => process.exit(1), 10_000).unref();               // hard deadline
});
```
Fail `/readyz` first so the orchestrator stops routing traffic before you close.

## Verify
- [ ] An async handler that throws returns your JSON 500, not a hang (test on your Express major).
- [ ] Unknown routes give 404 JSON; the error handler has 4 params and is registered last.
- [ ] Oversized body → 413; malformed JSON → 400.
- [ ] `req.ip` shows the real client behind your proxy, and spoofed `X-Forwarded-For` is ignored.
- [ ] `kill -TERM` during a slow request lets it finish, then the process exits.
