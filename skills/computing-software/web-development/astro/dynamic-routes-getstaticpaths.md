---
id: computing-software.web-development.astro.dynamic-routes-getstaticpaths
name: dynamic-routes-getstaticpaths
category: computing-software
field: web-development
product: astro
tags: [dynamic-routes, getstaticpaths, astro-params, decodeuri]
level: practitioner
status: docs-checked
description: "Generate pages from a bracketed filename in static mode: export getStaticPaths returning params, read Astro.params, use several params, and decode them."
sources:
  - https://raw.githubusercontent.com/withastro/docs/main/src/content/docs/en/guides/routing.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A file like `src/pages/authors/[author].astro` makes `author` a parameter. In static output, every route must be known at build time, so export `getStaticPaths()` returning objects with a `params` property whose keys match the filename.

```astro title="src/pages/dogs/[dog].astro"
---
export function getStaticPaths() {
  return [
    { params: { dog: "clifford" }},
    { params: { dog: "rover" }},
    { params: { dog: "spot" }},
  ];
}

const { dog } = Astro.params;
---
<div>Good dog, {dog}!</div>
```

This generates `/dogs/clifford`, `/dogs/rover` and `/dogs/spot`.

Multiple parameters must all be included in each `params`:

```astro title="src/pages/[lang]-[version]/info.astro"
---
export function getStaticPaths() {
  return [
    { params: { lang: "en", version: "v1" }},
    { params: { lang: "fr", version: "v2" }},
  ];
}

const { lang, version } = Astro.params;
---
```

That yields `/en-v1/info` and `/fr-v2/info`. With `src/pages/[lang]/[version]/info.astro` it yields `/en/v1/info` and `/fr/v2/info`.

`params` from `getStaticPaths()` are not decoded; use `decodeURI()`:

```astro title="src/pages/[slug].astro"
export function getStaticPaths() {
  return [
    { params: { slug: decodeURI("%5Bpage%5D") }}, // decodes to "[page]"
  ]
}
```

## Checked

2026-11-04. Confirmed against the Astro routing guide: getStaticPaths params, multiple params, and decodeURI for undecoded params. Nothing removed.

Method: documentation only; no commands were run.
