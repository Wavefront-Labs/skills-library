---
id: computing-software.web-development.trpc.input-merging
name: input-merging
category: computing-software
field: web-development
product: trpc
tags: [trpc, input, merging, base-procedure, zod]
level: practitioner
status: docs-checked
description: "Stack .input() calls to merge object inputs across a base procedure and its children, and know the rules for precedence and optional inputs."
sources:
  - https://github.com/trpc/trpc/blob/main/www/v11/docs/server/validators.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`.input()` can be chained to build bigger input types. This is useful when a collection of procedures shares input that a middleware needs.

Merging works by spreading object properties together, which has three consequences from the docs:

- Only object types can be chained; non-object types such as `z.string()` cannot be merged.
- If two chained `.input()` calls define the same property, the later one takes precedence.
- An optional input (for example `z.object({...}).optional()`) can only be chained after another optional input.

```ts
const baseProcedure = t.procedure
  .input(z.object({ townName: z.string() }))
  .use((opts) => {
    console.log(`Handling request with user from: ${opts.input.townName}`);
    return opts.next();
  });

export const appRouter = t.router({
  hello: baseProcedure
    .input(z.object({ name: z.string() }))
    .query((opts) => {
      const input = opts.input; // { townName: string; name: string }
      return { greeting: `Hello ${input.name}, my friend from ${input.townName}` };
    }),
});
```

The middleware sees only the fields parsed so far, and the final resolver sees the union.


## Checked

2026-11-04: read in full against the tRPC docs repo (trpc/trpc, docs repo www/v11/docs/): server/validators.md (Input Merging). Every parameter name, default, error string and code sample left in this skill appears on those pages. Removed: the invented Verify step and the bare-string-id pitfall.

Method: documentation only; no commands were run.
