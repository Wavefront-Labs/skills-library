---
id: computing-software.web-development.appwrite.appwrite-functions-execution-triggers
name: appwrite-functions-execution-triggers
category: computing-software
field: web-development
product: appwrite
tags: [appwrite, functions, execution, events, cron, scheduling]
level: practitioner
status: docs-checked
description: "Run functions by HTTP, SDK, events, cron schedules or delayed executions and understand sync versus async limits."
sources:
  - https://github.com/appwrite/website/blob/main/src/routes/docs/products/functions/execute/+page.markdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: choose the right trigger.

Execution modes:
- Synchronous: Appwrite calls the runtime and waits; the client gets the response body and headers directly. Created by Create execution with `async: false`, or by requests to a generated or custom domain. Hard timeout of 30 seconds.
- Asynchronous: queued and run by the function worker as a background job, with no timeout limit beyond the function's configured timeout. Created by Create execution with `async: true`, by event triggers, and by scheduled executions (cron or delayed). Response bodies and headers are not stored anywhere, so they only come back from synchronous executions.

Ways to execute:
- Domain/HTTP: set Execute access to `Any`, then call the generated domain (Domains tab) or a custom domain. Request URL, headers and body are passed to the function; use the `x-appwrite-user-jwt` header to authenticate users. Domain executions are unauthenticated, so callers are guests.
- SDK: `functions.createExecution({ functionId, body, async, xpath, method, headers })` (all but `functionId` optional). Client SDKs need an account with execute permission on the function; Server SDKs need an API key with the right scopes.
- Console: Execute now mocks path, method, headers and body.
- Events: Settings tab > Events, add one or more events. The triggering event arrives in the `x-appwrite-event` header and the event data in the request body.
- Schedule: cron expressions in the function settings, as frequently as every minute (`*/15 * * * *` every 15 minutes, `0 * * * *` hourly, `0 0 * * *` daily at 00:00, `0 0 * * 1` Mondays at 00:00).
- Delayed execution: runs once at a future time. Console: your function > Executions > Execute now > Schedule. SDK: `createExecution` with `async: true` and `scheduledAt` as an ISO 8601 timestamp such as `2020-10-15T06:38:00.000+00:00`; scheduled executions must be async.

Gotcha: do not select events the function itself can cause, or it triggers its own execution in an infinite recursion.

## Checked

2026-11-04. Confirmed against the Appwrite docs page Execution (functions/execute), read from the raw markdown because the rendered page was truncated: the two modes and their creators, the 30-second sync limit, async queueing, the response-storage note, domains and Execute access `Any`, the `createExecution` parameters, Console steps, the `x-appwrite-event` header, cron granularity and examples, `scheduledAt`, and the permissions section. Removed: the Verify step and the claim that triggers show as "schedule" or "event" in the Executions tab.
Method: documentation only; no commands were run.
