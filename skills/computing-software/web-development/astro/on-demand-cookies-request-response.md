---
id: computing-software.web-development.astro.on-demand-cookies-request-response
name: on-demand-cookies-request-response
category: computing-software
field: web-development
product: astro
tags: [astro-cookies, astro-response, astro-request, html-streaming, headers]
level: practitioner
status: docs-checked
description: "Use cookies, Astro.response status and headers, Astro.request, and returned Response objects in on-demand pages; headers can only change at page level."
sources:
  - https://raw.githubusercontent.com/withastro/docs/main/src/content/docs/en/guides/on-demand-rendering.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
On-demand rendering uses HTML streaming: each component is sent as it renders. Features that modify Response headers work only at the page level, not in components or layouts, because headers are already sent.

Cookies:

```astro
---
export const prerender = false; // Not needed in 'server' mode

let counter = 0

if (Astro.cookies.has('counter')) {
  const cookie = Astro.cookies.get('counter')
  const value = cookie?.number()
  if (value !== undefined && !isNaN(value)) counter = value + 1
}

Astro.cookies.set('counter', String(counter))
---
<h1>Counter = {counter}</h1>
```

`Astro.response` sets status and headers:

```astro
---
if (!product) {
  Astro.response.status = 404;
  Astro.response.statusText = 'Not found';
}
Astro.response.headers.set('Cache-Control', 'public, max-age=3600');
---
```

Or return a `Response` from the page:

```astro
---
const product = await getProduct(Astro.params.id);

if (!product) {
  return new Response(null, {
    status: 404,
    statusText: 'Not found'
  });
}

if (!product.isAvailable) {
  return Astro.redirect("/products", 301);
}
---
```

`Astro.request` is a standard `Request`: `Astro.request.headers.get('cookie')`, `Astro.request.method`, url and body.

## Checked

2026-11-04. Confirmed against the Astro on-demand rendering guide: HTML streaming, page-level-only header features, Astro.cookies, Astro.response status and headers, returning a Response, Astro.redirect, Astro.request. Nothing removed.

Method: documentation only; no commands were run.
