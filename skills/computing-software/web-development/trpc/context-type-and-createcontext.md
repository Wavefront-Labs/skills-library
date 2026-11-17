---
id: computing-software.web-development.trpc.context-type-and-createcontext
name: context-type-and-createcontext
category: computing-software
field: web-development
product: trpc
tags: [trpc, context, createcontext, inittrpc, authentication]
level: practitioner
status: docs-checked
description: "Define the context type with initTRPC.context and supply createContext to the adapter; it runs once per request and is shared by batched calls."
sources:
  - https://github.com/trpc/trpc/blob/main/www/v11/docs/server/context.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Context holds data every procedure can read, typically authentication info. Setup has two steps.

1. Define the type during initialization by piping `.context<TContext>()` before `.create()`. The type can be inferred from a function's return type:

```ts
export const createContext = async (opts: CreateHTTPContextOptions) => {
  const token = opts.req.headers['authorization'];
  return { token };
};
export type Context = Awaited<ReturnType<typeof createContext>>;
const t = initTRPC.context<Context>().create();
```

2. Pass `createContext` to the handler that mounts your router, for example `createHTTPHandler({ router: appRouter, createContext })`.

`createContext()` is called once per request, so all procedures inside one batched HTTP request share the same context object. The same context type is then available inside procedures and middlewares (`opts.ctx`).

In the docs example `createContext` returns a nullable `user` (a real app would verify the token there), and `protectedProcedure = t.procedure.use(...)` throws `UNAUTHORIZED` when `ctx.user?.email` is missing and returns a non-nullable `user` through `opts.next({ ctx: { user: opts.ctx.user } })`.

## Checked

2026-11-04: read in full against the tRPC docs repo (trpc/trpc, docs repo www/v11/docs/): server/context.md (Defining the context type, Creating the context, Example code). Every parameter name, default, error string and code sample left in this skill appears on those pages. Removed: the invented Verify step and the 'typically verifies the token in createContext or a middleware' generalisation.

Method: documentation only; no commands were run.
