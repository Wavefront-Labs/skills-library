---
id: computing-software.web-development.vite.css-preprocessors
name: css-preprocessors
category: computing-software
field: web-development
product: vite
tags: [sass-support, less-support, stylus-support, preprocessor-install]
level: intro
status: docs-checked
description: "Use Sass, Less and Stylus in Vite: install only the pre-processor, alias and url() rebasing limits, and the preference for native CSS."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/features.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Vite targets modern browsers, so the docs recommend native CSS variables plus PostCSS plugins implementing CSSWG drafts (for example `postcss-nesting`) and plain standards-compliant CSS.

Built-in support covers `.scss`, `.sass`, `.less`, `.styl` and `.stylus`. No Vite-specific plugin is needed, just the pre-processor itself:

```bash
npm add -D sass-embedded   # or sass; for .scss and .sass
npm add -D less            # .less
npm add -D stylus          # .styl and .stylus
```

Behaviour:
- Sass and Less `@import` resolving respects Vite aliases.
- Relative `url()` in imported Sass/Less files from other directories is rebased. A `url()` starting with a variable or interpolation is not rebased.
- Stylus gets neither `@import` aliases nor url rebasing, due to its API constraints.
- Vue SFC `<style lang="sass">` is enabled automatically.
- CSS modules combine with pre-processors via `style.module.scss`.

## Checked

Date: 2026-11-07. Read the CSS Pre-processors section of features.md (features.md read in full). Install commands (`sass-embedded` or `sass`, `less`, `stylus`), alias and url rebasing support for Sass/Less, the variable/interpolation limit, Stylus limits, Vue SFC `lang` and `style.module.scss` matched; nothing trimmed.

Method: documentation only; no commands were run.
