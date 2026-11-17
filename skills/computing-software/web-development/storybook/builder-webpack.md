---
id: computing-software.web-development.storybook.builder-webpack
name: builder-webpack
category: computing-software
field: web-development
product: storybook
tags: [webpack-builder, webpackfinal, lazy-compilation, fscache, swc]
level: practitioner
status: docs-checked
description: "Configure the Webpack 5 builder with webpackFinal, lazyCompilation, fsCache and SWC support."
sources:
  - https://storybook.js.org/docs/builders/webpack
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Webpack builder

Goal: extend Storybook's Webpack config.

Webpack 5 is supported; Webpack 4 is not. Options go under `core.builder.options`:

```ts
core: { builder: { name: '@storybook/builder-webpack5', options: { lazyCompilation: true, fsCache: true } } },
```
- `lazyCompilation`: Webpack lazy compilation
- `fsCache`: filesystem cache

Extend with `webpackFinal`, which receives the config and must return it:

```ts
webpackFinal: async (config) => {
  config.module?.rules?.push({ test: /\.scss$/, use: ['style-loader', 'css-loader', 'sass-loader'] });
  return config;
},
```

Tips:
- Append to `config.plugins` rather than overwriting it.
- For loaders without a `test`, exclude `.ejs` files.
- Debug the final config with `npm run storybook -- --debug-webpack` (or `storybook build --debug-webpack`).
- Compiler addons: `@storybook/addon-webpack5-compiler-swc` for SWC, `@storybook/addon-webpack5-compiler-babel` for Babel.
- The Vitest addon needs Vite, so Webpack projects must migrate to use it.

Verify: the loader you added transforms its file type in a story.

## Checked
Date: 2026-11-04. Read the Webpack builder page, CLI options page and Interaction tests page (storybookjs/storybook main branch docs, commit e4ec607).
Confirmed: option names, `webpackFinal` contract, `.ejs` note, debug flag, compiler addons, Webpack 4 unsupported, Vite requirement for the Vitest addon.
Removed: a claim about Rspack/Rsbuild via `storybook-rsbuild`, not on the pages read.
Method: documentation only; no commands were run.
