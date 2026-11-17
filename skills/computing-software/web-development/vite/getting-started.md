---
id: computing-software.web-development.vite.getting-started
name: getting-started
category: computing-software
field: web-development
product: vite
tags: [create-vite, scaffold-project, node-version, manual-install]
level: intro
status: docs-checked
description: "Scaffold a Vite project with create-vite, install vite manually, know the Node.js requirement, and run the default dev, build and preview scripts."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/index.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Vite has two parts: a dev server over native ES modules (with HMR) and a build command that bundles with Rolldown.

Scaffold:

```bash
npm create vite@latest
npm create vite@latest my-vue-app -- --template vue   # npm 7+ needs the extra --
```

Use `.` as the name to scaffold in the current directory; `--no-interactive` skips prompts. Templates: `vanilla`, `vue`, `react`, `react-compiler`, `preact`, `lit`, `svelte`, `solid`, `qwik`, each with a `-ts` variant.

Manual install: `npm install -D vite`, create an `index.html`, run `npx vite`; it is served on `http://localhost:5173`.

Default scripts:

```json
{ "scripts": { "dev": "vite", "build": "vite build", "preview": "vite preview" } }
```

Requirements and notes:
- Node.js 20.19+ or 22.12+; some templates need newer.
- `vite dev` and `vite serve` are aliases of `vite`.
- A different root: `vite serve some/sub/dir`. The config file is resolved inside the project root, so move it with the root.
- `index.html` sits at the project root because it is the entry point and part of the module graph.

## Checked

2026-11-07. Confirmed against guide/index.md, read in full: Vite as dev server plus Rolldown build, the `npm create vite@latest` forms and the npm 7+ double dash, `.` as project name, `--no-interactive`, the template list with `-ts` variants (including `react-compiler-ts`), manual install and `npx vite` on `http://localhost:5173`, the Node.js 20.19+ or 22.12+ requirement, default scripts and the `vite dev`/`vite serve` aliases, `vite serve some/sub/dir` with the config file note, and why `index.html` sits at the root. Nothing removed.

Method: documentation only; no commands were run.
