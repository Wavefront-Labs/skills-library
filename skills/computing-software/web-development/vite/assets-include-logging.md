---
id: computing-software.web-development.vite.assets-include-logging
name: assets-include-logging
category: computing-software
field: web-development
product: vite
tags: [assets-include-option, log-level-option, custom-logger, clear-screen-option]
level: practitioner
status: docs-checked
description: "Treat extra file types as assets with assetsInclude, set logLevel, filter warnings with customLogger from createLogger, and keep the terminal with clearScreen false."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/config/shared-options.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`assetsInclude` (`string | RegExp | (string | RegExp)[]`): extra picomatch patterns treated as static assets. They are excluded from the plugin transform pipeline when referenced from HTML or requested via `fetch` or XHR, and importing them from JS returns the resolved URL (an `enforce: 'pre'` plugin can override).

```js
export default defineConfig({ assetsInclude: ['**/*.gltf'] })
```

`logLevel`: `'info' | 'warn' | 'error' | 'silent'`, default `'info'`.

`customLogger`: an object with `info`, `warn`, `warnOnce`, `error`, `clearScreen`, `hasErrorLogged` and `hasWarned`. Start from `createLogger()` and override:

```ts
const logger = createLogger()
const loggerWarn = logger.warn
logger.warn = (msg, options) => {
  if (msg.includes('vite:css') && msg.includes(' is empty')) return
  loggerWarn(msg, options)
}
export default defineConfig({ customLogger: logger })
```

`clearScreen`: default `true`; `false` (or `--clearScreen false`) stops Vite clearing the terminal for certain messages.

## Checked

2026-11-04. Confirmed against the Vite shared options page (docs/config/shared-options.md): assetsInclude behaviour, logLevel values and default, customLogger interface and createLogger example, clearScreen. Nothing removed.

Method: documentation only; no commands were run.
