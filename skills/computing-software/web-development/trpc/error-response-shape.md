---
id: computing-software.web-development.trpc.error-response-shape
name: error-response-shape
category: computing-software
field: web-development
product: trpc
tags: [trpc, error, json-rpc, error-shape, httpstatus]
level: intro
status: docs-checked
description: "The JSON shape of a tRPC error response (message, JSON-RPC code, data.code, httpStatus, path, stack) and when the stack is included."
sources:
  - https://github.com/trpc/trpc/blob/main/www/v11/docs/server/error-handling.md
  - https://github.com/trpc/trpc/blob/main/www/v11/docs/server/error-formatting.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
When a procedure fails, tRPC answers with an object that has an `error` property carrying everything the client needs. An example from a bad request:

```json
{
  "id": null,
  "error": {
    "message": "\"password\" must be at least 4 characters",
    "code": -32600,
    "data": {
      "code": "BAD_REQUEST",
      "httpStatus": 400,
      "stack": "...",
      "path": "user.changepassword"
    }
  }
}
```

The top-level `code` is a JSON-RPC 2.0 number (tRPC is compliant with JSON-RPC 2.0); `data.code` is the tRPC code name; `httpStatus` is the HTTP status the response uses; `path` is the procedure that threw; `stack` appears only in development.

In TypeScript this is `DefaultErrorShape`: `{ message: string; code: TRPC_ERROR_CODE_NUMBER; data: { code: TRPC_ERROR_CODE_KEY; httpStatus: number; path?: string; stack?: string } }`. Custom error formatting extends this shape and the extension is inferred on the client.

`error.data.stack` is only included when `isDev` is true; `initTRPC.create()` sets `isDev` to `process.env.NODE_ENV !== 'production'`. Override `isDev` for deterministic behaviour across runtimes.

## Checked

2026-11-04: read in full against the tRPC docs repo (trpc/trpc, docs repo www/v11/docs/): server/error-handling.md, server/error-formatting.md (DefaultErrorShape). Every parameter name, default, error string and code sample left in this skill appears on those pages. Removed: the invented Verify step.

Method: documentation only; no commands were run.
