---
id: computing-software.web-development.vite.build-watch-mode
name: build-watch-mode
category: computing-software
field: web-development
product: vite
tags: [build-watch, rebuild-on-change, watcher-options]
level: intro
status: docs-checked
description: "Rebuild on file changes with vite build --watch or build.watch WatcherOptions, and remember config changes need a restart."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/build.md
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/config/build-options.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Enable the Rolldown watcher with `vite build --watch`. Or set the underlying WatcherOptions through `build.watch`:

```js
export default defineConfig({
  build: {
    watch: {
      // https://rolldown.rs/reference/InputOptions.watch
    },
  },
})
```

`build.watch` is `WatcherOptions | null`, default `null`; `{}` enables the Rolldown watcher. With watching on, changes to files being bundled trigger a rebuild. Changes to the config and its dependencies require restarting the build command.

## Checked

Date: 2026-11-07. Read build.md in full (Rebuild on Files Changes) and the `build.watch` section of build-options.md (read in full). Added the type and default (`null`, `{}` enables). The config-restart sentence and the rolldown.rs WatcherOptions link target matched the page.

Method: documentation only; no commands were run.
