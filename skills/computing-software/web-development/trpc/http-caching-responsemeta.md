---
id: computing-software.web-development.trpc.http-caching-responsemeta
name: http-caching-responsemeta
category: computing-software
field: web-development
product: trpc
tags: [trpc, caching, responsemeta, cache-control, cdn]
level: advanced
status: docs-checked
description: "Cache public query responses with the adapter responseMeta callback, only when every call in a batch is a public ok query."
sources:
  - https://github.com/trpc/trpc/blob/main/www/v11/docs/server/caching.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
All tRPC queries are normal HTTP GET requests, so standard cache headers work with any host that honours them (Vercel, Cloudflare, CloudFront). Be careful with personal data. Batching is on by default, so set cache headers in `responseMeta` and make sure no concurrent call in the batch carries personal data, or omit cache headers when there is an auth header or cookie.

```ts
createHTTPServer({
  router: appRouter,
  createContext,
  responseMeta(opts) {
    const { info, errors, type, eagerGeneration } = opts;
    const allPublic = info?.calls.every((call) => call.path.startsWith('public.'));
    const allOk = !eagerGeneration && errors.length === 0;
    const isQuery = type === 'query';
    if (allPublic && allOk && isQuery) {
      return {
        headers: new Headers([
          ['cache-control', 's-maxage=1, stale-while-revalidate=86400'],
        ]),
      };
    }
    return {};
  },
});
```

`responseMeta` runs once per HTTP response, so it decides the headers for every procedure in the batch. It also receives `ctx`, e.g. to skip caching for signed-in users. For streamed responses (`httpBatchStreamLink`) headers go out before any procedure finishes, so it runs with `eagerGeneration: true` and an empty `errors` array.

Convention used above: put all cacheable procedures under a `public` router so the path prefix identifies them.

## Checked

2026-11-04: read in full against the tRPC docs repo (trpc/trpc, docs repo www/v11/docs/): server/caching.md. Every parameter name, default, error string and code sample left in this skill appears on those pages. Removed: the invented Verify step.

Method: documentation only; no commands were run.
