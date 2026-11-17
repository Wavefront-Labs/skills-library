---
id: computing-software.web-development.trpc.fetch-adapter-edge-runtimes
name: fetch-adapter-edge-runtimes
category: computing-software
field: web-development
product: trpc
tags: [trpc, fetch-adapter, fetchrequesthandler, cloudflare-workers, edge]
level: practitioner
status: docs-checked
description: "Serve tRPC from any WinterCG runtime with fetchRequestHandler: Cloudflare Workers, Deno, Vercel Edge, Astro, Remix, SolidStart; endpoint must match the route."
sources:
  - https://github.com/trpc/trpc/blob/main/www/v11/docs/server/adapters/fetch.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The Fetch adapter converts a router into a handler from `Request` to `Response`, so it runs on any runtime implementing the WinterCG Minimum Common Web Platform API (needs `Request`, `Response`, `fetch`, `Headers`, `URL`): Cloudflare Workers, Deno Deploy, Vercel Edge Runtime, and frameworks such as Astro (SSR), Remix and SolidStart.

```ts
export default {
  async fetch(request: Request): Promise<Response> {
    return fetchRequestHandler({
      endpoint: '/trpc',
      req: request,
      router: appRouter,
      createContext,
    });
  },
};
```

Context uses `FetchCreateContextFnOptions` with `req` and `resHeaders`; headers set on `resHeaders` (like `Set-Cookie`) are added to the response. Runtime recipes from the docs:

- Astro: export `ALL: APIRoute` in `src/pages/trpc/[trpc].ts` calling the handler with `opts.request`.
- Remix: `loader` and `action` in `app/routes/trpc.$trpc.ts` both call the handler with `args.request`.
- SolidStart: export `handler as GET, handler as POST` in `src/routes/api/trpc/[trpc].ts` with `endpoint: '/api/trpc'`.
- Deno: import from `npm:@trpc/server`; Deno Deploy uses `Deno.serve(handler)`.
- Vercel Edge Runtime: `addEventListener('fetch', e => e.respondWith(...))`, run with `edge-runtime --listen server.ts`.

Common mistake: tRPC strips `endpoint` from the start of the URL path to find the procedure, so a handler serving `/api/trpc/*` needs `endpoint: '/api/trpc'`; a wrong value makes every call return 404 NOT_FOUND.

## Checked

2026-11-04: read in full against the tRPC docs repo (trpc/trpc, docs repo www/v11/docs/): server/adapters/fetch.md (runtime list, Common setup, Astro, Deno Deploy, Remix, SolidStart, Vercel Edge Runtime, Common mistakes). Every parameter name, default, error string and code sample left in this skill appears on those pages. Removed: the invented Verify step.

Method: documentation only; no commands were run.
