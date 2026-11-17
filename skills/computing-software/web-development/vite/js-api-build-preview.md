---
id: computing-software.web-development.vite.js-api-build-preview
name: js-api-build-preview
category: computing-software
field: web-development
product: vite
tags: [build-api, preview-api, preview-server, resolve-config-api]
level: practitioner
status: docs-checked
description: "Programmatic build(), preview() and PreviewServer members, and resolveConfig(inlineConfig, command, defaultMode, defaultNodeEnv, isPreview)."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/api-javascript.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`build(inlineConfig?)` returns `Promise<RolldownOutput | RolldownOutput[] | RolldownWatcher>`:

```ts
import path from 'node:path'
import { build } from 'vite'

await build({
  root: path.resolve(import.meta.dirname, './project'),
  base: '/foo/',
  build: { rolldownOptions: { /* ... */ } },
})
```


`preview(inlineConfig?)` returns `Promise<PreviewServer>`:

```ts
const previewServer = await preview({ preview: { port: 8080, open: true } })
previewServer.printUrls()
previewServer.bindCLIShortcuts({ print: true })
```

`PreviewServer` has `config`, `middlewares` (connect app), `httpServer`, `resolvedUrls` (`null` if not listening), `printUrls()` and `bindCLIShortcuts()`.

`resolveConfig(inlineConfig, command, defaultMode = 'development', defaultNodeEnv = 'development', isPreview = false)` returns `ResolvedConfig`. `command` is `serve` for dev and preview, `build` for build.

## Checked

2026-11-07. Confirmed against the `build`, `preview`, `PreviewServer` and `resolveConfig` sections of guide/api-javascript.md (page read in full): signatures, return types, the examples, the `PreviewServer` members and the `command` rule. Removed the "use `build.write: false` to post-process the bundle" sentence, which the page does not contain.

Method: documentation only; no commands were run.
