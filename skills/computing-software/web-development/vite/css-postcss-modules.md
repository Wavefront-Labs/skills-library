---
id: computing-software.web-development.vite.css-postcss-modules
name: css-postcss-modules
category: computing-software
field: web-development
product: vite
tags: [css-import-inlining, postcss-config, css-modules, locals-convention]
level: practitioner
status: docs-checked
description: "Vite CSS handling: HMR style injection, @import inlining with aliases, url() rebasing, automatic PostCSS config, and .module.css imports."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/features.md
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/config/shared-options.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Importing a `.css` file injects it via a `<style>` tag with HMR.

- `@import` is inlined through `postcss-import` and Vite aliases are respected. All CSS `url()` references are rebased even across directories.
- A valid PostCSS config (any format `postcss-load-config` supports, such as `postcss.config.js`) is applied automatically to all imported CSS. CSS minification runs after PostCSS using `build.cssTarget`.
- Files ending in `.module.css` are CSS modules and return an object:

```js
import classes from './example.module.css'
document.getElementById('foo').className = classes.red
```

Configure with `css.modules`. If `css.modules.localsConvention` enables camelCase (for example `camelCaseOnly`), named imports work:

```js
// .apply-color -> applyColor
import { applyColor } from './example.module.css'
```

Add `.module` before the extension to combine with pre-processors, for example `style.module.scss`.

## Checked

Date: 2026-11-07. Read the CSS section of features.md (features.md read in full: `@import` inlining, PostCSS, CSS Modules, pre-processor modules) and `css.modules` in shared-options.md (read in full). `postcss-import`, url rebasing, PostCSS minification order with `build.cssTarget`, `.module.css` and `localsConvention: 'camelCaseOnly'` named imports matched; nothing trimmed.

Method: documentation only; no commands were run.
