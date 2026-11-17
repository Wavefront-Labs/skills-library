---
id: computing-software.web-development.trpc.adapter-onerror-handling
name: adapter-onerror-handling
category: computing-software
field: web-development
product: trpc
tags: [trpc, onerror, error-handling, logging, adapter]
level: practitioner
status: docs-checked
description: "Use the adapter onError callback to log or report every procedure error with its error, type, path, input, ctx and req before it reaches the client."
sources:
  - https://github.com/trpc/trpc/blob/main/www/v11/docs/server/error-handling.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
All errors that occur in a procedure pass through the adapter's `onError` before being sent to the client. This is the place to log or report; to change what the client sees use the error formatter instead.

```ts
const server = createHTTPServer({
  router: appRouter,
  onError(opts) {
    const { error, type, path, input, ctx, req } = opts;
    console.error('Error:', error);
    if (error.code === 'INTERNAL_SERVER_ERROR') {
      // send to bug reporting
    }
  },
});
```

The `opts` object contains `error` (a `TRPCError`), `type` (`query`, `mutation`, `subscription` or `unknown`), `path` (string or undefined), `input` (unknown), `ctx` (unknown) and `req` (the Request).

`onError` receives the full error, including its `cause`, while the error formatter controls what the client sees, so internal detail can be logged here even if the formatter hides it from users.

For server-side callers, `createCaller` accepts an equivalent `onError` option (see the server-side calls skill). The caller still throws after the handler runs.

## Checked

2026-11-04: read in full against the tRPC docs repo (trpc/trpc, docs repo www/v11/docs/): server/error-handling.md (Handling errors, Secure error reporting), server/server-side-calls.md (Error handling). Every parameter name, default, error string and code sample left in this skill appears on those pages. Removed: the invented Verify step and the unsupported 'send only INTERNAL_SERVER_ERROR / redacted input as tags' recipe.

Method: documentation only; no commands were run.
