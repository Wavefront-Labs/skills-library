---
id: computing-software.software-engineering.wails.sveltekit-frontend
name: sveltekit-frontend
category: computing-software
field: software-engineering
product: wails
tags: [wails, go, sveltekit, svelte, frontend, adapter-static, spa]
level: practitioner
status: docs-checked
description: "Replace the Wails Svelte frontend with SvelteKit in SPA mode using adapter-static, then avoid runtime loss on full page navigations, server files and unhandled errors."
sources: [https://wails.io/docs/guides/sveltekit]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SvelteKit as a Wails frontend

Goal: run SvelteKit (prerendered SPA) inside a Wails v2 project.

## Setup

1. `wails init -n myapp -t svelte`, then delete the `frontend` folder.
2. In the project root: `npx sv create frontend` (no Wails-specific answers needed).
3. `wails.json`: add `"wailsjsdir": "./frontend/src/lib",` (where the Go and runtime bindings will appear); change the package manager entries if not using npm.
4. `main.go`: change `//go:embed all:frontend/dist` to `//go:embed all:frontend/build`. `.gitignore`: replace `frontend/dist` with `frontend/build`.
5. In `frontend`: `npm i`, `npm uninstall @sveltejs/adapter-auto`, `npm i -D @sveltejs/adapter-static`. In `svelte.config.js` import `@sveltejs/adapter-static` instead of `adapter-auto`.
6. Create `frontend/src/routes/+layout.ts` (or .js) containing `export const prerender = true` and `export const ssr = false`.
7. From the project root run `wails dev`; if it fails, recheck the steps.

The page also provides a bash script (`sveltekit-wails.sh <manager> <project> [brand]`) automating this; read it before running.

## Important notes

- Any server file (`+layout.server.ts`, `+page.server.ts`, `+server.ts`, or any file with "server" in its name) fails the build because all routes are prerendered.
- Full page navigations (`window.location.href = ...`, or the context menu reload in `wails dev`) unload the Wails runtime. Use `goto()` from `$app/navigation`, or, if unavoidable, add to `<head>` in `src/app.html`:
  ```html
  <meta name="wails-options" content="noautoinject" />
  <script src="/wails/ipc.js"></script>
  <script src="/wails/runtime.js"></script>
  ```
- Load initial data with `load()` in `+page.ts`; `invalidateAll()` re-runs it.
- Expected errors (thrown in `+page.ts` with `+error.svelte`) work. Unexpected errors make the app unusable; the only known recovery is reloading, via `src/hooks.client.ts`:
  ```ts
  import { WindowReloadApp } from '$lib/wailsjs/runtime/runtime'
  export async function handleError() { WindowReloadApp() }
  ```
- Forms: simplest is `<form method="POST" on:submit|preventDefault={handle}>`. With `use:enhance`, always call `cancel()` to prevent server-side behavior.

## Checked

2026-11-07. Read the whole SvelteKit guide (website/docs/guides/sveltekit.mdx): the minimal installation steps (wails init -t svelte, npx sv create frontend, wailsjsdir, go:embed and .gitignore dist-to-build, adapter-static swap, +layout.ts prerender/ssr lines, wails dev), the install-script section (only its usage line and read-before-running warning are referenced by the skill) and the Important Notes (server files, full-navigation runtime loss with goto and the noautoinject head snippet, load()/invalidateAll(), expected versus unexpected errors with the hooks.client.ts WindowReloadApp workaround, forms with preventDefault and use:enhance cancel()). The SvelteKit docs pages the guide links to were not opened. No claims were trimmed.

Method: documentation only; no commands were run.
