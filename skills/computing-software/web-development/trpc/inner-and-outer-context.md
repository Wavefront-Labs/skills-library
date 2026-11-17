---
id: computing-software.web-development.trpc.inner-and-outer-context
name: inner-and-outer-context
category: computing-software
field: web-development
product: trpc
tags: [trpc, context, createcontextinner, testing, session]
level: advanced
status: docs-checked
description: "Split context into an inner part (db, session, no request needed) and an outer part (req and res) so tests and server-side calls work without HTTP."
sources:
  - https://github.com/trpc/trpc/blob/main/www/v11/docs/server/context.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
For some apps, split `createContext` in two functions.

Inner context defines things that do not depend on the request, such as the database connection. It is usable in integration tests and server-side calls with no request object, and whatever it defines is always available in procedures.

Outer context defines request-dependent things such as the user's session, and only exists for procedures called over HTTP.

```ts
export async function createContextInner(opts?: { session: Session | null }) {
  return { db, session: opts?.session };
}

export async function createContext(opts: CreateHTTPContextOptions) {
  const session = getSessionFromCookie(opts.req);
  const contextInner = await createContextInner({ session });
  return { ...contextInner, req: opts.req, res: opts.res };
}

export type Context = Awaited<ReturnType<typeof createContextInner>>;
```

Important: infer the `Context` type from the inner function, because only what is defined there is truly always available. If a procedure needs `req` or `res`, make a small reusable procedure that throws when they are missing and then overwrites the context with the truthy values via `opts.next({ ctx: { req: opts.ctx.req, res: opts.ctx.res } })`.

Tradeoff noted in the docs: putting a very large generated client (Prisma) on the inner context can increase type-checking overhead because it becomes part of every procedure's context type. If that is noticeable, import the client directly where needed.

## Checked

2026-11-04: read in full against the tRPC docs repo (trpc/trpc, docs repo www/v11/docs/): server/context.md (Inner and outer context). Every parameter name, default, error string and code sample left in this skill appears on those pages. Removed: nothing; no Verify step was present.

Method: documentation only; no commands were run.
