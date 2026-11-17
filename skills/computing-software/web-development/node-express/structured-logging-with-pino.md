---
id: computing-software.web-development.node-express.structured-logging-with-pino
name: structured-logging-with-pino
category: computing-software
field: web-development
product: node-express
tags: [express, pino, structured-logging, pino-http, request-id, redaction, asynclocalstorage, observability, web-development]
level: practitioner
status: verified
description: "Structured JSON logging for Express with pino and pino-http: request ids, child loggers, redaction, error serialisation, log levels and transports."
sources:
  - https://getpino.io/#/
  - https://github.com/pinojs/pino-http
  - https://getpino.io/#/docs/redaction
  - https://nodejs.org/api/async_context.html#class-asynclocalstorage
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Structured logging with pino

**Goal:** JSON logs with a request id on every line, no secrets, and negligible overhead.

## 1. Setup
```js
import pino from "pino";
import pinoHttp from "pino-http";
import { randomUUID } from "node:crypto";

export const logger = pino({
  level: process.env.LOG_LEVEL ?? "info",
  redact: { paths: ["req.headers.authorization", "req.headers.cookie", "password", "token", "*.password", "*.token"], censor: "[redacted]" },   // "*.x" covers one level only: a top-level `password` key needs its own path
  base: { service: "orders-api", env: process.env.NODE_ENV },
  timestamp: pino.stdTimeFunctions.isoTime,
});

app.use(pinoHttp({
  logger,
  genReqId: (req, res) => {
    const id = req.headers["x-request-id"] ?? randomUUID();
    res.setHeader("x-request-id", id);
    return id;
  },
  customLogLevel: (req, res, err) => err || res.statusCode >= 500 ? "error" : res.statusCode >= 400 ? "warn" : "info",
  autoLogging: { ignore: (req) => req.url === "/healthz" },
}));
```

## 2. Use the request logger
```js
app.post("/orders", async (req, res) => {
  req.log.info({ orderId }, "order created");      // every line carries req.id (pino-http binds `req`, not `reqId`)
});
```
Message last, object first: `log.info({ userId }, "msg")`. Don't string-interpolate data into messages - fields must stay queryable.

## 3. Correlation beyond req
Deep in services without `req`, use AsyncLocalStorage:
```js
const als = new AsyncLocalStorage();
app.use((req, res, next) => als.run({ log: req.log }, next));
export const log = () => als.getStore()?.log ?? logger;
```
Or pino's `mixin()` to add trace ids from OpenTelemetry.

## 4. Errors
`logger.error({ err }, "payment failed")` - the `err` key uses pino's serializer (`type`, `message`, `stack`; `cause` when present). Logging `{ error: e }` gives `{}` (both checked with pino 10.4).

## 5. Output and transports
- Production: write JSON to stdout; let the platform (Docker, systemd-journald, Kubernetes, Vector/Fluent Bit) ship it. No file rotation in the app.
- Development: `node app.js | pino-pretty` or `transport: { target: "pino-pretty" }` (transports run in a worker thread).
- Never use `pino-pretty` in production (slow, unparseable).

## 6. Levels
`fatal > error > warn > info > debug > trace`. Info for business events and request summaries; debug for diagnostics, off in production; change at runtime via env/flag.

## Verify
- [ ] Every log line from a request has the same `req.id` (pino-http 11 output; there is no top-level `reqId` unless you add it), also returned as `x-request-id`.
- [ ] `grep -i authorization` in logs shows only `[redacted]`.
- [ ] Error logs include stack traces; no `console.log` left (`grep -rn console.log src`).
