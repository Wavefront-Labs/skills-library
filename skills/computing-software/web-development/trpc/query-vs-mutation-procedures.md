---
id: computing-software.web-development.trpc.query-vs-mutation-procedures
name: query-vs-mutation-procedures
category: computing-software
field: web-development
product: trpc
tags: [trpc, query, mutation, procedure, resolver]
level: intro
status: docs-checked
description: "Choose between query, mutation and subscription procedure types and write the resolver with opts.input and opts.ctx."
sources:
  - https://github.com/trpc/trpc/blob/main/www/v11/docs/server/procedures.md
  - https://github.com/trpc/trpc/blob/main/www/v11/docs/server/validators.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A procedure is a function exposed to the client. There are three kinds: a `query` (fetch data, generally no changes), a `mutation` (send data, usually create/update/delete) and a `subscription` (streaming, see the subscriptions skills).

```ts
const appRouter = router({
  // Queries are the best place to fetch data
  hello: publicProcedure.query(() => {
    return { message: 'hello world' };
  }),

  // Mutations are the best place to do things like updating a database
  goodbye: publicProcedure.mutation(async (opts) => {
    await opts.ctx.signGuestBook();
    return { message: 'goodbye!' };
  }),
});
```

The resolver receives a single `opts` object. Use `opts.ctx` for context (auth, db), `opts.input` for validated input, and the return value becomes the typed response. Procedures use an immutable builder pattern, which is what lets you create reusable base procedures.

Per the page, a query generally does not change data and a mutation is often used for create, update or delete.

## Checked

2026-11-07. Read in full from a clone of github.com/trpc/trpc (main, commit fe64009), www/v11/docs/server/procedures.md (read in full): the three procedure kinds and their descriptions, the hello/goodbye snippet and the immutable builder statement; opts.input is shown in www/v11/docs/server/validators.md (read in full).

Removed or corrected: the GET/POST mapping and React Query caching remark (neither is on the cited page), the claim about each builder call returning a new builder (only "immutable builder pattern" is stated), and the invented Verify step about .query()/.mutate().

Method: documentation only; no commands were run.
