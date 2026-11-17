---
id: computing-software.web-development.astro.rest-parameters-and-props
name: rest-parameters-and-props
category: computing-software
field: web-development
product: astro
tags: [rest-parameters, getstaticpaths-props, catch-all-routes, slug]
level: practitioner
status: docs-checked
description: "Match paths of any depth with [...path] rest parameters, allow the root with undefined, and pass per-page data through getStaticPaths props."
sources:
  - https://raw.githubusercontent.com/withastro/docs/main/src/content/docs/en/guides/routing.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A rest parameter (`[...path]`) in the filename matches paths of any depth:

```astro title="src/pages/sequences/[...path].astro"
---
export function getStaticPaths() {
  return [
    { params: { path: "one/two/three" }},
    { params: { path: "four" }},
    { params: { path: undefined }}
  ]
}

const { path } = Astro.params;
---
```

This generates `/sequences/one/two/three`, `/sequences/four` and `/sequences`. Setting the rest parameter to `undefined` matches the top-level page.

Rest parameters combine with named ones, e.g. `/[org]/[repo]/tree/[branch]/[...file]`; a request for `/withastro/astro/tree/main/docs/public/favicon.svg` splits to `{ org: "withastro", repo: "astro", branch: "main", file: "docs/public/favicon.svg" }`.

Return `props` next to `params` to pass data to each page:

```astro title="src/pages/[...slug].astro"
---
export function getStaticPaths() {
  const pages = [
    { slug: undefined, title: "Astro Store", text: "Welcome to the Astro store!" },
    { slug: "products", title: "Astro products", text: "We have lots of products for you" },
  ];
  
  return pages.map(({ slug, title, text }) => {
    return {
      params: { slug },
      props: { title, text },
    };
  });
}

const { title, text } = Astro.props;
---
```

## Checked

2026-11-04. Confirmed against the Astro routing guide: rest parameter examples, undefined for the root, the org/repo split, and props from getStaticPaths. Nothing removed.

Method: documentation only; no commands were run.
