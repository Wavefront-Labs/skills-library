---
id: computing-software.software-engineering.typescript.unhandled-rejections-and-process-errors
name: unhandled-rejections-and-process-errors
category: computing-software
field: software-engineering
product: typescript
tags: [typescript, nodejs, node-runtime, unhandled-rejection, uncaughtexception, graceful-shutdown, process-signals, error-handling]
level: practitioner
status: gated
description: "Handle Node process-level failures: unhandled promise rejections, uncaughtException, crash-and-restart policy, SIGTERM graceful shutdown and floating-promise lint rules."
sources:
  - https://nodejs.org/api/process.html#event-unhandledrejection
  - https://nodejs.org/api/process.html#event-uncaughtexception
  - https://nodejs.org/api/cli.html#--unhandled-rejectionsmode
  - https://typescript-eslint.io/rules/no-floating-promises/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Unhandled rejections and process error handling

**Goal:** errors are never silently lost, a corrupted process exits and restarts, and deployments shut down cleanly.

## 1. Defaults
- Since Node 15, an unhandled promise rejection **crashes** the process (`--unhandled-rejections=throw` is the default per the Node CLI docs; tested, exit code 1). Good: keep it. With `--unhandled-rejections=warn` it only printed `UnhandledPromiseRejectionWarning` and exited 0 (tested).
- `uncaughtException` after a synchronous throw outside any handler: the process state is undefined. Log and exit; do not resume.

## 2. Last-resort handlers
```ts
process.on("unhandledRejection", (reason) => {
  logger.fatal({ err: reason }, "unhandled rejection");
  throw reason;                       // escalate to uncaughtException path
});
process.on("uncaughtException", (err, origin) => {
  logger.fatal({ err, origin }, "uncaught exception");
  logger.flush?.();
  process.exit(1);                     // let the supervisor (k8s, systemd, pm2) restart us
});
```
Use these only for logging and exit. Do not use them as a general error-handling mechanism. (Tested: the `throw reason` in the first handler reached the `uncaughtException` handler with origin `uncaughtException`, and the process exited 1.)

## 3. Prevent floating promises at the source
```ts
// BAD: rejection unhandled, caller does not wait
saveAudit(evt);
// GOOD
await saveAudit(evt);
void saveAudit(evt).catch(err => logger.warn({ err }, "audit failed"));   // deliberate fire-and-forget
```
Enable typescript-eslint `no-floating-promises` and `no-misused-promises` (the rule docs list `array.forEach(async ...)` and async listeners passed to `addEventListener` as violations of `checksVoidReturn`).
Express 4 does not catch rejected async handlers (tested on 4.x: the rejection reached `unhandledRejection` and the request never got a response); wrap them or use Express 5, which forwards rejections to error middleware (tested on 5.3: the error middleware replied `handled:async fail`).

## 4. EventEmitter errors
An `error` event with no listener throws (tested). Every stream, socket and client emitter needs an `error` listener (or use `pipeline`/`events.once` which handle it).

## 5. Graceful shutdown
```ts
const server = app.listen(port);
let shuttingDown = false;
async function shutdown(signal: string) {
  if (shuttingDown) return; shuttingDown = true;
  logger.info({ signal }, "shutting down");
  server.close();                                  // stop accepting; finish in-flight requests
  server.closeIdleConnections?.();
  const timer = setTimeout(() => process.exit(1), 25_000).unref();
  await Promise.allSettled([db.end(), queue.close()]);
  clearTimeout(timer);
  process.exit(0);
}
process.on("SIGTERM", () => void shutdown("SIGTERM"));
process.on("SIGINT", () => void shutdown("SIGINT"));
```
Kubernetes sends SIGTERM then SIGKILL after `terminationGracePeriodSeconds` (30 s default; Kubernetes pod-lifecycle docs); finish before that. Fail readiness first so the load balancer stops routing.

## Gotchas
- Running `node` as PID 1 in a container: signals still reach Node, but `npm start` as PID 1 may not forward them. Use `node` directly or `--init`/tini (gated: unconfirmed, source is paywalled or blocked; no running container daemon to test).
- `process.exit()` right after `logger.error` can drop async log writes; flush or use synchronous destinations for fatal logs.
- `--unhandled-rejections=warn` or `none` hides bugs; never set them in production.

## Verify
- A test script with an unawaited rejecting promise exits non-zero with a logged stack; `kill -TERM <pid>` during a slow request lets it complete before exit.
