---
id: computing-software.web-development.vite.oxc-option
name: oxc-option
category: computing-software
field: web-development
product: vite
tags: [oxc-option, oxc-include-exclude, esbuild-option-deprecated]
level: practitioner
status: docs-checked
description: "The oxc option extends Oxc Transformer options: JSX runtime and pragma, include and exclude globs, jsxInject, disabling with false; esbuild option is deprecated."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/config/shared-options.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`oxc` is `OxcOptions | false`; `OxcOptions` extends the Oxc Transformer options. The common case is JSX:

```js
export default defineConfig({
  oxc: {
    jsx: {
      runtime: 'classic',
      pragma: 'h',
      pragmaFrag: 'Fragment',
    },
  },
})
```

By default Oxc transforms `ts`, `jsx` and `tsx` files. Customize with `oxc.include` and `oxc.exclude`: a regex, a picomatch pattern, or an array of either.

`oxc.jsxInject` injects JSX helper imports into every file Oxc transforms:

```js
oxc: { jsxInject: `import React from 'react'` }
```

`oxc: false` disables Oxc transformation.

`esbuild` is deprecated and is converted to `oxc` internally; use `oxc`.

## Checked

Date: 2026-11-07

Read shared-options.md in full (oxc and esbuild sections) and features.md in full (JSX section). Confirmed OxcOptions | false, the JSX example, default ts/jsx/tsx scope, include/exclude forms, jsxInject, false to disable, and esbuild deprecated and converted internally. Nothing removed.

Method: documentation only; no commands were run.
