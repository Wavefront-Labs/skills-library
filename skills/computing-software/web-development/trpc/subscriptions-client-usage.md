---
id: computing-software.web-development.trpc.subscriptions-client-usage
name: subscriptions-client-usage
category: computing-software
field: web-development
product: trpc
tags: [trpc, subscription, subscribe, splitlink, httpsubscriptionlink]
level: practitioner
status: docs-checked
description: "Route subscriptions to httpSubscriptionLink or wsLink with splitLink and call .subscribe() with onData and onError, then unsubscribe."
sources:
  - https://github.com/trpc/trpc/blob/main/www/v11/docs/server/subscriptions.md
  - https://github.com/trpc/trpc/blob/main/www/v11/docs/server/authorization.md
  - https://github.com/trpc/trpc/blob/main/www/v11/docs/client/links/httpSubscriptionLink.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
On the client, send subscriptions to `httpSubscriptionLink` (SSE) or `wsLink`, and everything else to a normal link, using a `splitLink` that checks `op.type`.

```ts
const client = createTRPCClient<AppRouter>({
  links: [
    splitLink({
      condition: (op) => op.type === 'subscription',
      true: httpSubscriptionLink({ url: 'http://localhost:3000' }),
      false: httpBatchLink({ url: 'http://localhost:3000' }),
    }),
  ],
});

const subscription = client.onPostAdd.subscribe(
  { lastEventId: null },
  {
    onData(event) {
      console.log(event.id, event.data.title); // tracked events arrive as { id, data }
    },
    onError(err) {
      console.error(err);
    },
  },
);

// stop listening
subscription.unsubscribe();
```

Tracked events arrive in `onData` as `{ id, data }`. Without callbacks, `.subscribe()` returns an async iterator you can consume with `for await`; it has no `unsubscribe()`, and leaving the loop or aborting the `signal` you passed unsubscribes.

For React the docs point to `subscriptionOptions` with TanStack React Query or the classic `useSubscription()` hook (see the React skills).

Authentication for SSE: the browser `EventSource` cannot send custom headers, so use cookies or an EventSource ponyfill, and avoid tokens in `connectionParams`, which are sent as part of the URL.

## Checked

2026-11-07. Read in full from a clone of github.com/trpc/trpc (main, commit fe64009), www/v11/docs/server/subscriptions.md (read in full): "Subscribing from the client" with both snippets; www/v11/docs/server/authorization.md and www/v11/docs/client/links/httpSubscriptionLink.md (both read in full) for the EventSource header limit, cookies, ponyfill and connectionParams-in-URL statements.

Removed or corrected: the claims that untracked events arrive as the plain yielded value and that every splitLink link needs the transformer (not on the page), and the invented Verify step about a server `finally`.

Method: documentation only; no commands were run.
