---
id: computing-software.web-development.trpc.server-side-call-error-handling
name: server-side-call-error-handling
category: computing-software
field: web-development
product: trpc
tags: [trpc, createcaller, error-handling, trpcerror, onerror]
level: practitioner
status: docs-checked
description: "Handle errors from server-side callers: TRPCError instances, getHTTPStatusCodeFromError for custom endpoints, and the createCaller onError option."
sources:
  - https://github.com/trpc/trpc/blob/main/www/v11/docs/server/server-side-calls.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A procedure called through a caller throws its error as a `TRPCError`; errors that were not thrown as one become `INTERNAL_SERVER_ERROR` with the original as `cause`. This lets a custom endpoint forward the right status:

```ts
const caller = appRouter.createCaller({});
try {
  const postResult = await caller.post.byId({ id: postId });
  res.status(200).json({ data: { postTitle: postResult.title } });
} catch (cause) {
  if (cause instanceof TRPCError) {
    // the specific HTTP status from tRPC, e.g. 404 for NOT_FOUND
    const httpStatusCode = getHTTPStatusCodeFromError(cause);
    res.status(httpStatusCode).json({ error: { message: cause.message } });
    return;
  }
  res.status(500).json({ error: { message: `Error while accessing post with ID ${postId}` } });
}
```

`createCaller` also takes a second argument with an `onError` handler (for logging or reporting) and a `signal` which procedures receive as `opts.signal`. The handler gets `ctx`, `error`, `path`, `input` and `type`, like an error formatter minus the shape; the caller still throws after it runs.

```ts
const caller = router.createCaller({}, {
  onError: (opts) => console.error('An error occurred:', opts.error),
});
```

The docs note that tRPC already creates API endpoints for you, so this pattern is for custom endpoints that need to call a procedure.

## Checked

2026-11-07. Read in full from a clone of github.com/trpc/trpc (main, commit fe64009), www/v11/docs/server/server-side-calls.md (read in full): the Next.js API endpoint example, the "Error handling" section (TRPCError, INTERNAL_SERVER_ERROR with cause, onError, signal as opts.signal, handler arguments, throws after the handler runs) and the tip that tRPC already creates endpoints. Every claim matched the page text.

Removed or corrected: the invented Verify step; no other claim needed changing.

Method: documentation only; no commands were run.
