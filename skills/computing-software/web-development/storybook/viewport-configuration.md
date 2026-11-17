---
id: computing-software.web-development.storybook.viewport-configuration
name: viewport-configuration
category: computing-software
field: web-development
product: storybook
tags: [viewport, responsive, initial-viewports, minimal-viewports, viewport-globals]
level: practitioner
status: docs-checked
description: "Define available viewports, set a default viewport and lock a story to a device size."
sources:
  - https://storybook.js.org/docs/essentials/viewport
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Viewport

Goal: test components at device sizes.

Configure in the preview file:

```ts
import { INITIAL_VIEWPORTS } from 'storybook/viewport';

export default definePreview({
  parameters: { viewport: { options: INITIAL_VIEWPORTS } },
  initialGlobals: { viewport: { value: 'ipad', isRotated: false } },
});
```

- Default set is `MINIMAL_VIEWPORTS` (`mobile1` 320x568, `mobile2` 414x896, `tablet` 834x1112, `desktop` 1280x1024); `INITIAL_VIEWPORTS` is a detailed device list including `iphone14` (390x844), `galaxys9` (360x740), `ipad` (768x1024), `ipad12p` (1024x1366).
- Each `options` entry is keyed by id with `name`, `styles: { height, width }` and `type` (`desktop`, `mobile`, `tablet` or `other`). `width` and `height` must include the unit, e.g. `'320px'`. The docs show adding two Kindle devices to the minimal set.
- Parameters apply at project, component and story level. `parameters.viewport.disable: true` turns the module off and can be re-enabled at a more specific level.
- `globals.viewport` has `value` (must match an option key) and `isRotated` (true rotates 90 degrees).

Lock a story to a size with `globals`; the toolbar can no longer change it:

```ts
export const OnPhone = meta.story({
  globals: { viewport: { value: 'mobile1', isRotated: false } },
});
```

Shortcuts: next viewport Alt+V, previous Alt+Shift+V, reset Alt+Ctrl+V.

## Checked

Method: 2026-11-08 read docs/essentials/viewport.mdx and the viewport snippets from the Storybook repo; fixed the default set (adds `desktop`), option fields and units, and the disable parameter; removed an unsupported Verify step. Code samples match the snippets.
