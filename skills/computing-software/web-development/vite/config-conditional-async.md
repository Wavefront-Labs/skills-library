---
id: computing-software.web-development.vite.config-conditional-async
name: config-conditional-async
category: computing-software
field: web-development
product: vite
tags: [conditional-config, config-function, async-config, is-ssr-build]
level: practitioner
status: docs-checked
description: "Export a config function receiving command, mode, isSsrBuild and isPreview, compare flags explicitly, and return an async config when setup needs await."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/config/index.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Export a function to vary options by command, mode, SSR build or preview:

```js
export default defineConfig(({ command, mode, isSsrBuild, isPreview }) => {
  if (command === 'serve') {
    return { /* dev specific config */ }
  } else {
    // command === 'build'
    return { /* build specific config */ }
  }
})
```

`command` is `serve` during dev (`vite`, `vite dev` and `vite serve` are aliases) and `build` for `vite build`.

`isSsrBuild` and `isPreview` are optional flags. Tools that load the config may not support them and pass `undefined`, so compare explicitly with `true` and `false`.

Async work: export an async function, still wrapped in `defineConfig` for intellisense:

```js
export default defineConfig(async ({ command, mode }) => {
  const data = await asyncFunction()
  return { /* vite config */ }
})
```

## Checked

Date: 2026-11-07. Read config/index.md in full (Conditional Config and Async Config sections). The `command`/`mode`/`isSsrBuild`/`isPreview` arguments, the serve/build alias note, the `undefined` caveat and the async `defineConfig` example all matched; nothing trimmed.

Method: documentation only; no commands were run.
