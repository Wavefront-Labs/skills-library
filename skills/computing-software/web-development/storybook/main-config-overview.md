---
id: computing-software.web-development.storybook.main-config-overview
name: main-config-overview
category: computing-software
field: web-development
product: storybook
tags: [main-config, main-js, storybook-config, config-dir, presets]
level: practitioner
status: docs-checked
description: "Understand the .storybook main config fields: stories, addons, framework, staticDirs, typescript, core, docs, features, refs, env."
sources:
  - https://storybook.js.org/docs/configure
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Main configuration (.storybook/main)

Goal: know what the main config controls.

Storybook is configured by the `.storybook` folder (change the folder with the `-c` flag on `storybook dev` and `storybook build`). The main config (`main.js|ts`) defines the location of your stories, the addons you use, feature flags and other project settings. It is a preset, so it can be customised further (see Storybook's docs on writing presets). Common fields:

| Field | Purpose |
| --- | --- |
| `stories` | array of globs of story files, relative to main |
| `staticDirs` | directories of static files to serve, e.g. `['../public']` |
| `addons` | addons loaded by Storybook, e.g. `['@storybook/addon-docs']` |
| `framework` | framework settings, e.g. `{ name: '@storybook/svelte-vite', options: {} }` |
| `typescript` | how TypeScript files are handled, e.g. `{ check: false, checkOptions: {} }` |
| `core` | internal features, e.g. `{ disableTelemetry: true }` |
| `docs` | auto-generated docs, e.g. `{ defaultName: 'Documentation' }` |
| `features` | additional features |
| `refs` | Storybook composition, e.g. `{ example: { title: 'ExampleStorybook', url: 'https://your-url.com' } }` |
| `logLevel` | browser terminal log level, useful for debugging, e.g. `'debug'` |
| `webpackFinal` | customise the Webpack setup |
| `viteFinal` | customise the Vite setup when using the Vite builder |
| `env` | custom Storybook environment variables |
| `build` | optimise the production build by excluding specific features, e.g. `{ test: {} }` |

Story loading: by default stories load from a glob matching all files with extension `.stories.*`, colocated with the component (`Button.js` next to `Button.stories.js`). Change the naming convention by altering the glob (picomatch syntax). `stories` also accepts configuration objects, a directory, or custom logic.

Other config files in `.storybook`:
- `preview.js`: controls how stories render; export `decorators`, `parameters` and `globalTypes`. Loaded in the Canvas preview iframe, so use it for global code such as CSS imports or JavaScript mocks.
- `manager.js`: controls the Storybook UI (the manager): UI options and theme.

## Checked
Read the whole configure page (storybookjs/storybook docs/configure/index.mdx, source of the cited page) on 2026-11-08. Confirmed the `.storybook` folder, the `-c` flag, the preset note, every field in the table with its example, default story loading, `preview.js` keys and `manager.js` role. Removed: the code example, the `preview-head.html`/`preview-body.html` mention, the restart-after-editing claim (not on the page) and the `'Docs'` default name (page example is `'Documentation'`).
Method: docs-only read of cited pages, 2026-11-08
