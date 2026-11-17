---
id: computing-software.web-development.trpc.data-transformer-superjson
name: data-transformer-superjson
category: computing-software
field: web-development
product: trpc
tags: [trpc, transformer, superjson, date, serialization]
level: practitioner
status: docs-checked
description: "Preserve Date, Map and Set over the wire by setting superjson as the transformer on initTRPC and on every terminating client link."
sources:
  - https://github.com/trpc/trpc/blob/main/www/v11/docs/server/data-transformers.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Without a transformer tRPC serializes with `JSON.stringify`: a `Date` arrives as a string and `Map`/`Set` become `{}`. A transformer such as superjson preserves them.

1. Install `superjson`.
2. Server: `initTRPC.create({ transformer: superjson })`.
3. Client: put `transformer: superjson` on every terminating link, not on `createTRPCClient()`.

```ts
export const client = createTRPCClient<AppRouter>({
  links: [httpLink({ url: 'http://localhost:3000', transformer: superjson })],
});
```

TypeScript guides you: once the server has a transformer, links lacking it fail to compile. Every terminating link needs it, including both branches of a `splitLink` (for example `httpSubscriptionLink` and `httpBatchLink`). With `wsLink`, the option goes on `wsLink()`, not on `createWSClient()`.

After this, a `Date` returned by a procedure is a real `Date` on the client (`event.at.getFullYear()` type-checks and works).

Remember that transformers apply to tRPC requests and responses only. If you dehydrate a TanStack Query cache on the server and hydrate on the client yourself, set `serializeData` and `deserializeData` too (see the Query Client factory in the TanStack React Query server components docs).

## Checked

2026-11-04: read in full against the tRPC docs repo (trpc/trpc, docs repo www/v11/docs/): server/data-transformers.md (superjson, Common mistakes). Every parameter name, default, error string and code sample left in this skill appears on those pages. Removed: the invented Verify step and a cross-reference to other skills in place of the page's own pointer.

Method: documentation only; no commands were run.
