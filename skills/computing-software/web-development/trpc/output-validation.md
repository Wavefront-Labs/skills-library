---
id: computing-software.web-development.trpc.output-validation
name: output-validation
category: computing-software
field: web-development
product: trpc
tags: [trpc, output, validation, internal-server-error, zod]
level: practitioner
status: docs-checked
description: "Add .output() to check untrusted data and strip extra fields; a failing output validator returns INTERNAL_SERVER_ERROR."
sources:
  - https://github.com/trpc/trpc/blob/main/www/v11/docs/server/validators.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
tRPC infers return types automatically, so output validation is not always as important as input validation; the docs list two reasons to add it: checking data returned from untrusted sources, and making sure you do not return more data to the client than necessary.

```ts
export const appRouter = t.router({
  hello: publicProcedure
    .output(z.object({ greeting: z.string() }))
    .query(() => {
      return { greeting: 'hello world' };
    }),
});
```

Behavior to know:

- If output validation fails, the server responds with `INTERNAL_SERVER_ERROR` .
- The client receives the value your output validator returns. A schema that strips unknown keys (like `z.object()`) also strips them from the response.
- Subscriptions are async iterators; the same techniques apply (see the subscriptions guide's output validation section).

Because the return type is inferred from the validator's output, changing the schema changes the client's type.

## Checked

2026-11-07. Read in full from a clone of github.com/trpc/trpc (main, commit fe64009), www/v11/docs/server/validators.md (read in full): the Output Validators section, the info note on INTERNAL_SERVER_ERROR, the sentence that the client receives the validator return value and unknown keys are stripped by z.object(), and the subscription output validation pointer.

Removed or corrected: the password-hash leak claim, the "fault is yours" gloss, the unsourced per-call cost advice, and the invented Verify step.

Method: documentation only; no commands were run.
