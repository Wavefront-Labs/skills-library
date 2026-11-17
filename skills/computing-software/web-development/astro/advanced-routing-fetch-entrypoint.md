---
id: computing-software.web-development.astro.advanced-routing-fetch-entrypoint
name: advanced-routing-fetch-entrypoint
category: computing-software
field: web-development
product: astro
tags: [advanced-routing, fetch-entrypoint, fetchstate, fetchfile]
level: sme
status: docs-checked
description: "Replace Astro's built-in request pipeline with src/fetch.ts: wrap astro(), compose handlers from astro/fetch, rename or disable the entrypoint, and the pathname caution."
sources:
  - https://raw.githubusercontent.com/withastro/docs/main/src/content/docs/en/guides/routing.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The default pipeline order is: trailing-slash normalization, redirects, sessions, actions, user middleware, page rendering, i18n, caching. To replace it, create `src/fetch.ts` default-exporting an object with `fetch(request)` returning a `Response` (`.ts`, `.js`, `.mjs`, `.mts` supported).

Wrap the full pipeline with `astro()`:

```ts title="src/fetch.ts"
import { FetchState, astro } from 'astro/fetch';

export default {
  async fetch(request: Request): Promise<Response> {
    const state = new FetchState(request);

    // Custom pre-processing, runs before any Astro handler
    console.log(`${request.method} ${new URL(request.url).pathname}`);

    const response = await astro(state);

    // Custom post-processing, runs after Astro renders
    response.headers.set('X-Powered-By', 'Astro');
    return response;
  },
};
```

Or compose handlers (`actions`, `middleware`, `pages`, `i18n`) in your own order:

```ts
const actionResponse = await actions(state);
if (actionResponse) return actionResponse;

const response = await middleware(state, (s) => pages(s));
return i18n(state, response);
```

Caution: the request pathname is not guaranteed to equal the route Astro matches, so `url.pathname.startsWith('/dashboard')` can be bypassed. Do not authorize by matching pathname strings; use a router that owns route matching, such as Hono via `astro/hono`.

Change the filename with `fetchFile: 'handler'` in the config, or set `fetchFile: null` to disable the entrypoint.

## Checked

2026-11-04. Confirmed against the Astro routing guide: default pipeline order, src/fetch.ts, astro() wrapper, handler composition, the pathname caution, and fetchFile. Nothing removed.

Method: documentation only; no commands were run.
