---
id: computing-software.web-development.vite.plugin-ordering-apply
name: plugin-ordering-apply
category: computing-software
field: web-development
product: vite
tags: [plugin-enforce-order, plugin-apply-property, rolldown-plugin-compat, build-only-plugins]
level: advanced
status: docs-checked
description: "Plugin enforce order list, the apply property (string or function), when Rolldown or Rollup plugins work in Vite, and build.rolldownOptions.plugins."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/api-plugin.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`enforce: 'pre' | 'post'` sets order. Resolved order: Alias, user `pre` plugins, Vite core plugins, user plugins without enforce, Vite build plugins, user `post` plugins, Vite post build plugins (minify, manifest, reporting). This is separate from per-hook `order`.

`apply: 'build' | 'serve'` limits a plugin; a function allows finer control:

```js
apply(config, { command }) {
  return command === 'build' && !config.build.ssr
}
```

Compatibility: a Rolldown or Rollup plugin should work as a Vite plugin if it does not use `moduleParsed`, does not rely on Rolldown-specific options like `transform.inject`, and does not tightly couple bundle-phase and output-phase hooks. Build-only ones can go under `build.rolldownOptions.plugins`, which behaves like `enforce: 'post'` plus `apply: 'build'`. Or add the properties yourself:

```js
plugins: [{ ...example(), enforce: 'post', apply: 'build' }]
```

## Checked

Date: 2026-11-07

Read api-plugin.md in full (Plugin Ordering, Conditional Application, Rolldown Plugin Compatibility). Confirmed the seven-step order, apply string and function form, compatibility criteria and build.rolldownOptions.plugins equivalence. Nothing removed.

Method: documentation only; no commands were run.
