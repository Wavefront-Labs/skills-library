---
id: computing-software.web-development.trpc.error-formatting-zod-errors
name: error-formatting-zod-errors
category: computing-software
field: web-development
product: trpc
tags: [trpc, errorformatter, zod, zoderror, flatten]
level: practitioner
status: docs-checked
description: "Add a flattened ZodError to the error shape with errorFormatter and read it, typed, on the client for field-level form errors."
sources:
  - https://github.com/trpc/trpc/blob/main/www/v11/docs/server/error-formatting.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Error formatting in your router is inferred all the way to the client. A common use is surfacing Zod field errors:

```ts
export const t = initTRPC.create({
  errorFormatter(opts) {
    const { shape, error } = opts;
    return {
      ...shape,
      data: {
        ...shape.data,
        zodError:
          error.code === 'BAD_REQUEST' && error.cause instanceof ZodError
            ? error.cause.flatten()
            : null,
      },
    };
  },
});
```

On the client (React example from the docs):

```tsx
const mutation = trpc.addPost.useMutation();
if (mutation.error?.data?.zodError) {
  // zodError will be inferred
  return <pre>Error: {JSON.stringify(mutation.error.data.zodError, null, 2)}</pre>;
}
```

The check on `error.code === 'BAD_REQUEST'` plus `error.cause instanceof ZodError` matters: an input validation failure is a `BAD_REQUEST` whose `cause` is the error your validator threw.

Properties passed to `errorFormatter`: `error` (TRPCError), `type`, `path`, `input`, `ctx` and `shape`. The example spreads `...shape` and `...shape.data` to keep the default fields.

## Checked

2026-11-04: read in full against the tRPC docs repo (trpc/trpc, docs repo www/v11/docs/): server/error-formatting.md, server/validators.md (cause of the BAD_REQUEST). Every parameter name, default, error string and code sample left in this skill appears on those pages. Removed: the invented Verify step and the claim that flatten() output maps onto form libraries.

Method: documentation only; no commands were run.
