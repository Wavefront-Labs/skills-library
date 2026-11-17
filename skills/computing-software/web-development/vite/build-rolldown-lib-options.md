---
id: computing-software.web-development.vite.build-rolldown-lib-options
name: build-rolldown-lib-options
category: computing-software
field: web-development
product: vite
tags: [build-rolldown-options, build-lib-option, preserve-entry-signatures, dynamic-import-vars-options]
level: advanced
status: docs-checked
description: "build.rolldownOptions merging, preserveEntrySignatures defaults, rollupOptions alias, build.lib entry, name, formats, fileName, cssFileName, dynamicImportVarsOptions."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/config/build-options.md
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/config/shared-options.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`build.rolldownOptions` (`RolldownOptions`) is merged with Vite's internal Rolldown options. Vite overrides `preserveEntrySignatures` when unset: `false` for client builds, `'strict'` for library builds, `'allow-extension'` for SSR. Prefer the top-level `input` over `build.rolldownOptions.input` (it also applies in dev); if the latter is set it overrides `input` for build only. `build.rollupOptions` is a deprecated alias.

`build.lib`: `{ entry?, name?, formats?, fileName?, cssFileName? }`. `entry` defaults to top-level `input`; one is required (no HTML entry). `name` is the global variable and is required for `umd` or `iife`. Default `formats` are `['es', 'umd']`, or `['es', 'cjs']` with multiple entries. `fileName` defaults to the `package.json` name, or is a function `(format, entryName)`. `cssFileName` defaults to a string `fileName`, else the package name.

```js
build: {
  lib: {
    entry: ['src/main.js'],
    fileName: (format, entryName) => `my-lib-${entryName}.${format}.js`,
    cssFileName: 'my-lib-style',
  },
}
```

`build.dynamicImportVarsOptions`: `{ include?, exclude? }` string or RegExp filters for transforming variable dynamic imports.

## Checked

Date: 2026-11-07. Read build-options.md (read in full) (`build.rolldownOptions`, `build.rollupOptions` deprecated alias, `build.lib`, `build.dynamicImportVarsOptions`) and the `input` section of shared-options.md (read in full). Every claim in the skill (preserveEntrySignatures defaults false/'strict'/'allow-extension', top-level `input` precedence, lib `formats` defaults, `fileName` and `cssFileName` fallbacks) matched; nothing trimmed.

Method: documentation only; no commands were run.
