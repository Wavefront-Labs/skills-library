---
id: computing-software.web-development.storybook.ui-config-and-theming
name: ui-config-and-theming
category: computing-software
field: web-development
product: storybook
tags: [manager-config, addons-setconfig, theming, brandimage, sidebar-config]
level: practitioner
status: docs-checked
description: "Configure the manager UI with addons.setConfig and brand it with a custom theme made via create()."
sources:
  - https://storybook.js.org/docs/configure/user-interface/theming
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Manager UI config and theming

Goal: change layout, sidebar and look of the Storybook UI.

`.storybook/manager.ts`:

```ts
import { addons } from 'storybook/manager-api';
import { themes } from 'storybook/theming';

addons.setConfig({
  theme: themes.dark,
  layout: { navSize: 300, panelPosition: 'right' },
  ui: { enableShortcuts: true },
  sidebar: { showRoots: false },
  selectedPanel: 'storybook/actions/panel',
});
```

`layout` options include `navSize`, `bottomPanelHeight`, `rightPanelWidth`, `panelPosition` (`bottom` or `right`), `showNav`, `showPanel`, `showToolbar`, `initialActive`. `toolbar` hides tools by addon id, e.g. `{ fullscreen: { hidden: true } }`. In Storybook 11, `layout` and `ui` must be under their own keys, not top level.

Custom theme:

```ts
import { create } from 'storybook/theming';

export default create({
  base: 'light',
  brandTitle: 'My Design System',
  brandUrl: 'https://example.com',
  brandImage: 'logo.png',
  brandTarget: '_self',
});
```
Import it in `manager.ts` and set `theme`. A theme replaces rather than merges, so set a complete theme. Many theme variables are optional but `base` is not. Built-in themes are light, dark and a "normal" theme matching the preferred color scheme (the default). Docs pages are themed independently via `parameters.docs.theme` in the preview file (default light).

For finer CSS control, the docs offer class-name escape hatches (`.storybook/manager-head.html` for the UI, `.storybook/preview-head.html` for Docs), flagged as use at your own risk because Storybook's inner HTML can change between releases.

## Checked

Method: 2026-11-08 compared against the Storybook docs source mdx for Theming and Features and behavior (configure/user-interface), plus their code snippets. setConfig options, create() fields and docs theming match. Dropped an invented "Verify" step. Note that `fullscreen: { hidden: true }` is an extrapolation of the page's `{ hidden: false }` toolbar example.
