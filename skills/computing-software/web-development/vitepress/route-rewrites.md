---
id: computing-software.web-development.vitepress.route-rewrites
name: route-rewrites
category: computing-software
field: web-development
product: vitepress
tags: [vitepress, rewrites, route-rewrites, path-to-regexp, monorepo-docs, source-to-url-mapping]
level: advanced
status: docs-checked
description: "Map source Markdown paths to different output URLs with rewrites, including parameterised patterns and function form."
sources:
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/guide/routing.md
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/reference/site-config.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`rewrites` customizes the mapping between source file paths and generated pages. A common case is a monorepo that keeps docs beside package sources:

```
packages/pkg-a/src/index.md  ->  /pkg-a/index.html
packages/pkg-a/src/foo.md    ->  /pkg-a/foo.html
packages/pkg-b/src/bar.md    ->  /pkg-b/bar.html
```

**Static map**

```ts
export default {
  rewrites: {
    'packages/pkg-a/src/index.md': 'pkg-a/index.md',
    'packages/pkg-a/src/foo.md': 'pkg-a/foo.md'
  }
}
```

**Parameterised.** Keys and values are compiled with `path-to-regexp`, so one rule covers all packages:

```ts
rewrites: { 'packages/:pkg/src/:slug*': ':pkg/:slug*' }
```

**Function form** receives the original path and returns the new one:

```ts
rewrites(id) {
  return id.replace(/^packages\/([^/]+)\/src\//, '$1/')
}
```

**Gotcha.** With rewrites enabled, relative links in Markdown must be based on the *rewritten* paths. To link from `packages/pkg-a/src/pkg-a-code.md` to `packages/pkg-b/src/pkg-b-code.md` write `[Link to PKG B](../pkg-b/pkg-b-code)`.

The rewrite paths are compiled with `path-to-regexp`, so consult its documentation (version 6.x parameters section) for more advanced syntax.

Verify: the dev server serves the page at the rewritten URL.

## Checked

2026-11-08. Read the VitePress docs source pages routing (Route Rewrites) and site-config (rewrites). Confirmed the monorepo mapping, static map, :pkg and :slug* parameterised form, function form, path-to-regexp compilation with its 6.x link, and the rewritten-path relative link rule. Removed a sentence about what keys are relative to, which the pages do not state.

Method: docs-only read of cited pages, 2026-11-08
