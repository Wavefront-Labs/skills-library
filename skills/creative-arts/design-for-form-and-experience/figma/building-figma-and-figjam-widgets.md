---
id: creative-arts.design-for-form-and-experience.figma.building-figma-and-figjam-widgets
name: building-figma-and-figjam-widgets
category: creative-arts
field: design-for-form-and-experience
product: figma
tags: [figma-widgets, widgets, widget-api, usesyncedstate, figjam-widgets, multiplayer-widgets, widget-development, figma]
level: practitioner
status: docs-checked
description: "Build Figma and FigJam widgets: what widgets are, desktop app setup, starter widget, TypeScript and JSX build, tsconfig, typings and the documentAccess manifest field."
sources:
  - "https://developers.figma.com/docs/widgets/"
  - "https://developers.figma.com/docs/widgets/setup-guide/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Figma and FigJam widgets

**What they are:** interactive objects in design files and FigJam boards that everyone can see and use, unlike plugins which run for one person. Typical uses: live polls and voting counters, tables and visualisations from imported data, timelines and calendars, multiplayer games.

## How they are built
- The Widget API is based on TypeScript and JSX; a widget is a function that renders components inside a widget object, and properties customise the look. The API's "components" are canvas layers (frames, text, shapes), not Figma components and instances.
- Interaction options: a property menu, a custom interface, or click event handlers.
- Widgets can use the Plugin API, for example to fetch outside data, open an iframe for more UI, or edit other objects.

## Setup (Setup Guide)
1. Install Visual Studio Code and Node.js with npm; widget development and testing needs the Figma desktop app, because Figma reads your code from a local file.
2. In the desktop app: Menu > Widgets > Development > New widget..., name it, choose "Simple widget" and save it on disk. `npm init @figma/widget` is a one-command alternative.
3. Open the widget folder in VS Code and run `npm install`; this installs TypeScript and both widget and plugin typings. Optionally install Figma's typescript-eslint rules (the `eslint-plugin-figma-plugins` repository).
4. Run the build task "npm: watch": it compiles `widget-src/code.tsx` into `dist/code.js` and recompiles on change. Edit the `.tsx` file, never the generated `code.js`.
5. Insert the widget from Menu > Widgets > Development > your widget name. The starter is a click counter.

## Building from scratch
Use `npm install --save-dev @figma/widget-typings @figma/plugin-typings`, and in `tsconfig.json` set `jsx` to `react`, `jsxFactory` to `figma.widget.h`, `jsxFragmentFactory` to `figma.widget.Fragment`, `target` to `es6`, `strict` to true, and `typeRoots` to the `@types` and `@figma` folders under `node_modules`.

## Performance
Without the manifest field `"documentAccess": "dynamic-page"` the whole document loads when a widget runs; in large files this can delay first run by 20 to 30 seconds. Add the field and load only the pages you need.

## Verify
- [ ] Builds with the watch task and appears in the Development menu.
- [ ] Manifest declares `documentAccess` if it touches other pages.
- [ ] Tested with more than one person in the file.

## Checked
2026-11-01. Confirmed on the Widget API Introduction and Setup Guide: widget definition and uses, TypeScript and JSX, desktop-app requirement, creation menu path, starter widget, `npm init @figma/widget`, watch build and file locations, typings and tsconfig settings, and the `documentAccess` note. Removed as unconfirmed (the hook and manifest pages returned 404): the code sample, hook names (synced state, property menu, effects), manifest field values, esbuild, publishing and review steps, and the practices paragraph.
Method: documentation only; no commands were run.
