---
id: computing-software.web-development.astro.prefetch-links
name: prefetch-links
category: computing-software
field: web-development
product: astro
tags: [prefetch, data-astro-prefetch, prefetch-strategies, prefetchall]
level: intro
status: docs-checked
description: "Enable link prefetching with the prefetch config, pick hover/tap/viewport/load strategies per link, set defaults, or prefetch all links."
sources:
  - https://raw.githubusercontent.com/withastro/docs/main/src/content/docs/en/guides/prefetch.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Enable prefetching in config, then opt links in with `data-astro-prefetch`. Only links within your site are prefetched.

```js title="astro.config.mjs"
import { defineConfig } from 'astro/config';

export default defineConfig({
  prefetch: true
});
```

```html
<a href="/about" data-astro-prefetch>
```

Strategies:

- `hover` (default): on hover or focus
- `tap`: just before click
- `viewport`: as links enter the viewport
- `load`: all links after page load

```html
<a href="/about" data-astro-prefetch="tap">About</a>
```

Data saver mode or a slow connection falls back to `tap`; quick hovers or scrolls do not prefetch.

Change the default:

```js
export default defineConfig({
  prefetch: {
    defaultStrategy: 'viewport'
  }
});
```

Prefetch every link with `prefetchAll: true`, and opt links out with `data-astro-prefetch="false"`.

Using `<ClientRouter />` enables prefetching by default with `{ prefetchAll: true }`; override with `prefetch: false` or `prefetch: { prefetchAll: false }`.

## Checked

2026-11-04. Confirmed against the Astro prefetch guide: prefetch config, data-astro-prefetch, four strategies and hover default, data saver and slow-connection fallback to tap, defaultStrategy, prefetchAll, opt-out with false, ClientRouter default. Nothing removed.

Method: documentation only; no commands were run.
