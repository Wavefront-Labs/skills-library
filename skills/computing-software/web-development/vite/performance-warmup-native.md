---
id: computing-software.web-development.vite.performance-warmup-native
name: performance-warmup-native
category: computing-software
field: web-development
product: vite
tags: [server-warmup, request-waterfall, debug-transform, native-tooling]
level: advanced
status: docs-checked
description: "Warm up frequently used files with server.warmup.clientFiles to break transform waterfalls, find them with --debug transform, and do less or use native tooling."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/performance.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The dev server transforms files only when requested, so a slow file delays everything it imports: `main.js -> BigComponent.vue -> big-utils.js -> large-data.json` forms a waterfall because imports are known only after a transform.

Find hot files:

```bash
vite --debug transform
# vite:transform 102.54ms /src/utils/big-utils.js +1ms
```

Warm them:

```js
export default defineConfig({
  server: {
    warmup: {
      clientFiles: [
        './src/components/BigComponent.vue',
        './src/utils/big-utils.js',
      ],
    },
  },
})
```

Only warm frequently used files so startup is not overloaded. `--open` or `server.open` also warms the app entry or the given URL.

Do less work: use CSS instead of Sass/Less/Stylus where possible (nesting via PostCSS or Lightning CSS); import SVGs as strings or URLs rather than transforming them into framework components. Use native tooling where worthwhile, such as the experimental LightningCSS support.

## Checked

Date: 2026-11-07

Read performance.md in full. Confirmed the waterfall example, vite --debug transform log line, server.warmup.clientFiles, the warm-only-frequent advice, --open and server.open warm-up, and the do-less and native-tooling bullets. Nothing removed.

Method: documentation only; no commands were run.
