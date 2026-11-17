---
id: computing-software.web-development.astro.static-routes-and-navigation
name: static-routes-and-navigation
category: computing-software
field: web-development
product: astro
tags: [routing, static-routes, anchor-links, build-format]
level: intro
status: docs-checked
description: "Map files in src/pages to URLs and navigate with plain anchor elements; Astro has no Link component."
sources:
  - https://raw.githubusercontent.com/withastro/docs/main/src/content/docs/en/guides/routing.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Astro uses file-based routing from `src/pages/`. Navigate with standard `<a>` elements; there is no framework-specific `<Link>` component.

```astro title="src/pages/index.astro"
<p>Read more <a href="/about/">about</a> Astro!</p>

<!-- With `base: "/docs"` configured -->
<p>Learn more in our <a href="/docs/reference/">reference</a> section!</p> 
```

`.astro`, `.md` and `.mdx` files automatically become pages; the route matches the path and filename:

```diff
src/pages/index.astro        -> mysite.com/
src/pages/about.astro        -> mysite.com/about
src/pages/about/index.astro  -> mysite.com/about
src/pages/about/me.astro     -> mysite.com/about/me
src/pages/posts/1.md         -> mysite.com/posts/1
```

There is no separate routing config. In static builds, customize the output file format with the `build.format` option.

Exclude a page or directory from routing by prefixing its name with `_`; such files are not recognized by the router or placed in `dist/`. This lets you colocate tests, utilities and components next to pages:

```
src/pages/
  _hidden-directory/
  _hidden-page.astro
  index.astro
  projects/
    _SomeComponent.astro
    project1.md
```

## Checked

2026-11-04. Confirmed against the Astro routing guide: anchor-element navigation, file-to-URL mapping, build.format, and underscore-prefix exclusion. Nothing removed.

Method: documentation only; no commands were run.
