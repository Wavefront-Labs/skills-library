---
id: computing-software.web-development.vitepress.default-theme-layouts-doc-page-home
name: default-theme-layouts-doc-page-home
category: computing-software
field: web-development
product: vitepress
tags: [vitepress, layout, doc-layout, page-layout, home-layout, layout-false, custom-layout, vp-doc]
level: practitioner
status: docs-checked
description: "Choose layout: doc, page, home, false or a custom registered component, and know which features each enables."
sources:
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/reference/default-theme-layout.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Set `layout` in page frontmatter. If omitted the page is `doc`.

- **`doc`**: styles the Markdown content as documentation by wrapping it in the `vp-doc` class, so generic elements like `p` and `h2` get styled (custom HTML inside will be affected too). Enables doc-only features: edit link, prev/next links, outline, and Carbon Ads.
- **`page`**: a blank page. Markdown is still parsed and all extensions work, but the content gets no default styling, which suits fully custom pages. A sidebar still appears if the page matches a sidebar config.
- **`home`**: templated homepage with `hero` and `features` options.
- **`layout: false`**: no layout at all, so no sidebar, navbar or footer by default; for fully custom landing pages.
- **Custom**: `layout: foo` looks up a component named `foo` registered in context.

```ts
// .vitepress/theme/index.ts
import DefaultTheme from 'vitepress/theme'
import Foo from './Foo.vue'
export default {
  extends: DefaultTheme,
  enhanceApp({ app }) { app.component('foo', Foo) }
}
```

```md
---
layout: foo
---
```

Related page-level toggles (`navbar`, `sidebar`, `aside`, `footer`) are in the frontmatter options skill.

## Checked

2026-11-04. Confirmed against the VitePress default-theme Layout page (doc, page, home, no layout, custom layout) and the Frontmatter Config page (layout values and default doc; navbar, sidebar, aside, footer toggles). Removed: the advice on choosing between page and false, and the Verify step.

Method: documentation only; no commands were run.
