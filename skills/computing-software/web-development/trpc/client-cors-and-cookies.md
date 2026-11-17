---
id: computing-software.web-development.trpc.client-cors-and-cookies
name: client-cors-and-cookies
category: computing-software
field: web-development
product: trpc
tags: [trpc, cors, cookies, credentials, fetch]
level: practitioner
status: docs-checked
description: "Send cookies to a cross-origin tRPC API by passing credentials include through the link fetch option and enabling CORS on the server adapter."
sources:
  - https://github.com/trpc/trpc/blob/main/www/v11/docs/client/cors.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
When the API lives on a different origin and needs cookies, two things are required.

1. Client: pass `credentials: 'include'` through the link's `fetch` option.

```ts
httpBatchLink({
  url: 'YOUR_SERVER_URL',
  fetch(url, options) {
    return fetch(url, { ...options, credentials: 'include' });
  },
})
```

2. Server: enable CORS, either in the tRPC adapter or in the HTTP server in front of your API. The method differs per adapter and hosting, and each adapter's docs cover it where it applies.

For SSE subscriptions, cookies are sent when client and server share a domain; across domains use `withCredentials: true` in `eventSourceOptions` instead of the fetch override.

`httpBatchStreamLink` can use `streamHeader: 'accept'`: the standard `Accept` header is CORS-safelisted, which can avoid a CORS preflight for cross-origin streaming queries.

## Checked

2026-11-04: read in full against the tRPC docs repo (trpc/trpc, docs repo www/v11/docs/): client/cors.md, client/links/httpSubscriptionLink.md (Cross-domain), client/links/httpBatchStreamLink.md (streamHeader). Every parameter name, default, error string and code sample left in this skill appears on those pages. Removed: the invented Verify step, the wildcard-origin / Access-Control-Allow-Credentials sentence and the claim that custom headers trigger preflight (neither is on the pages).

Method: documentation only; no commands were run.
