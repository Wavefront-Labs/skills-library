---
id: computing-software.web-development.trpc.local-link-in-process
name: local-link-in-process
category: computing-software
field: web-development
product: trpc
tags: [trpc, locallink, in-process, testing, terminating-link]
level: advanced
status: docs-checked
description: "Call a router in the same process through the client API with localLink, passing router, createContext, onError and transformer instead of using HTTP."
sources:
  - https://github.com/trpc/trpc/blob/main/www/v11/docs/client/links/localLink.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`localLink` (formerly `unstable_localLink`, still working but deprecated) is a terminating link that runs procedures directly, with no HTTP.

```ts
const client = createTRPCClient<AppRouter>({
  links: [
    localLink({
      router: appRouter,
      createContext: async () => ({}),
      onError: (opts) => console.error('Error:', opts.error),
    }),
  ],
});
```

It supports queries, mutations and subscriptions, handles and transforms errors automatically (as HTTP-based links do), supports abort signals and has type-safe context creation.

Options:
- `router`: the router instance to call.
- `createContext`: async function run for each procedure call; return the context.
- `onError`: optional handler receiving the error, operation type, path, input and context.
- `transformer`: optional input/output transformers for serialization and deserialization of data.

The page recommends it where you need direct procedure calls without HTTP; for most client-side applications use `httpLink` or other HTTP-based links instead.

## Checked

2026-11-07. Read in full from a clone of github.com/trpc/trpc (main, commit fe64009), www/v11/docs/client/links/localLink.md (read in full): terminating link, deprecated `unstable_localLink` name, usage snippet, features list and the four options (router, createContext, onError, transformer).

Removed or corrected: the claims that it suits server-side rendering, tests and monorepo scripts, and that a router transformer must be repeated (not on the page); the `httpBatchLink` recommendation (page says `httpLink` or other HTTP-based links); the invented Verify step.

Method: documentation only; no commands were run.
