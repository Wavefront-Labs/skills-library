---
id: computing-software.web-development.vite.public-base-path
name: public-base-path
category: computing-software
field: web-development
product: vite
tags: [base-option, relative-base, base-url-constant]
level: practitioner
status: docs-checked
description: "Deploy under a nested path with the base option or --base, use a relative base, and build dynamic URLs with import.meta.env.BASE_URL."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/build.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Set the `base` config option (or `vite build --base=/my/public/path/`) to deploy under a nested public path. JS-imported asset URLs, CSS `url()` references and asset references in `.html` files are rewritten at build.

For URLs concatenated on the fly use `import.meta.env.BASE_URL`. It is statically replaced, so it must appear exactly like that; `import.meta.env['BASE_URL']` will not work.

Unknown base in advance? Use a relative base so generated URLs are relative to each file:

```js
export default { base: './' } // or ''
```

A relative base requires `import.meta` support. For browsers without it, use the `legacy` plugin.

For separate locations of HTML, hashed assets and public files, see the advanced base option `experimental.renderBuiltUrl`.

## Checked

Date: 2026-11-07

Read build.md in full (Public Base Path, Relative base, Advanced Base Options). Confirmed base and --base, adjusted URL kinds, import.meta.env.BASE_URL static replacement, relative base values and import.meta requirement with the legacy plugin, and experimental.renderBuiltUrl. Nothing removed.

Method: documentation only; no commands were run.
