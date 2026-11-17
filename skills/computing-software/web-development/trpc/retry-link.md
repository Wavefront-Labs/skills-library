---
id: computing-software.web-development.trpc.retry-link
name: retry-link
category: computing-software
field: web-development
product: trpc
tags: [trpc, retrylink, retry, errors, client]
level: practitioner
status: docs-checked
description: "Retry failed tRPC operations with retryLink using a retry predicate on error, op and attempts plus retryDelayMs backoff, and how tracked ids are resumed."
sources:
  - https://github.com/trpc/trpc/blob/main/www/v11/docs/client/links/retryLink.md
  - https://github.com/trpc/trpc/blob/main/www/v11/docs/client/links/httpSubscriptionLink.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`retryLink` retries failed operations based on your rules. If you use `@trpc/react-query`, you generally do not need it, because `useQuery()` and `useMutation()` already retry through TanStack Query.

```ts
retryLink({
  retry(opts) {
    if (opts.error.data && opts.error.data.code !== 'INTERNAL_SERVER_ERROR') {
      return false; // do not retry non-500s
    }
    if (opts.op.type !== 'query') return false; // only queries
    return opts.attempts <= 3;
  },
  retryDelayMs: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000),
})
```

It can be placed before or after other links; the page example puts it before the terminating `httpBatchLink`. `retry` is required and receives `{ op, error, attempts }`, where `attempts` includes the first call and `error` is a `TRPCClientError`. The example retries when no valid tRPC error could be obtained (an error without `data`). `retryDelayMs(attempt)` defaults to 0 ms; the example uses an exponential backoff capped at 30 seconds.

The page example retries only queries, and only up to 3 times (`attempts <= 3`).

For subscriptions that use `tracked()`, the link automatically includes the last known event ID when retrying, so a reconnect can resume without missing events (the retryLink page gives SSE with `httpSubscriptionLink` and `401 Unauthorized` as an example). The `httpSubscriptionLink` page shows `retryLink` placed before `httpSubscriptionLink` and retrying on `UNAUTHORIZED` or `FORBIDDEN` to renew authentication, and cautions that restarting the connection recreates the `EventSource` from scratch, so previously tracked events are lost.

## Checked

2026-11-07. Read in full from a clone of github.com/trpc/trpc (main, commit fe64009), www/v11/docs/client/links/retryLink.md (read in full): the tip about @trpc/react-query, usage snippet, bullet list, options types (retry required, retryDelayMs default 0, attempts includes the first call) and "Handling tracked() events"; www/v11/docs/client/links/httpSubscriptionLink.md (read in full): the "Updating configuration on an active connection" section.

Removed or corrected: the "network failure" gloss, the advice to add a backoff, the idempotent/mutation side-effect warning (not on the page), and the invented Verify step; the placement sentence now matches the page ("before or after other links"). Added the contradiction caveat from the httpSubscriptionLink page about lost tracked events, and that page as a source.

Method: documentation only; no commands were run.
