---
id: computing-software.web-development.vitepress.build-time-data-loaders
name: build-time-data-loaders
category: computing-software
field: web-development
product: vitepress
tags: [vitepress, data-loaders, data-loading, build-time-data, watch, defineloader, vitepress-config-global]
level: advanced
status: docs-checked
description: "Write *.data.js loaders whose load() runs at build time in Node, watch local files with globs, type with defineLoader, and read the config."
sources:
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/guide/data-loading.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A data loader file ends in `.data.js` or `.data.ts` and default-exports an object with `load()`. VitePress calls `load()` and exposes the result as the `data` named export of the same module; the loader never exports `data` itself.

```js
// example.data.js
export default {
  load() { return { hello: 'world' } }
}
```

```vue
<script setup>
import { data } from './example.data.js'
</script>
<pre>{{ data }}</pre>
```

`load()` runs **only at build time** in Node (so Node APIs and npm dependencies are available and never shipped), and the result is serialized as JSON into the client bundle. It may be async, for example `return (await fetch('...')).json()`.

**Local files with `watch`.** Provide glob patterns (fast-glob syntax) relative to the loader file; `load(watchedFiles)` receives absolute paths and file changes trigger hot updates.

```js
import fs from 'node:fs'
import { parse } from 'csv-parse/sync'
export default {
  watch: ['./data/*.csv'],
  load(files) {
    return files.map((f) => parse(fs.readFileSync(f, 'utf-8'), { columns: true, skip_empty_lines: true }))
  }
}
```

The CSV parser is not shipped to the client.

**Typed loaders (TypeScript):**

```ts
import { defineLoader } from 'vitepress'
export interface Data { /* data type */ }
declare const data: Data
export { data }
export default defineLoader({
  watch: ['...'],
  async load(): Promise<Data> { /* ... */ }
})
```

**Config access inside a loader:**

```ts
import type { SiteConfig } from 'vitepress'
const config: SiteConfig = (globalThis as any).VITEPRESS_CONFIG
```

Keep payloads small: everything returned is inlined into the JS.

## Checked

2026-11-04. Confirmed against the VitePress data-loading guide (.data.js/.data.ts, load(), data named export, async loaders, watch globs and absolute paths, csv-parse example, defineLoader, VITEPRESS_CONFIG). Removed: the Verify step.

Method: documentation only; no commands were run.
