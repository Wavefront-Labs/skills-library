---
id: computing-software.web-development.vite.plugin-config-hooks
name: plugin-config-hooks
category: computing-software
field: web-development
product: vite
tags: [plugin-config-hook, config-resolved-hook, deep-merge-config, plugin-global-hooks]
level: advanced
status: docs-checked
description: "Vite plugin hooks config (return partial config or mutate) and configResolved (store final config), their kinds and the no-plugin-injection caveat."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/api-plugin.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Vite-specific hooks are ignored by Rollup.

`config(config, { mode, command, isSsrBuild, isPreview })`: async, sequential, global. Receives the raw user config (CLI merged with file). Return a partial config to be deeply merged (recommended), or mutate directly only when merging cannot do it. Plugins are resolved before this runs, so injecting plugins here has no effect.

```js
config: () => ({ resolve: { alias: { foo: 'bar' } } })
// or
config(config, { command }) { if (command === 'build') config.root = 'foo' }
```

`configResolved(resolvedConfig)`: async, parallel, global. Store the final config for other hooks, or branch on command:

```js
let config
return {
  name: 'read-config',
  configResolved(c) { config = c },
  transform(code, id) { if (config.command === 'serve') { /* dev */ } },
}
```

`command` is `serve` in dev (`vite`, `vite dev`, `vite serve` are aliases).

## Checked

Date: 2026-11-07

Read api-plugin.md in full (config and configResolved hooks). Confirmed the env keys, kinds (async sequential global; async parallel global), deep merge, the no-plugin-injection warning and the serve command aliases. Nothing removed.

Method: documentation only; no commands were run.
