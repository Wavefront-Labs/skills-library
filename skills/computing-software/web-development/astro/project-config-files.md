---
id: computing-software.web-development.astro.project-config-files
name: project-config-files
category: computing-software
field: web-development
product: astro
tags: [astro-config, tsconfig, config-file-formats]
level: intro
status: docs-checked
description: "Choose the Astro configuration file format (.js, .mjs, .ts) and know why tsconfig.json is recommended."
sources:
  - https://raw.githubusercontent.com/withastro/docs/main/src/content/docs/en/basics/project-structure.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`astro.config.mjs` is generated in every starter template. It holds configuration for integrations, build options, server options and more.

Astro supports `astro.config.js`, `astro.config.mjs` and `astro.config.ts`. The docs recommend `.mjs` in most cases, or `.ts` if you want to write TypeScript in your config file. TypeScript config loading is handled using `tsm` and respects your project's `tsconfig` options.

`tsconfig.json` is also generated in every starter template. Some features, like npm package imports, are not fully supported in the editor without a `tsconfig.json`.

Complete details are in the configuration reference.

## Checked

2026-11-04. Confirmed against the Astro project structure page: config file formats and recommendation, tsm loading, tsconfig.json note. Nothing removed.

Method: documentation only; no commands were run.
