---
id: computing-software.web-development.trpc.context-in-http-caller-and-ssr-helpers
name: context-in-http-caller-and-ssr-helpers
category: computing-software
field: web-development
product: trpc
tags: [trpc, context, createcaller, server-side-helpers, adapters]
level: practitioner
status: docs-checked
description: "The three places a context is supplied: an HTTP handler, a createCaller server-side call, and createServerSideHelpers; each needs its own context value."
sources:
  - https://github.com/trpc/trpc/blob/main/www/v11/docs/server/context.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The docs list three entry points that need a context for your router:

1. An HTTP request via an adapter, for example `createHTTPHandler({ router: appRouter, createContext })`. The adapter calls your `createContext(opts)` with request and response objects.
2. A server-side call: build a caller factory with `t.createCallerFactory(appRouter)` and then `const caller = createCaller(await createContext())`. You pass the context value directly because there is no request.
3. Server-side helpers (Next.js pages router): `createServerSideHelpers({ router: appRouter, ctx: await createContext() })` from `@trpc/react-query/server`.

The docs describe splitting the context into inner and outer parts (see the inner-and-outer-context skill): the inner context does not depend on the request, so integration tests and server-side calls, which have no request object, can use it.

`createContext()` is called once per request, so all procedures within a single batched request share the same context.

## Checked

2026-11-04: read in full against the tRPC docs repo (trpc/trpc, docs repo www/v11/docs/): server/context.md (Creating the context, Inner and outer context). Every parameter name, default, error string and code sample left in this skill appears on those pages. Removed: the invented Verify step and the inference about session-lookup cost and what callers can read.

Method: documentation only; no commands were run.
