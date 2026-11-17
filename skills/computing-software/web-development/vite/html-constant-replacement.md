---
id: computing-software.web-development.vite.html-constant-replacement
name: html-constant-replacement
category: computing-software
field: web-development
product: vite
tags: [html-env-replacement, percent-syntax, transform-index-html-env]
level: intro
status: docs-checked
description: "Substitute import.meta.env values in HTML with %NAME% syntax, how missing keys are left alone, and the transformIndexHtml hook for complex needs."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/env-and-mode.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Any property of `import.meta.env` can be used in HTML with `%CONST_NAME%`:

```html
<h1>Vite is running in %MODE%</h1>
<p>Using data from %VITE_API_URL%</p>
```

If the key does not exist in `import.meta.env` (for example `%NON_EXISTENT%`) it is ignored and left as written. In JS, a missing `import.meta.env.NON_EXISTENT` is replaced by `undefined` instead.

Vite is deliberately unopinionated about complex replacement such as conditionals. Use an existing userland transformer plugin or a custom plugin that implements the `transformIndexHtml` hook.

## Checked

2026-11-04. Confirmed against the Vite Env Variables and Modes guide (docs/guide/env-and-mode.md, HTML Constant Replacement): %CONST_NAME% syntax, missing keys left unreplaced, transformIndexHtml hook. Nothing removed.

Method: documentation only; no commands were run.
