---
id: computing-software.web-development.storybook.writing-addons
name: writing-addons
category: computing-software
field: web-development
product: storybook
tags: [addon-development, addon-kit, toolbar-addon, panel-addon, manager-api]
level: advanced
status: docs-checked
description: "Build a UI addon with the Addon Kit and register panels and toolbar tools via the manager API."
sources:
  - https://storybook.js.org/docs/addons/writing-addons
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Writing a Storybook addon

Goal: create a toolbar addon (panels and tabs follow the same pattern).

Two categories: UI-based addons (toolbars, panels) and presets. UI addons with a UI must use the same React version as Storybook; otherwise build and publish them as standalone packages with the Addon Kit. Start from the Addon Kit template repository (Use this template, clone, install; you are prompted with configuration questions). It uses TypeScript (run `eject-ts` to convert to JavaScript) and bundles with tsup (powered by esbuild). Presets run in Node; the manager and preview provide certain packages globally, so addons need not bundle them.

Code lives in `src/Tool.tsx`, `src/Panel.tsx` or `src/Tab.tsx`. Register the tool in the manager entry (`src/manager.ts`):

```ts
import { addons, types } from 'storybook/manager-api';
import { ADDON_ID, TOOL_ID } from './constants';
import { Tool } from './Tool';

addons.register(ADDON_ID, () => {
  addons.add(TOOL_ID, {
    type: types.TOOL,
    title: 'My addon',
    match: ({ viewMode }) => viewMode === 'story',
    render: Tool,
  });
});
```

Notes:
- `match` controls the view mode where the toolbar addon shows: `viewMode === 'story'` for the canvas, `viewMode === 'docs'` for component documentation.
- In `Tool.tsx` use `useGlobals` and `useStorybookApi` from `storybook/manager-api`, `Button` from `storybook/internal/components`, and icons from `@storybook/icons`. `api.setAddonShortcut` registers a keyboard shortcut.
- Applying styles is a side effect: use a decorator and globals, with `useEffect`, `useMemo` and `useGlobals` from `storybook/preview-api` in the preview-side file (`src/withGlobals.ts`). Choose a different DOM selector for story and docs mode, since docs mode renders multiple previews on one page.
- Publishing: the package needs a `dist` folder and `package.json` with `exports` (including `./manager` and `./preview`), `bundler` entries, a `storybook` property (`displayName`, `icon`, `unsupportedFrameworks`) and the `storybook-addon` keyword for the integration catalog. The Addon Kit uses Auto for releases (`GH_TOKEN` and `NPM_TOKEN`, `npx auto create-labels`) and ships a GitHub Actions workflow that needs an `NPM_TOKEN` secret.

Verify: run the `start` script; the addon appears in the toolbar.

## Checked
Read the whole writing-addons page (storybookjs/storybook docs/addons/writing-addons.mdx) and the page's manager-initial-state snippet and use-global import line on 2026-11-08. Confirmed addon categories, React version note, Addon Kit, tsup/esbuild, `eject-ts`, file layout, manager registration, `match`, the imports, packaging metadata and Auto release flow. Removed: the `types.PANEL` example, the claim of required fields `type`, `title`, `render` and `render` receiving `active`, the `addons.getChannel()` note and the "added to main.ts" verification, none of which is on the page.
Method: docs-only read of cited pages, 2026-11-08
