---
id: computing-software.web-development.docusaurus.module-shorthands
name: module-shorthands
category: computing-software
field: web-development
product: docusaurus
tags: [module-shorthands, name-resolution, scoped-packages, plugin-naming, themes-field]
level: advanced
status: docs-checked
description: "How Docusaurus resolves short plugin, theme and preset names such as sitemap or content-blog, including scoped packages, and why the field you use matters."
sources:
  - https://raw.githubusercontent.com/facebook/docusaurus/main/website/docs/using-plugins.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
For a name in `plugins`, `themes` or `presets`, Docusaurus tries in order:

1. `[name]` (like `content-docs`)
2. `@docusaurus/[moduleType]-[name]` (like `@docusaurus/plugin-content-docs`)
3. `docusaurus-[moduleType]-[name]`

`moduleType` is `preset`, `theme` or `plugin` depending on which config field holds the name, so use the right field if you rely on shorthands. The first found module loads.

```js
plugins: ['content-blog', 'content-pages'],
themes: ['classic'],
```

Scoped names (starting with `@`) are split into scope and name at the first slash. With no name (`@my-company`) it loads `[scope]/docusaurus-[moduleType]`. Otherwise it tries `[scope]/[name]`, then `[scope]/docusaurus-[moduleType]-[name]`.

| Declaration in `plugins` | May resolve as |
| --- | --- |
| `awesome` | `docusaurus-plugin-awesome` |
| `sitemap` | `@docusaurus/plugin-sitemap` |
| `@my-company` | `@my-company/docusaurus-plugin` |
| `@my-company/awesome` | `@my-company/docusaurus-plugin-awesome` |
| `@my-company/awesome/web` | `@my-company/docusaurus-plugin-awesome/web` |

Unlike ESLint or Babel there is no mandatory naming convention, so resolution follows the priority above and is not certain.

## Checked

2026-11-04: read the Docusaurus Using Plugins page, section Module shorthands, and the Using themes tip. Confirmed the resolution order, moduleType by field, scoped name rules and the example table. Nothing removed.

Method: documentation only; no commands were run.
