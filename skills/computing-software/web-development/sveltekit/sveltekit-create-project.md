---
id: computing-software.web-development.sveltekit.sveltekit-create-project
name: sveltekit-create-project
category: computing-software
field: web-development
product: sveltekit
tags: [sveltekit, create-project, sv-create, scaffold, dev-server, vscode]
level: intro
status: docs-checked
description: "Scaffold a new SvelteKit app with npx sv create, start the dev server, and set up an editor."
sources:
  - https://github.com/sveltejs/kit/blob/main/documentation/docs/10-getting-started/20-creating-a-project.md
  - https://github.com/sveltejs/kit/blob/main/documentation/docs/10-getting-started/10-introduction.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: get a running SvelteKit app and know where pages live.

## Steps
```sh
npx sv create my-app
cd my-app
npm run dev
```
- The first command scaffolds a project in `my-app` and asks whether to set up basic tooling such as TypeScript (options are described in the sv CLI docs).
- `npm run dev` starts the development server on localhost:5173. If you skipped installing dependencies during project creation, install them before running it.

## Core ideas
- Each page of the app is a Svelte component.
- You create pages by adding files under `src/routes`. They are server-rendered so the first visit is fast, then a client-side app takes over.

## Editor
Recommended: VS Code with the Svelte extension; other editors are supported too.

## Context (from the introduction)
- SvelteKit is the framework around Svelte: Svelte renders UI components, SvelteKit adds the router, build optimisations, offline support (service workers), link preloading, configurable rendering (SSR, CSR or prerendering), image optimisation and a Vite-based HMR dev experience.
- You do not need to know Svelte to follow the docs, but it helps.

Try editing the generated files to see how things fit together.

## Checked

2026-11-07. Read in full from the sveltejs/kit docs source (including inline snippets; the pages have no external include files): `10-getting-started/20-creating-a-project.md`, `10-getting-started/10-introduction.md`. Every remaining claim, name, default and option was compared line by line with that text. Removed or reworded: nothing; every claim matched the pages.

Method: documentation only; no commands were run.
