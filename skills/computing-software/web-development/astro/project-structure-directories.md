---
id: computing-software.web-development.astro.project-structure-directories
name: project-structure-directories
category: computing-software
field: web-development
product: astro
tags: [project-structure, src-directory, public-directory, conventions]
level: intro
status: docs-checked
description: "Know the Astro project layout: required src/pages, conventional src folders, and how public/ differs from src/ in processing."
sources:
  - https://raw.githubusercontent.com/withastro/docs/main/src/content/docs/en/basics/project-structure.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Every Astro project root should include:

- `src/*` - project source code (components, pages, styles, images)
- `public/*` - non-code, unprocessed assets (fonts, icons)
- `package.json` - project manifest
- `astro.config.mjs` - Astro configuration (recommended)
- `tsconfig.json` - TypeScript configuration (recommended)

The only directory reserved by Astro is `src/pages/`, and it is required: without it your site has no pages or routes. Others are conventions: `src/components`, `src/layouts`, `src/styles`.

`src/` files are processed, optimized and bundled by Astro. Some (Astro components) are rendered to static HTML; CSS is sent to the browser but may be optimized or bundled.

`public/` files are copied into the build folder untouched. It suits files like `robots.txt` and `manifest.webmanifest`, and images or fonts needing no processing. CSS and JavaScript placed there are not bundled or optimized. As a rule, any CSS or JavaScript you write should live in `src/`.

`package.json`: the docs recommend putting all dependencies in `dependencies` to start, since Astro needs all of them at build time.

## Checked

2026-11-04. Confirmed against the Astro project structure page: root files, src/pages reserved and required, conventional folders, src versus public processing, dependencies advice. Nothing removed.

Method: documentation only; no commands were run.
