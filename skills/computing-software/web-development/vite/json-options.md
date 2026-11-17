---
id: computing-software.web-development.vite.json-options
name: json-options
category: computing-software
field: web-development
product: vite
tags: [json-named-exports-option, json-stringify, css-transformer-option]
level: practitioner
status: docs-checked
description: "json.namedExports and json.stringify (auto above 10kB) plus css.transformer and css.lightningcss option shapes."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/config/shared-options.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`json.namedExports` (boolean, default `true`): support named imports from `.json` files.

`json.stringify` (`boolean | 'auto'`, default `'auto'`): `true` turns imported JSON into `export default JSON.parse("...")`, significantly faster than an object literal, especially for large files. `'auto'` stringifies only when the data is bigger than 10kB.

`css.transformer` (experimental): `'postcss' | 'lightningcss'`, default `'postcss'`; selects the CSS processing engine. Duplicate `@import`s behave differently in postcss-import than in browsers.

`css.lightningcss` (experimental): Lightning CSS transform options, such as `targets`, `include`, `exclude`, `drafts`, `nonStandard`, `pseudoClasses`, `unusedSymbols` and `cssModules`. The full list is in the Lightning CSS repository's typings.

```js
css: { transformer: 'lightningcss', lightningcss: { drafts: { /* ... */ } } }
```

## Checked

2026-11-04. Confirmed against the Vite shared options page (docs/config/shared-options.md): json.namedExports, json.stringify and the 10kB auto threshold, css.transformer default and postcss-import @import note, css.lightningcss option names. Nothing removed.

Method: documentation only; no commands were run.
