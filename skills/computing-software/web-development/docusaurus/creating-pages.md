---
id: computing-software.web-development.docusaurus.creating-pages
name: creating-pages
category: computing-software
field: web-development
product: docusaurus
tags: [src-pages, react-page, markdown-page, layout-component, duplicate-routes]
level: intro
status: docs-checked
description: "Add standalone React or Markdown pages under src/pages, how file paths map to routes, ignored underscore files, and duplicate route warnings."
sources:
  - https://raw.githubusercontent.com/facebook/docusaurus/main/website/docs/guides/creating-pages.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`@docusaurus/plugin-content-pages` creates one-off pages. Pages have no sidebars; only docs do.

React page: export a component and wrap content in `Layout` to get the navbar and footer.

```jsx title="/src/pages/helloReact.js"
import Layout from '@theme/Layout';

export default function Hello() {
  return <Layout title="Hello" description="Hello React Page">...</Layout>;
}
```

`.tsx` works too.

Markdown page (always uses the theme layout, so less flexible):

```md title="/src/pages/helloMarkdown.md"
---
title: my hello page title
description: my hello page description
hide_table_of_contents: true
---
```

Routing follows the directory hierarchy: `index.js` is `[baseUrl]`, `foo.js` is `[baseUrl]/foo`, `foo/index.js` is `[baseUrl]/foo/`. Prefer `support/index.js` so you can co-locate a CSS module; you still import it yourself.

Files starting with `_`, test files (`.test.js`) and files in `__tests__` are not turned into pages by default (the `exclude` option). Put reusable components elsewhere or exclude them.

Duplicate routes produce a warning on start or build (behaviour set by `onDuplicateRoutes`), but the build succeeds; the page created last overrides the others.

## Checked

2026-11-04: read the Docusaurus Creating Pages guide in full. Confirmed Layout usage, .tsx, Markdown page front matter, routing examples, co-located CSS module, underscore and test file exclusion, duplicate route behaviour with onDuplicateRoutes. Nothing removed.

Method: documentation only; no commands were run.
