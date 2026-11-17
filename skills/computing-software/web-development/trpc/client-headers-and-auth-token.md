---
id: computing-software.web-development.trpc.client-headers-and-auth-token
name: client-headers-and-auth-token
category: computing-software
field: web-development
product: trpc
tags: [trpc, headers, authorization, client, httplink]
level: intro
status: docs-checked
description: "Send auth headers from the tRPC client using a headers object or per-request function on any HTTP link, and update the token after login."
sources:
  - https://github.com/trpc/trpc/blob/main/www/v11/docs/client/headers.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The `headers` option works on `httpBatchLink`, `httpBatchStreamLink`, `httpLink` and `httpSubscriptionLink`. It can be an object or a function; a function runs for every HTTP request, so it always sees the latest value.

```ts
let token: string;
export function setToken(newToken: string) { token = newToken; }

export const trpc = createTRPCClient<AppRouter>({
  links: [
    httpBatchLink({
      url: 'http://localhost:3000',
      headers() { return { Authorization: token }; },
    }),
  ],
});
```

Login flow: call the login mutation, then `setToken(result.accessToken)`. Where the token lives is up to you: a module variable, cookies or local storage read inside the function.

For batch links the callback receives `{ opList }` (all operations in the batch), while `httpLink` receives `{ op }`. The callback may be async.

Because a batch is one request, headers apply to the whole batch. For subscriptions over SSE, headers need an EventSource ponyfill and `eventSourceOptions` instead (see `computing-software.web-development.trpc.http-subscription-link-setup-and-auth`).

## Checked

2026-11-04: read in full against the tRPC docs repo (trpc/trpc, docs repo www/v11/docs/): client/headers.md, client/links.md (Common mistakes), client/links/httpSubscriptionLink.md. Every parameter name, default, error string and code sample left in this skill appears on those pages. Removed: the invented Verify step.

Method: documentation only; no commands were run.
