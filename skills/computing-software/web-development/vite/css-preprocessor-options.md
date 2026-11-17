---
id: computing-software.web-development.vite.css-preprocessor-options
name: css-preprocessor-options
category: computing-software
field: web-development
product: vite
tags: [preprocessor-options, additional-data, preprocessor-max-workers, css-dev-sourcemap]
level: advanced
status: docs-checked
description: "Pass options to Sass, Less and Stylus via css.preprocessorOptions, inject code with additionalData, limit preprocessorMaxWorkers, and enable css.devSourcemap."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/config/shared-options.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`css.preprocessorOptions` is keyed by file extension:
- `sass`/`scss`: uses `sass-embedded` if installed, else `sass` (embedded is recommended for performance).
- `less`: Less options.
- `styl`/`stylus`: only `define` is supported, as an object.

```js
css: {
  preprocessorOptions: {
    less: { math: 'parens-division' },
    scss: { importers: [/* ... */] },
  },
}
```

`additionalData` (string, or `(source, filename) => string | { content, map? }`) injects code into each style. Real styles, not just variables, get duplicated in the bundle. Relative paths break because the same code is prepended in different directories; use absolute paths or aliases.

```js
scss: { additionalData: `$injectedColor: orange;` }
```

`css.preprocessorMaxWorkers`: `number | true`, default `true` (CPUs minus 1). `0` runs preprocessors on the main thread; depending on options Vite may use the main thread anyway.

`css.devSourcemap` (experimental): default `false`; enables sourcemaps in dev.

## Checked

2026-11-04. Confirmed against the Vite shared options page (docs/config/shared-options.md): preprocessorOptions keys, sass-embedded preference, stylus define only, additionalData notes, preprocessorMaxWorkers, devSourcemap. Nothing removed.

Method: documentation only; no commands were run.
