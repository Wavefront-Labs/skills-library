---
id: computing-software.web-development.trpc.input-validation
name: input-validation
category: computing-software
field: web-development
product: trpc
tags: [trpc, input, validation, zod, bad-request]
level: intro
status: docs-checked
description: "Validate procedure input with .input(); failures return BAD_REQUEST before the resolver runs and the validator types opts.input automatically."
sources:
  - https://github.com/trpc/trpc/blob/main/www/v11/docs/server/validators.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Define an input validator with `procedure.input()`. tRPC checks the call and returns a validation error if it is wrong, and it infers the resolver's `opts.input` type from the validator. Validators are read through the Standard Schema interface when available, or custom interfaces for supported libraries.

```ts
export const appRouter = t.router({
  hello: publicProcedure
    .input(z.object({ name: z.string() }))
    .query((opts) => {
      return { greeting: `Hello ${opts.input.name}` };
    }),
});
```

If validation fails the procedure does not run and the call fails with a `BAD_REQUEST` error whose `cause` is the error your validator threw. To send structured validation errors (for example Zod field errors) to the client, use the error formatter (see `computing-software.web-development.trpc.error-formatting-zod-errors`).

Zod is the docs' default recommendation: strong ecosystem and usable in many parts of a codebase. Any Standard Schema library also works.

## Checked

2026-11-04: read in full against the tRPC docs repo (trpc/trpc, docs repo www/v11/docs/): server/validators.md (Input Validators, Zod). Every parameter name, default, error string and code sample left in this skill appears on those pages. Removed: the invented Verify step and the unsupported tip about validating at the edge.

Method: documentation only; no commands were run.
