---
id: computing-software.web-development.appwrite.appwrite-functions-write-handler
name: appwrite-functions-write-handler
category: computing-software
field: web-development
product: appwrite
tags: [appwrite, functions, context, runtime, serverless]
level: practitioner
status: docs-checked
description: "Write an Appwrite Function using the context object for requests, responses and logging, and read trigger headers."
sources:
  - https://github.com/appwrite/website/blob/main/src/routes/docs/products/functions/develop/+page.markdoc
  - https://github.com/appwrite/website/blob/main/src/routes/docs/products/functions/functions/+page.markdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: understand the handler contract.

Each execution follows a request and response pattern. The executor of the active deployment passes request information through the `context.req` object of your exported entrypoint function, your code runs, and the function ends when you return a result such as `return context.res.text()` or `return context.res.json()`. All input, output and logging must go through the `context` object, which has:
- `req`: method, body, headers and other request data.
- `res`: methods to build the response.
- `log()` and `error()`: log information or errors to the Appwrite Console; end users cannot see them.

Request body accessors: `req.bodyText` (text converted from binary), `req.bodyJson` (body text parsed as JSON) and `req.bodyBinary` (the binary body). Deprecated: use `req.bodyText` instead of `req.bodyRaw`, `res.text` instead of `res.send`, and `req.bodyText` or `req.bodyJson` instead of `req.body`.

Response methods: `empty` (204 No Content), `json` (stringifies and sets content-type `application/json`), `binary`, `redirect` (to a URL) and `text` (UTF-8 encoded).

Headers always sent with an execution:
- `x-appwrite-trigger`: `http`, `schedule` or `event`.
- `x-appwrite-event`: the triggering event, for event executions.
- `x-appwrite-key`: a dynamic API key.
- `x-appwrite-user-id`: set when an authenticated user invoked the function (not Console users or API keys).
- `x-appwrite-user-jwt`: a JWT from the invoking user's session, for authenticating Server SDKs so user permissions are respected.
- `x-appwrite-country-code`, `x-appwrite-continent-code`, `x-appwrite-continent-eu`, `x-appwrite-client-ip`, `x-appwrite-execution-id`.

Using Appwrite inside the function: add the SDK to the function's dependencies. The dynamic API key is generated per execution, works only inside Appwrite functions, arrives in `x-appwrite-key` and acts as an admin-type role; set its scopes under Settings > Scopes and grant only what is needed. During builds it is the `APPWRITE_FUNCTION_API_KEY` environment variable. To act as the caller instead, use the `x-appwrite-user-jwt` header so only resources that user can access are reachable.

Gotcha: to protect user privacy, request and response objects are not logged to the Console by default, so log what you need explicitly.

## Checked

2026-11-04. Confirmed against the Appwrite docs page Develop Appwrite Functions (functions/develop), read from the raw markdown because the rendered page was truncated: lifecycle, the context object, request and response tables, deprecation notice, the header table, dynamic API key and JWT sections, and the logging note. Removed: the claim that user headers appear only via `createExecution`, the per-method status-code and header arguments, and the Verify step; the Node example was dropped because the page's code samples could not be matched line by line.
Method: documentation only; no commands were run.
