---
id: computing-software.web-development.sveltekit.sveltekit-migrate-v1-to-v2
name: sveltekit-migrate-v1-to-v2
category: computing-software
field: web-development
product: sveltekit
tags: [sveltekit, migrate-v2, migration, breaking-changes, cookies, redirect, upgrade]
level: practitioner
status: docs-checked
description: "Upgrade a SvelteKit 1 app to SvelteKit 2: the codemod, the required code changes (error/redirect, cookie path, load promises, goto, paths) and minimum versions."
sources:
  - https://github.com/sveltejs/kit/blob/main/documentation/docs/60-appendix/30-migrating-to-sveltekit-2.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: move an app from SvelteKit 1 to 2 with the fewest surprises.

## Prepare
- Upgrade to the latest 1.x first (targeted deprecation warnings) and to Svelte 4 first (SvelteKit 2 requires it).
- Run `npx sv migrate sveltekit-2` to automate many of the changes below.
- Requirements: Node 18.13+, `svelte@4`, `vite@5`, `typescript@5`, `@sveltejs/vite-plugin-svelte@3` (now a peerDependency), and adapter majors: cloudflare 3, cloudflare-workers 2, netlify 3, node 2, static 3, vercel 4.

## Code changes
- **error/redirect**: do not `throw` them any more; just call `error(500, 'something went wrong')`. If you call them inside a `try`, tell them apart from real errors with `isHttpError` / `isRedirect` from `@sveltejs/kit`.
- **Cookies**: `cookies.set`, `cookies.delete` and `cookies.serialize` need an explicit `path`, usually `{ path: '/' }` (`''` = current path, `'.'` = current directory).
- **Load promises**: top-level promises returned from `load` are no longer auto-awaited. Make the function `async`, `await` the data, and use `Promise.all([...])` for several fetches to avoid waterfalls.
- **goto**: no external URLs (use `window.location.href = url`); the `state` option feeds `$page.state` and must match `App.PageState`.
- **Paths**: `paths.relative` now defaults to `true` and applies consistently to `%sveltekit.assets%`, `base` and `assets`.
- **preloadCode / preloadData**: both paths must be prefixed with `base`; `preloadCode` takes a single argument.
- **resolvePath removed**: use `resolveRoute('/blog/[slug]', { slug })` from `$app/paths` (it already includes `base`; do not prepend it again).
- **handleError** now receives `status` and `message`; for code-thrown errors these are `500` and `Internal Error`, and `message` is safe to show users.
- **Env**: `$env/dynamic/*` cannot be read while prerendering; use the `static` modules. On prerendered pages the client fetches fresh dynamic public values from `/_app/env.js` by default.
- **use:enhance** callbacks: `form`/`data` are gone, use `formElement`/`formData`.
- Forms with `<input type="file">` need `enctype="multipart/form-data"`, otherwise SvelteKit throws during an `use:enhance` submit.
- `dangerZone.trackServerFetches` is removed (server fetches are not trackable).
- `getRequest` (`@sveltejs/kit/node`) no longer throws for an oversize `Content-Length`; the error comes when the body is read.
- `vitePreprocess` is no longer exported from `@sveltejs/kit/vite`; import it from `@sveltejs/vite-plugin-svelte`.

## TypeScript
The generated tsconfig uses `"moduleResolution": "bundler"` and `verbatimModuleSyntax`; delete `importsNotUsedAsValues` and `preserveValueImports`. Using `paths` or `baseUrl` in your tsconfig now warns: configure the plugin's `alias` option instead.

## $app/stores (2.12+)
Deprecated in favour of `$app/state`: change the import and drop the `$` prefix (`page.data`, not `$page.data`). Auto-migrate with `npx sv migrate app-state`.

## Checked

2026-11-07. Read in full from the sveltejs/kit docs source (including inline snippets; the pages have no external include files): `60-appendix/30-migrating-to-sveltekit-2.md`. Every remaining claim, name, default and option was compared line by line with that text. Removed or reworded: nothing; every claim matched the pages.

Method: documentation only; no commands were run.
