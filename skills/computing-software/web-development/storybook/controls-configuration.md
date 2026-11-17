---
id: computing-software.web-development.storybook.controls-configuration
name: controls-configuration
category: computing-software
field: web-development
product: storybook
tags: [controls-parameters, include-exclude, sort-controls, expanded, disable-control]
level: practitioner
status: docs-checked
description: "Configure the Controls panel with include, exclude, sort, expanded, preset colors, matchers and disabling single controls."
sources:
  - https://storybook.js.org/docs/essentials/controls
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Controls: panel configuration

Goal: tune which controls show and how.

Set under `parameters.controls` (project, meta or story):

```ts
parameters: {
  controls: {
    include: ['label', /^on/],
    exclude: /^internal/,
    sort: 'requiredFirst',
    expanded: true,
    presetColors: [{ color: '#f00', title: 'Danger' }, 'green'],
    matchers: { color: /(background|color)$/i, date: /Date$/ },
    disableSaveFromUI: true,
  },
},
```

- `include` / `exclude`: `string[]` or `RegExp` by arg name.
- `sort`: `'none'` (default), `'alpha'`, `'requiredFirst'`.
- `expanded`: show description and default value in the panel (default false).
- `presetColors`: swatches for color controls (CSS color strings or `{ color, title }`).
- `disableSaveFromUI`: hide create or edit story from Controls (default false). Not supported with Svelte native CSF.
- `disable`: turn the panel off at one level.

Disable one arg's control but keep its docs row:
```ts
argTypes: { foo: { control: false } }
```
Remove it from the table entirely with `table: { disable: true }`.

Saving: adjust a control, then save as a new story or update the existing story; Storybook edits the story file for you.

Verify: only the expected controls appear, in the expected order.

## Checked
Date: 2026-11-04. Read the Controls page (storybookjs/storybook main branch docs, commit e4ec607).
Confirmed: every parameter, type and default listed above, `control: false` versus `table.disable`.
Method: documentation only; no commands were run.
