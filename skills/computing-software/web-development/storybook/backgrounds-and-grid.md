---
id: computing-software.web-development.storybook.backgrounds-and-grid
name: backgrounds-and-grid
category: computing-software
field: web-development
product: storybook
tags: [backgrounds, background-colors, grid, backgrounds-globals, canvas-background]
level: intro
status: docs-checked
description: "Configure background colors and the alignment grid, set a default and lock a story to one background."
sources:
  - https://storybook.js.org/docs/essentials/backgrounds
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Backgrounds and grid

Goal: render stories on the right background.

Defaults are a light and a dark background. Configure in the preview file:

```ts
parameters: {
  backgrounds: {
    options: {
      dark: { name: 'Dark', value: '#333' },
      light: { name: 'Light', value: '#F7F9F2' },
      maroon: { name: 'Maroon', value: '#400' },
    },
  },
},
initialGlobals: { backgrounds: { value: 'light' } },
```

- Override `options` at component or story level with parameters inheritance.
- Lock a story's background with `globals: { backgrounds: { value: 'dark' } }`; the toolbar can then not change it.
- Disable: `parameters: { backgrounds: { disable: true } }`.
- Grid: toggle from the toolbar or set `globals.backgrounds.grid = true`. Grid parameters have defaults: `cellAmount` 5, `cellSize` 20, `opacity` 0.5.

API: globals `backgrounds.value` (key of a configured background) and `backgrounds.grid` (boolean).

Gotcha: `value` must match a key in `options`.

Verify: the toolbar lists your backgrounds and the canvas color changes.

## Checked
Date: 2026-11-04. Read the Backgrounds page (storybookjs/storybook main branch docs, commit e4ec607).
Confirmed: options shape, `initialGlobals`, story-level lock, `disable`, globals names.
Added: the grid parameter defaults.
Method: documentation only; no commands were run.
