---
id: computing-software.web-development.trpc.throwing-trpcerror
name: throwing-trpcerror
category: computing-software
field: web-development
product: trpc
tags: [trpc, trpcerror, throw, cause, error-handling]
level: practitioner
status: docs-checked
description: "Throw TRPCError with a fitting code, message and optional cause; other thrown errors become INTERNAL_SERVER_ERROR with the original as cause."
sources:
  - https://github.com/trpc/trpc/blob/main/www/v11/docs/server/error-handling.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`TRPCError` is the error subclass for failures inside procedures and middleware.

```ts
const appRouter = t.router({
  hello: t.procedure.query(() => {
    throw new TRPCError({
      code: 'INTERNAL_SERVER_ERROR',
      message: 'An unexpected error occurred, please try again later.',
      // optional: pass the original error to retain stack trace
      cause: theError,
    });
  }),
});
```

This results in a response with `message`, JSON-RPC `code: -32603`, and `data` containing `code: 'INTERNAL_SERVER_ERROR'`, `httpStatus: 500`, `path: 'hello'` and a dev-only `stack`.

Guidance from the docs: throw a `TRPCError` with the code that fits (`NOT_FOUND`, `FORBIDDEN`) so the client gets the right HTTP status. Any other error thrown in a procedure or middleware becomes an `INTERNAL_SERVER_ERROR` with the original error as its `cause`.

Warning: the `message` of an error you did not throw as a `TRPCError` is still sent to the client, in production too. If your errors can include internal details (for example table names, queries or file paths from a database driver), hide them with an error formatter.

Pass `cause` to retain the original error's stack trace, as the page's snippet comment says.

## Checked

2026-11-07. Read in full from a clone of github.com/trpc/trpc (main, commit fe64009), www/v11/docs/server/error-handling.md (read in full): "Throwing errors" with the snippet and response (code -32603, httpStatus 500, path, stack), the guidance and warning paragraphs, and "Stack traces in production" for the dev-only stack.

Removed or corrected: the claim that `cause` lets `onError` and the formatter recognise the original class (for example ZodError), which is not on the page, and the invented Verify step.

Method: documentation only; no commands were run.
