---
id: computing-software.web-development.astro.on-demand-dynamic-routes
name: on-demand-dynamic-routes
category: computing-software
field: web-development
product: astro
tags: [ssr-routes, prerender-false, on-demand-routes, slug-lookup]
level: practitioner
status: docs-checked
description: "Define dynamic routes for on-demand rendering: no getStaticPaths, no props, one rest parameter at most, and look up the slug yourself."
sources:
  - https://raw.githubusercontent.com/withastro/docs/main/src/content/docs/en/guides/routing.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
With on-demand rendering (adapter), define dynamic routes with the same `[param]` or `[...path]` filenames, but the page is served to any matching route. Do not use `getStaticPaths` there.

Only one spread rest parameter is allowed per filename: `src/pages/[locale]/[...slug].astro` or `src/pages/[...locale]/[slug].astro` work, `src/pages/[...locale]/[...slug].astro` does not.

```astro title="src/pages/resources/[resource]/[id].astro"
---
export const prerender = false; // Not needed in 'server' mode
const { resource, id } = Astro.params;
---
<h1>{resource}: {id}</h1>
```

This serves `resources/users/1`, `resources/colors/blue`, etc.

Without `getStaticPaths()` there are no props, so look up the `slug` param yourself. At the root the `slug` param is `undefined`; redirect to 404 when nothing matches:

```astro title="src/pages/[...slug].astro"
---
const pages = [
	{ slug: undefined, title: 'Astro Store', text: 'Welcome to the Astro store!' },
	{ slug: 'products', title: 'Astro products', text: 'We have lots of products for you' },
];

const { slug } = Astro.params;
const page = pages.find((page) => page.slug === slug);
if (!page) return Astro.redirect("/404");
const { title, text } = page;
---
```

## Checked

2026-11-04. Confirmed against the Astro routing guide: no getStaticPaths in on-demand routes, one rest parameter only, prerender = false, slug lookup and the 404 redirect. Replaced a duplicate tag.

Method: documentation only; no commands were run.
