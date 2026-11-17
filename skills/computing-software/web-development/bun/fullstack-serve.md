---
id: computing-software.web-development.bun.fullstack-serve
name: fullstack-serve
category: computing-software
field: web-development
product: bun
tags: [fullstack-server, html-imports, hmr-development, production-bundle]
level: practitioner
status: docs-checked
description: "Build a full-stack Bun app: HTML imports as Bun.serve routes beside API routes, development hmr and console, and ahead-of-time production bundling."
sources:
  - https://raw.githubusercontent.com/oven-sh/bun/main/docs/bundler/fullstack.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```ts
import { serve } from "bun";
import homepage from "./index.html";
import dashboard from "./dashboard.html";

serve({
  routes: {
    "/": homepage,
    "/dashboard": dashboard,
    "/api/users/:id": async req => Response.json({ id: req.params.id }),
    "/api/items": { async GET() { return Response.json([]); }, async POST(req) { return Response.json(await req.json()); } },
  },
  development: { hmr: true, console: true },
});
```
Bun bundles the `<script>` and `<link>` tags of each imported HTML file. Unmatched requests go to the `fetch` fallback.

`development: true` adds source map headers, skips minification, re-bundles HTML on each request and enables HMR. `console: true` echoes browser logs to the terminal.

Production:

```bash
bun build --target=bun --production --outdir=dist ./src/index.ts
NODE_ENV=production bun dist/index.js
```
Or set `development: false`: Bun bundles lazily on first request, caches in memory, minifies and sends `Cache-Control` and `ETag`.

```toml
[serve.static]
plugins = ["bun-plugin-tailwind"]
env = "PUBLIC_*"
sourcemap = "linked"
```

Gotchas:
- API routes and HMR need v1.2.3+; ahead-of-time bundling needs v1.2.17+.
- Sourcemaps are off in production unless configured.
- Only literal `process.env.FOO` is inlined.
- Plugins are not yet supported by the `bun build` CLI.
- No API route auto-discovery or built-in SSR; the feature is marked work in progress.

## Checked

2026-11-04. Confirmed against the Bun docs page bundler/fullstack: HTML imports as routes bundling script and link tags, method handlers and params, development true features (SourceMap header, no minification, re-bundle per request, HMR), the development object with hmr and console, production build command and the v1.2.17 requirement, runtime bundling with development:false (lazy, cached in memory, Cache-Control and ETag, minified), serve.static plugins/env/sourcemap options, literal process.env.FOO only, sourcemaps off in production by default, plugins not yet in the bun build CLI, and the no-auto-discovery and no-SSR limitations. Nothing removed.
Method: documentation only; no commands were run.
