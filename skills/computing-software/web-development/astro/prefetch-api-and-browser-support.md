---
id: computing-software.web-development.astro.prefetch-api-and-browser-support
name: prefetch-api-and-browser-support
category: computing-software
field: web-development
product: astro
tags: [prefetch-api, astro-prefetch, eagerness, cache-headers, safari]
level: advanced
status: docs-checked
description: "Call prefetch() from astro:prefetch for non-link navigation, tune eagerness, and set cache headers so Firefox and Safari prefetch correctly."
sources:
  - https://raw.githubusercontent.com/withastro/docs/main/src/content/docs/en/guides/prefetch.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Prefetch programmatically with `prefetch()` from `astro:prefetch`, only in client-side scripts since it uses browser APIs:

```astro
<button id="btn">Click me</button>

<script>
  import { prefetch } from 'astro:prefetch';

  const btn = document.getElementById('btn');
  btn?.addEventListener('click', () => {
    prefetch('/about');
  });
</script>
```

It has the same data saver and slow-connection detection; override with:

```js
prefetch('/about', { ignoreSlowConnection: true });
```

With the experimental `clientPrerender` flag, `eagerness` (`'immediate'` default, `'eager'`, `'moderate'`, `'conservative'`) follows the Speculation Rules API:

```js
prefetch('/data-heavy-dashboard', { eagerness: 'conservative' });
prefetch('/terms-of-service', { eagerness: 'moderate' });
```

Browser support: prefetching uses `<link rel="prefetch">` when supported, else `fetch()`.

- Chrome: works as intended.
- Firefox: without an explicit cache header (`Cache-Control` or `Expires`) it errors with `NS_BINDING_ABORTED`; a proper `ETag` is still re-used on navigation.
- Safari: falls back to `fetch()`, which requires cache headers (`Cache-Control`, `Expires`, `ETag`). `ETag` does not work in private windows.

Prerendered pages usually get `ETag` from the host. For server-rendered pages, set cache headers yourself.

Migrating from `@astrojs/prefetch`: remove the integration, set `prefetch: true`, and replace `selector` with `data-astro-prefetch="viewport"` on links, and `intentSelector` with `data-astro-prefetch`. `throttles` is no longer needed.

## Checked

2026-11-04. Confirmed against the Astro prefetch guide: prefetch() from astro:prefetch, ignoreSlowConnection, eagerness values and clientPrerender requirement, link rel=prefetch with fetch fallback, Chrome, Firefox and Safari notes, cache header advice, migration from @astrojs/prefetch. Nothing removed.

Method: documentation only; no commands were run.
