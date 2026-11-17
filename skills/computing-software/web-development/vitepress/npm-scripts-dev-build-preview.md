---
id: computing-software.web-development.vitepress.npm-scripts-dev-build-preview
name: npm-scripts-dev-build-preview
category: computing-software
field: web-development
product: vitepress
tags: [vitepress, docs-dev, docs-build, docs-preview, npm-scripts, dev-server, localhost-5173, localhost-4173]
level: intro
status: docs-checked
description: "Wire docs:dev, docs:build and docs:preview scripts and understand the dev server (port 5173) versus preview server (port 4173)."
sources:
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/guide/getting-started.md
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/guide/deploy.md
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/reference/cli.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The init wizard (if allowed) adds these scripts:

```json
{
  "scripts": {
    "docs:dev": "vitepress dev docs",
    "docs:build": "vitepress build docs",
    "docs:preview": "vitepress preview docs"
  }
}
```

- `docs:dev` starts the Vite dev server with instant hot updates at `http://localhost:5173`. You can run `npx vitepress dev docs` directly (`pnpm vitepress`, `yarn vitepress`, `bun vitepress` equivalents).
- `docs:build` produces the static production site, by default into `docs/.vitepress/dist`.
- `docs:preview` boots a local static web server for the built output at `http://localhost:4173`. Use it to check the real production output (hashed assets, base path, clean URLs) before pushing. Change the port with `vitepress preview docs --port 8080`.

All deployment guides in the docs assume the site sits in `docs`, the default output directory is used, and these scripts exist.

Habit: check deployment-affecting settings (`base`, `cleanUrls`, `assetsBase`) with build then preview, not the dev server alone. The docs say `assetsBase` affects production builds only and that relative-base behaviour applies to the production build.

If you embed the site in a larger repository, name the scripts so they do not clash with the app's own `dev`/`build`.

Verify: after `npm run docs:build && npm run docs:preview`, the preview URL shows the same site and links work.

## Checked

2026-11-08. Read the VitePress docs source pages getting-started, deploy, cli and site-config. Confirmed the three scripts, port 5173 for dev, port 4173 for preview with the --port 8080 example, the default dist output, the deploy guide's shared assumptions, hashed asset names, and the direct invocation forms. Reworded the habit line to what the pages state.

Method: docs-only read of cited pages, 2026-11-08
