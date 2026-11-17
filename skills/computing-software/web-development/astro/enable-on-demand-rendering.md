---
id: computing-software.web-development.astro.enable-on-demand-rendering
name: enable-on-demand-rendering
category: computing-software
field: web-development
product: astro
tags: [ssr, adapters, prerender, output-server, astro-add]
level: practitioner
status: docs-checked
description: "Turn on server rendering in Astro: add an adapter with astro add, opt pages out of prerendering, or switch to output server and opt pages back in."
sources:
  - https://raw.githubusercontent.com/withastro/docs/main/src/content/docs/en/guides/on-demand-rendering.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
By default every page, route and endpoint is prerendered at build time. To render on demand (SSR) you need an adapter for your runtime. Official adapters exist for Node.js, Netlify, Vercel and Cloudflare. Adding one also enables features like server islands (`server:defer`).

```shell
npx astro add netlify
```

This installs the adapter and edits `astro.config.mjs`. Adapters have their own config options.

Opt a single page or endpoint out of prerendering; the rest stays static:

```astro title="src/pages/page-rendered-on-demand.astro"
---
export const prerender = false
---
```

```js title="src/pages/randomnumber.js"
export const prerender = false;

export async function GET() {
  let number = Math.random();
  return new Response(
    JSON.stringify({
      number,
      message: `Here's a random number: ${number}`,
    }),
  );
}
```

For a highly dynamic app set `output: 'server'` to server-render everything by default, then prerender individual pages:

```astro
---
export const prerender = true
---
```

Start with the default `'static'` mode until most or all pages need a server. `'server'` adds no functionality; it only switches the default rendering behavior.

## Checked

2026-11-04. Confirmed against the Astro on-demand rendering guide: prerendered by default, adapters and the official adapter list, astro add netlify, prerender false and true exports, output server mode and the static-first tip. Nothing removed.

Method: documentation only; no commands were run.
