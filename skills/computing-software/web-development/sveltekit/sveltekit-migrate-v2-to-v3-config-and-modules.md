---
id: computing-software.web-development.sveltekit.sveltekit-migrate-v2-to-v3-config-and-modules
name: sveltekit-migrate-v2-to-v3-config-and-modules
category: computing-software
field: web-development
product: sveltekit
tags: [sveltekit, migrate-v3, migration, vite-config, app-navigation, app-paths, lib-alias]
level: practitioner
status: docs-checked
description: "Upgrade SvelteKit 2 to 3: move svelte.config.js into the Vite plugin, switch $lib to #lib, and replace changed $app/* modules and their APIs."
sources:
  - https://github.com/sveltejs/kit/blob/main/documentation/docs/60-appendix/35-migrating-to-sveltekit-3.md
  - https://github.com/sveltejs/kit/blob/main/documentation/docs/98-reference/26-$lib.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: first half of a v2 to v3 upgrade, covering dependencies, config and the `$app/*` module changes. Runtime, security and adapter changes are in sveltekit-migrate-v3-runtime-security-adapters.

Start with `npx sv migrate sveltekit-3` and upgrade to the newest 2.x first.

## Minimum versions
Node v22.17, TypeScript v6, Svelte v5.57.1, Vite v8.0.12, `@sveltejs/vite-plugin-svelte` v7.

## Configuration
- `svelte.config.js` is unsupported: pass options (formerly `config.kit.*`) to the `sveltekit` plugin in `vite.config.js`, next to `compilerOptions`:
```js
sveltekit({
	compilerOptions: { experimental: { async: true }},
	adapter: adapter()
})
```
- Remove: `files.lib`, `experimental.handleRenderingErrors`, `experimental.instrumentation`, `vitePlugin` (pass e.g. `inspector` directly), `preloadStrategy`. `experimental.tracing` becomes top-level `tracing`; `prerender.origin` becomes `paths.origin`; `csrf.checkOrigin` becomes `csrf.trustedOrigins`.
- New: `output.linkHeaderPreload` (by default `<link>` elements are used, not `Link` headers). `version.pollInterval` now defaults to one hour.

## $lib becomes #lib
SvelteKit no longer generates `$lib`. Declare the alias in `package.json` (Node subpath imports; Vite and TypeScript resolve them natively):
```json
{ "imports": { "#lib": "./src/lib/index.js", "#lib/*": "./src/lib/*" } }
```
Then `import { foo } from '#lib/foo.js'`; module extensions are now required. The `sv` CLI adds this entry when scaffolding a new project.

## $app modules
- `$app/environment` is renamed `$app/env` (usable in service workers). `$service-worker` is removed: `version` now comes from `$app/env`; `assets`, `immutable`, `prerendered` from `$app/manifest`; `resolved` from `$app/paths`.
- `$app/stores` is removed: use `$app/state` (`page`, no `$`). `page.url` is readonly; copy with `new URL(page.url.href)` to mutate. `updated.current` now flips automatically (navigation that fetches server data, remote calls, window focus, hourly poll).
- `$app/paths`: `base`, `assets`, `resolveRoute` removed. Use `resolve('/blog/[slug]', { slug })` and `asset('foo.png')`. Types `Pathname`/`Asset` become `Path`/`AssetPath` with no leading `/`; only route IDs start with `/`.
- `$app/navigation`: `pushState('/foo', state)` becomes `goto('/foo', { shallow: true, state })` (add `replace: true` for replaceState; `persistState: true` reapplies `page.state` after reload). Shallow routing now fires navigation hooks; filter on `shallow`. `invalidateAll` becomes `refreshAll` (also as the `goto` option). `keepFocus: true` plus `noScroll: true` become `reset: false`; `replaceState` becomes `replace`. `goto` rejects for URLs that match no route. `delta` exists only for `popstate`. `preloadData` can return `{ type: 'error', status, error }`; add that branch.
- `$app/forms`: a `use:enhance` form whose `action` is on another page now navigates there.
- New `$app/manifest` and `$app/service-worker`. The `$env/...` modules are deprecated for `$app/env/private` and `$app/env/public`.

## tsconfig
Extend `$app/tsconfig` (not `./.svelte-kit/tsconfig.json`) and supply `include`/`exclude` yourself; see sveltekit-typescript-tsconfig-and-types.

## Checked

2026-11-07. Read in full from the sveltejs/kit docs source (including inline snippets; the pages have no external include files): `60-appendix/35-migrating-to-sveltekit-3.md`, `98-reference/26-$lib.md`. Every remaining claim, name, default and option was compared line by line with that text. Removed or reworded: nothing; every claim matched the pages.

Method: documentation only; no commands were run.
