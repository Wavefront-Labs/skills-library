---
id: computing-software.web-development.astro.static-file-endpoints
name: static-file-endpoints
category: computing-software
field: web-development
product: astro
tags: [endpoints, get-function, apiroute, static-endpoints, file-extension]
level: practitioner
status: docs-checked
description: "Create endpoints as .js or .ts files in src/pages that export GET and return a Response, with dynamic params, APIRoute typing, and file-extension caveats."
sources:
  - https://raw.githubusercontent.com/withastro/docs/main/src/content/docs/en/guides/endpoints.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Add a `.js` or `.ts` file to `src/pages/`; the extension is dropped at build, so name the file with the data extension: `src/pages/data.json.ts` builds `/data.json`. Export a `GET` function (optionally async) that receives a context object and returns a `Response`. In static builds it is called at build time.

```ts title="src/pages/builtwith.json.ts"
// Outputs: /builtwith.json
export function GET({ params, request }) {
  return new Response(
    JSON.stringify({
      name: "Astro",
      url: "https://astro.build/",
    }),
  );
}
```

Binary output needs no `encoding` property:

```ts
export async function GET({ params, request }) {
  const response = await fetch(
    "https://docs.astro.build/assets/full-logo-light.png",
  );
  return new Response(await response.arrayBuffer());
}
```

Type with `APIRoute` and `satisfies`:

```ts
import type { APIRoute } from "astro";

export const GET = (async ({ params, request }) => { /* ... */ }) satisfies APIRoute;
```

Endpoints whose URL has a file extension (e.g. `sitemap.xml.ts`) can only be accessed without a trailing slash, regardless of `build.trailingSlash`.

Dynamic routing works as for pages: bracketed filename plus `getStaticPaths()`, and `params` in the function. In static mode you can pass props; with on-demand rendering you cannot. In static mode only `request.url` is available on `request`.

## Checked

2026-11-04. Confirmed against the Astro endpoints guide: .js/.ts files in src/pages, extension removal, GET function, no encoding property, APIRoute with satisfies, trailing-slash caveat for extension URLs, getStaticPaths and props limits, request.url only in static mode. Nothing removed.

Method: documentation only; no commands were run.
