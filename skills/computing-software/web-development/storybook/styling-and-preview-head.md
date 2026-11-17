---
id: computing-software.web-development.storybook.styling-and-preview-head
name: styling-and-preview-head
category: computing-software
field: web-development
product: storybook
tags: [css, global-styles, preview-head, webfonts, css-modules]
level: practitioner
status: docs-checked
description: "Load global CSS into the preview, add static CSS and webfonts via preview-head.html, and use CSS modules, PostCSS and Sass per builder."
sources:
  - https://storybook.js.org/docs/configure/styling-and-css
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Styling and preview head/body

Goal: make stories look like the app.

Global CSS: import it in `.storybook/preview.ts`:

```ts
import '../src/index.css';
```
Storybook injects styles into the preview iframe, not the manager UI. Importing in the preview file is the recommended route and gets HMR. CSS imported by components works too; Sass or PostCSS tooling may need extra configuration.

Static CSS: include it from `.storybook/preview-head.html`. These files are not hot reloaded; restart the server.

Builders:
- Vite: CSS modules, PostCSS and Sass/Less/Stylus work out of the box and use your `vite.config.js` customisations.
- Webpack: CSS modules, PostCSS and Sass/Less need extra configuration; the page recommends `@storybook/addon-styling-webpack` (or customise the webpack config yourself). `@storybook/nextjs` recreates your Next.js config so none is needed.
- CSS-in-JS usually works unchanged; for libraries needing a theme context, the page points to `withThemeFromJSXProvider` in `@storybook/addon-themes`.

Webfonts: add code to `preview-head.html` (the page prefers serving assets with Storybook via static dirs), or import fontsource CSS in the preview file.

Angular: add global styles to the `styles` array in `angular.json`, in both the `storybook` and `build-storybook` targets.

## Checked

Method: 2026-11-08 read docs/configure/styling-and-css.mdx from the Storybook repo. Removed unsupported claims (`preview-body.html` and `rem` font-size advice, programmatic head changes via presets, a "code that runs for every story" rule) and a Verify step; added HMR and Angular details from the page.
