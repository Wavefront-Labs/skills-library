---
id: computing-software.web-development.storybook.builder-vite
name: builder-vite
category: computing-software
field: web-development
product: storybook
tags: [vite-builder, viteconfig, vitefinal, vite-config-path, builder-options]
level: practitioner
status: docs-checked
description: "Customise the Vite builder with viteFinal, environment-based config and viteConfigPath."
sources:
  - https://storybook.js.org/docs/builders/vite
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Vite builder

Goal: tailor Vite for Storybook.

The Vite builder is already installed and configured for Vite projects. To opt in manually, install `@storybook/builder-vite` and set `core: { builder: '@storybook/builder-vite' }`. Storybook merges its framework defaults with your `vite.config.*`; the docs recommend putting configuration in the Vite config file where possible.

Only `build.target` is inherited from your Vite `build` options. Set other build options (such as `build.chunkSizeWarningLimit`) in `viteFinal`.

Customise in `main.ts` with the async `viteFinal`, which receives the default config and returns the updated one:

```ts
async viteFinal(config, { configType }) {
  const { mergeConfig } = await import('vite');
  if (configType === 'DEVELOPMENT') {
    // development-only config
  }
  if (configType === 'PRODUCTION') {
    // production-only config
  }
  return mergeConfig(config, {
    // shared config
  });
},
```

By default the builder looks for the Vite config in the root of the Storybook project. Point elsewhere with the builder option `viteConfigPath`, under `core.builder.options`:

```ts
core: {
  builder: {
    name: '@storybook/builder-vite',
    options: { viteConfigPath: '../customVite.config.js' },
  },
},
```

A path to a non-existent file stops Storybook loading any Vite config. The builder option `configLoader` is passed to Vite, equivalent to its `--configLoader` flag.

Verify: aliases from `viteFinal` resolve in a story import.

## Checked
Date: 2026-11-04. Read the Vite builder page (storybookjs/storybook main branch docs, commit e4ec607) and its code snippets.
Confirmed: registration, `build.target` only, `viteFinal` with `configType`, `viteConfigPath`, `configLoader`.
Fixed: `viteConfigPath` lives in `core.builder.options`, not in framework options. Replaced an invented `base` example with the page's DEVELOPMENT/PRODUCTION example.
Method: documentation only; no commands were run.
