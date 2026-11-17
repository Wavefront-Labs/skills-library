---
id: computing-software.web-development.vite.plugin-transform-virtual-module
name: plugin-transform-virtual-module
category: computing-software
field: web-development
product: vite
tags: [plugin-transform-hook, virtual-module, resolve-id-load, hook-filter, exact-regex]
level: advanced
status: docs-checked
description: "Plugin examples: transform custom file types with filter and handler, virtual modules via resolveId and load with a null-character prefix, hook filters and exactRegex."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/api-plugin.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Transform a file type; the object form carries a hook filter:

```js
transform: {
  filter: { id: /\.(my-file-ext)$/ },
  handler(src, id) {
    return { code: compileFileToJS(src), map: null }
  },
}
```

Virtual module: resolve the public id to a `\0`-prefixed id, then load it.

```js
import { exactRegex } from '@rolldown/pluginutils'
const virtualModuleId = 'virtual:my-module'
const resolved = '\0' + virtualModuleId
// resolveId: { filter: { id: exactRegex(virtualModuleId) }, handler() { return resolved } }
// load: { filter: { id: exactRegex(resolved) }, handler() { return `export const msg = "from virtual module"` } }
```

`\0` is not allowed in import URLs, so in dev the browser sees `/@id/__x00__{id}`; the id is decoded before plugin hooks run.

Hook filters cut Rust-to-JS calls. They need Rolldown, Rollup 4.38.0+ or Vite 6.3.0+; for older versions also test the filter inside the handler and return `null`. `@rolldown/pluginutils` offers `exactRegex` and `prefixRegex` (re-exported from `rolldown/filter`).

## Checked

Date: 2026-11-07

Read api-plugin.md in full (Simple Examples, Hook Filters). Confirmed the filter/handler transform, virtual module resolveId and load with exactRegex, the /@id/__x00__ encoding, Rollup 4.38.0+ and Vite 6.3.0+ filter support, and exactRegex and prefixRegex. Removed the backslash escape from the description.

Method: documentation only; no commands were run.
