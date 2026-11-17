---
id: computing-software.web-development.trpc.logger-link
name: logger-link
category: computing-software
field: web-development
product: trpc
tags: [trpc, loggerlink, logging, debugging, client]
level: intro
status: docs-checked
description: "Add loggerLink before the terminating link to log queries, mutations and subscriptions, enabled in development and for errors in production."
sources:
  - https://github.com/trpc/trpc/blob/main/www/v11/docs/client/links/loggerLink.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`loggerLink` prints a prettified log of each operation, request and response, to the console by default. In the page example it is listed before the terminating link (`httpBatchLink`).

```ts
createTRPCClient<AppRouter>({
  links: [
    loggerLink({
      enabled: (opts) =>
        (process.env.NODE_ENV === 'development' && typeof window !== 'undefined') ||
        (opts.direction === 'down' && opts.result instanceof Error),
    }),
    httpBatchLink({ url: 'http://localhost:3000' }),
  ],
});
```

The page's `enabled` example logs when `NODE_ENV` is `development` in a browser, or when the direction is `down` and the result is an `Error`.

Options:
- `logger`: custom log function.
- `enabled`: predicate, true by default.
- `console`: console-like object used by the default logger.
- `colorMode`: `'ansi' | 'css' | 'none'`; default is `ansi` when no `window` and `css` otherwise.
- `withContext`: include the operation context; defaults to false unless `colorMode` is `css`.

## Checked

2026-11-07. Read in full from a clone of github.com/trpc/trpc (main, commit fe64009), www/v11/docs/client/links/loggerLink.md (read in full): usage snippet, the `LoggerLinkOptions` type with its comments (enabled true by default, console used by the built-in defaultLogger, colorMode default, withContext default).

Removed or corrected: the claim that `logger` replaces `defaultLogger` (page does not say so), the advice to use colorMode none in CI, and the invented Verify step; reworded the placement and `enabled` sentences to match the page example.

Method: documentation only; no commands were run.
