---
id: computing-software.web-development.vite.plugin-authoring-conventions
name: plugin-authoring-conventions
category: computing-software
field: web-development
product: vite
tags: [plugin-authoring, plugin-naming, plugin-factory, plugin-presets, vite-plugin-inspect]
level: practitioner
status: docs-checked
description: "Author a Vite plugin: extends Rolldown's plugin interface, factory function pattern, vite-plugin- and rolldown-plugin- naming, keywords, presets and vite-plugin-inspect."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/api-plugin.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Vite plugins extend Rolldown's plugin interface with Vite-specific options, so one plugin can serve dev and build. Read Rolldown's plugin docs first and check the Features guide and community plugins before writing one. A plugin can be inlined in `vite.config.js`.

Conventions:
- Compatible Rolldown plugin (no Vite-only hooks): `rolldown-plugin-` prefix; `package.json` keywords `rolldown-plugin` and `vite-plugin`.
- Vite-only plugin: `vite-plugin-` prefix, keyword `vite-plugin`, and a docs section explaining why it is Vite only.
- Framework-specific: `vite-plugin-vue-`, `vite-plugin-react-`, `vite-plugin-svelte-`.

Write a factory function returning the plugin object (`name` is required and shows in warnings and errors). A factory may return an array as a preset; arrays are flattened and falsy entries ignored:

```js
export default function framework(config) {
  return [frameworkRefresh(config), frameworkDevTools(config)]
}
```

Debug with `vite-plugin-inspect`: visit `localhost:5173/__inspect/` to see the transformation stack.

## Checked

Date: 2026-11-07

Read api-plugin.md in full (Authoring a Plugin, Conventions, Plugins Config, Simple Examples). Confirmed the Rolldown-based plugin interface, naming prefixes and keywords, framework prefixes, factory function and required name, preset flattening and falsy plugins, and vite-plugin-inspect at /__inspect/. Nothing removed.

Method: documentation only; no commands were run.
