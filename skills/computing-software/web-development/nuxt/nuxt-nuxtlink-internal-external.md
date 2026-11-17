---
id: computing-software.web-development.nuxt.nuxt-nuxtlink-internal-external
name: nuxt-nuxtlink-internal-external
category: computing-software
field: web-development
product: nuxt
tags: [nuxt, nuxt-link, navigation, external-links, rel]
level: practitioner
status: docs-checked
description: "Use NuxtLink for internal routes, named routes with params, external URLs, static file links with external, and rel defaults."
sources:
  - https://github.com/nuxt/nuxt/blob/main/docs/4.api/1.components/4.nuxt-link.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`<NuxtLink>` is a drop-in replacement for both Vue Router's `<RouterLink>` and HTML's `<a>` tag. It determines whether a link is internal or external and renders it accordingly, with optimizations such as prefetching and default attributes.

Internal: `<NuxtLink to="/about">` renders `<a href="/about">` with Vue Router navigation and smart prefetching. Named routes with params: `<NuxtLink :to="{ name: 'posts-id', params: { id: 123 } }">` renders `/posts/123` for `~/pages/posts/[id].vue`. The Pages panel in Nuxt DevTools shows route names and the params they take. When you pass an object into `to`, query parameters are handled as in Vue Router: keys and values are automatically encoded, so you do not call `encodeURI` or `encodeURIComponent` yourself.

Static files and cross-app links: by default `<NuxtLink>` uses client-side navigation for relative routes, which can give unexpected 404 errors for files in the `/public` directory or another application on the same domain. Add the `external` prop so the link is rendered as a standard `<a>` tag, bypassing Vue Router:

```vue
<NuxtLink to="/example-report.pdf" external>Download Report</NuxtLink>
<NuxtLink to="/another-app" external>Go to Another App</NuxtLink>
```

External sites (`<NuxtLink to="https://nuxtjs.org">`) render with `rel="noopener noreferrer"`. That `rel` is applied by default to links with a `target` attribute or to absolute links (starting with `http://`, `https://` or `//`): `noopener` solves a security bug in older browsers and `noreferrer` improves privacy by not sending the `Referer` header. The docs say these defaults have no negative impact on SEO. Override with the `rel` prop, or use `noRel` (`no-rel`) to prevent the default `rel` on absolute links; `noRel` and `rel` cannot be used together and `rel` is then ignored.

## Checked

2026-11-04. Confirmed against the Nuxt NuxtLink API page: drop-in description, internal and named-route examples, DevTools tip, query encoding tip, external prop for static and cross-app links, rel defaults and rationale, rel and noRel props with their conflict note. Removed the Verify step.

Method: documentation only; no commands were run.
