---
id: computing-software.web-development.node-express.trpc-typed-apis
name: trpc-typed-apis
category: computing-software
field: web-development
product: node-express
tags: [trpc, end-to-end-type-safety, zod, tanstack-query, typescript-api, api-design]
level: practitioner
status: verified
description: "Building end-to-end typed APIs with tRPC v11: routers and procedures with zod input, auth middleware, adapters, batching client, TanStack Query integration and when not to use it."
sources:
  - https://trpc.io/docs
  - https://trpc.io/docs/server/middlewares
  - https://trpc.io/docs/client/tanstack-react-query/setup
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# tRPC typed APIs

tRPC shares TypeScript types between server and client without code generation. Best for a TS monorepo where you own both ends; not for public/third-party APIs (use REST + OpenAPI or GraphQL).

## 1. Server
```ts
import { initTRPC, TRPCError } from "@trpc/server";
import superjson from "superjson";
import { z } from "zod";
const t = initTRPC.context<{ user: User | null }>().create({ transformer: superjson });
const protectedProcedure = t.procedure.use(({ ctx, next }) => {
  if (!ctx.user) throw new TRPCError({ code: "UNAUTHORIZED" });
  return next({ ctx: { user: ctx.user } });          // narrows type for downstream
});
export const appRouter = t.router({
  post: t.router({
    byId: t.procedure.input(z.object({ id: z.string().uuid() })).query(({ input }) => db.post.find(input.id)),
    create: protectedProcedure.input(z.object({ title: z.string().min(1).max(200) }))
      .mutation(({ input, ctx }) => db.post.create({ ...input, authorId: ctx.user.id })),
  }),
});
export type AppRouter = typeof appRouter;
```
Adapters: Express (`createExpressMiddleware`), Next.js (fetch adapter in a route handler), standalone, Fastify, AWS Lambda.

## 2. Client
```ts
import { createTRPCClient, httpBatchLink } from "@trpc/client";
import type { AppRouter } from "../server/router";     // type-only import: no server code bundled
const trpc = createTRPCClient<AppRouter>({ links: [httpBatchLink({ url: "/api/trpc", transformer: superjson })] });
const post = await trpc.post.byId.query({ id });
```
React: `@trpc/tanstack-react-query` gives `trpc.post.byId.queryOptions({ id })` to pass to `useQuery`, with typed cache keys and invalidation.

Ran on @trpc/server and @trpc/client 11.19.0, superjson 2.2.6, zod 4.6.7, Express 5.3.0, TypeScript 7.0.2: Date and Map survived the wire; an unauthenticated mutation returned `UNAUTHORIZED` (HTTP 401); a non-uuid id returned `BAD_REQUEST` whose message holds the zod issues (a separate `zodError` field exists only if you add an `errorFormatter`); `ctx.user` was narrowed in the protected mutation; two concurrent `httpBatchLink` queries made 1 request (`batch=1` in the URL) and 2 with `httpLink`; a misspelled input field failed `tsc`. In zod 4 `z.string().uuid()` still works but `z.uuid()` is the current form. `@trpc/tanstack-react-query` `queryOptions` comes from `createTRPCOptionsProxy({ client, queryClient })` (ran: returns `queryKey`, `queryFn`).

## 3. Practices
- Validate every input with zod (types alone are compile-time only).
- Authorise per object in procedures, not only "logged in".
- Map errors to `TRPCError` codes; use an `errorFormatter` to hide internals.
- `superjson` keeps Dates/Maps intact across the wire (same transformer on both ends).
- Batching combines concurrent calls into one HTTP request; use `httpLink` for endpoints that must be cacheable by URL.

## Verify
- [ ] Renaming a field on the server breaks the client type-check; unauthenticated mutation returns UNAUTHORIZED; invalid input returns BAD_REQUEST with zod details.
