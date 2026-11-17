---
id: computing-software.web-development.vite.framework-plugins
name: framework-plugins
category: computing-software
field: web-development
product: vite
tags: [framework-plugins, plugin-vue, plugin-react, hmr-integrations]
level: intro
status: docs-checked
description: "Which framework plugins to use with Vite: official Vue, Vue JSX, React, React SWC and RSC plugins, and the first-party HMR integrations."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/features.md
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/index.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
All modern frameworks maintain Vite integrations. Most plugins are maintained by each framework team, except the official Vue and React plugins kept in the vite org:

- Vue: `@vitejs/plugin-vue`
- Vue JSX: `@vitejs/plugin-vue-jsx`
- React: `@vitejs/plugin-react`
- React using SWC: `@vitejs/plugin-react-swc`
- React Server Components: `@vitejs/plugin-rsc`

HMR integrations: first-party for Vue Single File Components and React Fast Refresh; Preact via `@prefresh/vite`. You do not set these up manually: templates from `create-vite` come preconfigured.

Legacy browser support is the separate `@vitejs/plugin-legacy`.

## Checked

2026-11-07. Confirmed against the "Frameworks" and "Hot Module Replacement" sections of guide/features.md (page read in full): the five plugin packages, framework-team maintenance, first-party Vue and React integrations plus `@prefresh/vite` for Preact, and `create-vite` preconfiguration. The `@vitejs/plugin-legacy` line is confirmed by the Browser Support section of guide/index.md (read in full), which was added to `sources`.

Method: documentation only; no commands were run.
