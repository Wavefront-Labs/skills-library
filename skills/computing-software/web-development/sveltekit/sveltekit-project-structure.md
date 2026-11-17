---
id: computing-software.web-development.sveltekit.sveltekit-project-structure
name: sveltekit-project-structure
category: computing-software
field: web-development
product: sveltekit
tags: [sveltekit, project-structure, app-html, error-html, static, src-lib, vite-config]
level: intro
status: docs-checked
description: "Know what each file and folder in a SvelteKit project does: src/lib, src/routes, app.html placeholders, error.html, static, hooks, params.js."
sources:
  - https://github.com/sveltejs/kit/blob/main/documentation/docs/10-getting-started/30-project-structure.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: find or place things correctly in a SvelteKit project.

```tree
my-project/
├ src/
│ ├ lib/
│ ├ routes/
│ ├ service-worker/
│ │ ├ index.js
│ │ └ tsconfig.json
│ ├ app.html
│ ├ error.html
│ ├ hooks.client.js
│ ├ hooks.server.js
│ ├ instrumentation.server.js
│ └ params.js
├ static/
├ tests/
├ package.json
├ tsconfig.json
└ vite.config.js
```

## src
Everything except `src/routes` and `src/app.html` is optional.
- `lib`: library code (utilities and components), imported through the `#lib` alias or packaged with `svelte-package`. Directories named `server` at any depth mark code as server-only; SvelteKit blocks importing it in client code.
- `routes`: your routes; you may colocate components used by a single route.
- `service-worker`, `hooks.client.js`, `hooks.server.js`, `params.js` (param matchers), `instrumentation.server.js` (observability; needs adapter support, runs before your app code if supported).
- `app.html`, the page template, placeholders:
  - `%sveltekit.head%` link/script elements plus `<svelte:head>` content
  - `%sveltekit.body%` the rendered page markup; put it inside a `<div>` or other element, not directly in `<body>`, because browser extensions injecting elements can break hydration (dev warns)
  - `%sveltekit.assets%` `paths.assets` if set, else a relative path to `paths.base`
  - `%sveltekit.nonce%` CSP nonce
  - `%sveltekit.env.[NAME]%` replaced at render time with the public env var `[NAME]`; falls back to `''`
  - `%sveltekit.version%` app version
- `error.html`: last-resort error page; placeholders `%sveltekit.status%` and `%sveltekit.error.message%`.

## Other
- `static/`: assets served unchanged (e.g. `robots.txt`). Prefer `import`ing assets so Vite hashes names for caching.
- `package.json` must list `@sveltejs/kit`, `svelte` and `vite` in `devDependencies`; `"type": "module"` means legacy CommonJS needs `.cjs`.
- `vite.config.js`: a Vite project using the `@sveltejs/kit/vite` plugin.
- `tsconfig.json` extends a config SvelteKit generates.
- `.svelte-kit` (configurable as `outDir`) is generated; ignore it and delete freely, it regenerates on `dev` or `build`.
- Vitest unit tests go in `src` as `.test.js`; Playwright tests go in `tests/`.

## Checked

Checked 2026-11-07.

Method: documentation only; no commands were run.

Read 10-getting-started/30-project-structure.md in full: directory tree, placeholders, error.html, package.json and .svelte-kit. No claims trimmed.
