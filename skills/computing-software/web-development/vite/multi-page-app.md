---
id: computing-software.web-development.vite.multi-page-app
name: multi-page-app
category: computing-software
field: web-development
product: vite
tags: [multi-page-app, html-entry-input, nested-html]
level: practitioner
status: docs-checked
description: "Build a multi-page Vite app by listing several HTML entry points in the input option, including root-relative path resolution and entry naming."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/build.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
In dev, navigate or link to `/nested/` and it works like a static server. For the build, list the HTML files as entry points:

```js
import { resolve } from 'node:path'
import { defineConfig } from 'vite'

export default defineConfig({
  build: {
    rolldownOptions: {
      input: {
        main: resolve(import.meta.dirname, 'index.html'),
        nested: resolve(import.meta.dirname, 'nested/index.html'),
      },
    },
  },
})
```

Notes:
- With a different `root`, `import.meta.dirname` is still the folder of `vite.config.js`, so include the root in the `resolve` arguments.
- For HTML files Vite ignores the entry names in the input object and uses the resolved id of the file when emitting the HTML asset to dist, matching the dev server structure.
- The build guide's snippet puts `input` at the config top level, while its text says `rolldownOptions.input`; the shared `input` option documents the top-level form as the default for `build.rolldownOptions.input`.

## Checked

Date: 2026-11-07

Read build.md in full (Multi-Page App section) and shared-options.md in full (input option). Confirmed dev navigation to /nested/, the root and import.meta.dirname note, and the entry-name behaviour for HTML. The final bullet was rewritten: it was an unfinished self-correction; it now states that the page snippet places input at the config top level while the text says rolldownOptions.input, and shared-options documents top-level input as the default for build.rolldownOptions.input.

Method: documentation only; no commands were run.
