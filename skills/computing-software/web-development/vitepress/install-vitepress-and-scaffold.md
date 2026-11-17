---
id: computing-software.web-development.vitepress.install-vitepress-and-scaffold
name: install-vitepress-and-scaffold
category: computing-software
field: web-development
product: vitepress
tags: [vitepress, installation, vitepress-init, setup-wizard, prerequisites, esm-only, npm]
level: intro
status: docs-checked
description: "Install VitePress (Node 22+), run the init setup wizard, and know the generated docs layout, scripts, and the ESM-only requirement."
sources:
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/guide/getting-started.md
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/snippets/init.ansi
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Prerequisites.** Node.js 22 or higher, a terminal, and an editor with Markdown support (VS Code with the official Vue extension is recommended). You can try it online at the StackBlitz link vitepress.new.

**Install** into a standalone folder or an existing project (the docs use the `@next` tag in this version):

```sh
npm add -D vitepress@next        # pnpm add -D / bun add -D / deno add -D likewise
yarn add -D vitepress@next vue   # yarn needs vue explicitly
```

VitePress is an ESM-only package. Never `require()` it: make sure the nearest `package.json` has `"type": "module"`, or rename config files to `.mjs`/`.mts` (for example `.vitepress/config.mts`). Inside async CommonJS code use `await import('vitepress')`.

**Setup wizard.**

```sh
npx vitepress init      # pnpm vitepress init / yarn vitepress init / bun vitepress init
```

It asks: where to initialize the config (for example `./docs`), where to look for Markdown files, the site title and description, the theme (the guide's example answer is Default Theme), whether to use TypeScript for config and theme files, whether to add npm scripts to package.json, and the script prefix (for example `docs`, producing `docs:dev`). If you plan to customize with Vue components or APIs, also install `vue` as an explicit dependency.

**Where to scaffold.** For a standalone site use `./`. If VitePress lives alongside other source, scaffold into a subfolder such as `./docs` so it is separated from the rest of the project.

Generated shape when scaffolded in `./docs`:

```
docs/.vitepress/config.js
docs/api-examples.md
docs/markdown-examples.md
docs/index.md
package.json
```

Verify: `npm run docs:dev` serves the site at http://localhost:5173.

## Checked

Read the Getting Started guide in full and the init wizard transcript it embeds. Confirmed Node.js 22 or higher, the install commands with `@next`, the ESM-only note, the wizard questions, the `./docs` file structure, the generated npm scripts and the dev server address. Reworded the theme question to what the transcript shows.

Method: docs-only read of cited pages, 2026-11-08
