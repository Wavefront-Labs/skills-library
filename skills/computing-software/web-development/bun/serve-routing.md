---
id: computing-software.web-development.bun.serve-routing
name: serve-routing
category: computing-software
field: web-development
product: bun
tags: [serve-routes, route-params, static-responses, directory-routes]
level: practitioner
status: docs-checked
description: "Define Bun.serve routes: params, wildcards, per-method handlers, static Response routes, directory and file routes, precedence order and path-safety gotchas."
sources:
  - https://raw.githubusercontent.com/oven-sh/bun/main/docs/runtime/http/routing.mdx
  - https://raw.githubusercontent.com/oven-sh/bun/main/docs/runtime/http/server.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```ts
Bun.serve({
  routes: {
    "/health": new Response("OK"),                 // static, cached for server lifetime
    "/orgs/:orgId/repos/:repoId": req => Response.json(req.params),
    "/api/posts": { GET: () => new Response("list"), POST: async req => Response.json(await req.json()) },
    "/static/*": { dir: "./public" },              // path must end in /*
    "/favicon.ico": Bun.file("./favicon.ico"),     // lazily loaded; new Response(Bun.file(p)) reads per request, 404 if missing
    "/api/*": Response.json({ message: "Not found" }, { status: 404 }),
  },
  fetch() { return new Response("Unmatched", { status: 404 }); },
});
```

`routes` needs Bun v1.2.3+; the `fetch` handler catches unmatched requests.

Precedence: exact, then parameter, then wildcard (`/api/*`), then global (`/*`). Percent-encoded parameter values are decoded automatically.

Gotchas:
- Static `Response` routes do not reflect changes until `server.reload(options)`.
- Routing is case-sensitive but macOS and Windows filesystems are not: keep access-controlled files outside `dir`.
- Non-canonical paths (`..`, empty segments, `%2F`) return 404. `dir` routes add `Content-Type`, weak `ETag`, 304 and range support; a directory without a trailing slash gets 301.
- `await file.bytes()` as a static route buffers at startup and errors if missing.

## Checked

2026-11-04. Confirmed against the Bun docs pages runtime/http/routing and runtime/http/server: route params and req.params, per-method handlers, static Response routes cached until server.reload, directory routes needing a trailing /* with non-canonical path 404s, weak ETag, 304, range support and the 301 for directories, case-sensitivity warning, precedence order, percent-decoding, routes needing Bun 1.2.3+, and buffered versus per-request file responses. The bare Bun.file route comment was corrected: the server page says it is loaded lazily; per-request reads and 404 are documented for new Response(Bun.file(path)).
Method: documentation only; no commands were run.
