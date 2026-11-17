---
id: computing-software.web-development.node-express.problem-details-error-responses
name: problem-details-error-responses
category: computing-software
field: web-development
product: node-express
tags: [rest-api, problem-details, rfc-9457, error-handling, api-design, express]
level: practitioner
status: verified
description: "Returning consistent API errors with RFC 9457 Problem Details: fields, application/problem+json, validation error extensions, status code choice, and not leaking internals."
sources:
  - https://www.rfc-editor.org/rfc/rfc9457
  - https://www.rfc-editor.org/rfc/rfc9110#name-status-codes
  - https://swagger.io/blog/problem-details-rfc9457-doing-api-errors-well/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Error responses with RFC 9457 Problem Details

## 1. Format
```http
HTTP/1.1 422 Unprocessable Content
Content-Type: application/problem+json

{
  "type": "https://api.example.com/problems/insufficient-funds",
  "title": "Insufficient funds",
  "status": 422,
  "detail": "Balance is 30.00 EUR; the transfer needs 50.00 EUR.",
  "instance": "/transfers/req-7f3a",
  "balance": "30.00",
  "errors": null
}
```
- `type`: URI identifying the problem type (documentation page); defaults to `about:blank` when absent, meaning "no semantics beyond the HTTP status", and then `title` SHOULD be the standard status phrase (`Not Found`, `Unprocessable Content`) (RFC 9457 section 4.2.1).
- `title`: short, stable per type (SHOULD NOT change per occurrence, except for localisation). `detail`: occurrence-specific, human-readable. `instance`: identifies this occurrence (request id/URI).
- Extension members allowed (`balance`, `errors`, `trace_id`). RFC 9457 obsoletes RFC 7807 (same format, adds a registry and multiple-problem guidance).

## 2. Validation errors
```json
{ "type": "https://api.example.com/problems/validation", "title": "Request validation failed", "status": 400,
  "errors": [ { "pointer": "/items/0/qty", "detail": "must be at least 1" }, { "pointer": "/email", "detail": "invalid format" } ] }
```
Use JSON Pointers for body fields (RFC 9457's own example writes them as URI fragments, `"pointer": "#/profile/color"`; the bare `/profile/color` form is what the sample above uses) and a `parameter` member for query params (a convention, not defined by the RFC). The RFC's validation example is a 422 response. Return all errors at once.

## 3. Express error handler
The handler below was run: it answers `application/problem+json; charset=utf-8`. With `type: "about:blank"` the `title` should be the status phrase, so set `err.type`/`err.title` for your own problem types.
```js
app.use((err, req, res, next) => {
  const status = err.status ?? 500;
  const body = status >= 500
    ? { type: "about:blank", title: "Internal Server Error", status, instance: req.id }        // no stack traces
    : { type: err.type ?? "about:blank", title: err.title ?? err.message, status, detail: err.detail, instance: req.id, ...err.extensions };
  if (status >= 500) req.log.error({ err, reqId: req.id }, "unhandled");
  res.status(status).type("application/problem+json").json(body);
});
```

## 4. Status codes
400 malformed/validation, 401 unauthenticated (with `WWW-Authenticate`), 403 forbidden, 404 not found (also for resources the caller may not know exist), 405 + `Allow`, 409 conflict/state, 412 precondition failed (ETag), 415 unsupported media type, 422 semantically invalid, 429 + `Retry-After`, 500 bug, 502/503/504 upstream/unavailable/timeouts. Never 200 with `{ "error": ... }`.

## 5. Security
No stack traces, SQL, internal hostnames or library versions in errors; don't distinguish "user not found" vs "wrong password" on auth endpoints. Include a request id so support can find logs.

## Verify
Contract tests assert content type and fields for representative 4xx/5xx; production 500 bodies contain no stack traces; OpenAPI documents the problem schema per operation.
