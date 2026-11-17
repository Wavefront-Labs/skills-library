---
id: computing-software.web-development.storybook.addon-presets-and-install
name: addon-presets-and-install
category: computing-software
field: web-development
product: storybook
tags: [presets, addon-presets, managerentries, previewannotations, install-addons]
level: advanced
status: docs-checked
description: "Install addons manually or with storybook add, and write presets that hook into Vite, Webpack, Babel and previews."
sources:
  - https://storybook.js.org/docs/addons/writing-presets
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Installing addons and writing presets

Goal: add addons and package reusable configuration.

Install:

```shell
npx storybook add @storybook/addon-a11y
```
`storybook add` does not work for preset addons, and installing several addons in one command installs only the first. Or install manually: add the package, then list it in `main.ts`:

```ts
addons: ['@storybook/addon-a11y'],
```
`storybook remove <addon>` uninstalls and unregisters it.

Presets are bundled configuration for addons. Two kinds:
- Local presets: encapsulate addon-specific configuration such as builder support.
- Root-level presets: user-facing, register the addon without further setup.

Preset APIs:
- `viteFinal(config)` and `webpackFinal(config)`: modify the builder config
- `babelDefault(config)`: add Babel config, only for frameworks that use Babel
- `managerEntries(entry = [])`: add manager-side files
- `previewAnnotations(entry = [])`: add decorators or parameters to the preview
- `addons`: have a preset load other addons so users do not need technical `managerEntries`

Root preset file:

```js
export const previewAnnotations = [import.meta.resolve('./dist/preview')];
export const managerEntries = [import.meta.resolve('./dist/manager')];
```

Verify: the addon's panel or behavior appears without extra user configuration.

## Checked
Date: 2026-11-04. Read the Writing presets and Install addons pages (storybookjs/storybook main branch docs, commit e4ec607).
Confirmed: preset kinds, preset API list, add/remove commands.
Fixed: replaced the `require.resolve` example with the page's `import.meta.resolve` form. Added the two `storybook add` limits.
Method: documentation only; no commands were run.
