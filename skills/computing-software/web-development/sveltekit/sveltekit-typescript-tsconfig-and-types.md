---
id: computing-software.web-development.sveltekit.sveltekit-typescript-tsconfig-and-types
name: sveltekit-typescript-tsconfig-and-types
category: computing-software
field: web-development
product: sveltekit
tags: [sveltekit, tsconfig, typescript, generated-types, app-types, svelte-kit-sync, service-worker]
level: practitioner
status: docs-checked
description: "Set up tsconfig for SvelteKit and use the generated ./$types, PageProps, RouteParams and app.d.ts so route params and load data are typed."
sources:
  - https://github.com/sveltejs/kit/blob/main/documentation/docs/98-reference/20-$app-tsconfig.md
  - https://github.com/sveltejs/kit/blob/main/documentation/docs/98-reference/22-$app-types.md
  - https://github.com/sveltejs/kit/blob/main/documentation/docs/98-reference/54-types.md
  - https://github.com/sveltejs/kit/blob/main/documentation/docs/98-reference/52-cli.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: get type-safe `params`, `data` and route IDs without hand-writing types.

## tsconfig
Extend the module `$app/tsconfig` and give `include`/`exclude` yourself:
```json
{
	"extends": "$app/tsconfig",
	"include": ["src", "test"],
	"exclude": ["src/service-worker"]
}
```
Overriding these may break things (SvelteKit warns):
- `paths`: derived from the (deprecated) `alias` option plus `package.json` subpath imports; prefer subpath imports.
- `types`: must include `"$app/types"` so generated declarations (e.g. environment variables) are visible.
- `isolatedModules`: must be `true` (Vite compiles modules one at a time).
- `verbatimModuleSyntax`: must be `true`, so type imports in `.svelte` files are safe.

A service worker needs its own TypeScript project: exclude it (as above) and add `src/service-worker/tsconfig.json` extending `$app/tsconfig/service-worker`.

## Generated types
`svelte-kit sync` writes `tsconfig.json` and all generated types (imported as `./$types` in routing files). It is the `prepare` script in new projects and runs with the npm lifecycle, so you rarely run it by hand. Vite itself is driven with `vite dev`, `vite build`, `vite preview`.

For each route SvelteKit generates a `$types.d.ts` (under `.svelte-kit/types/...`) next to your files via `rootDirs`, e.g. for `[foo]/[bar]/[baz]`: `RouteParams` with those three strings, `RequestHandler`, `PageLoad`:
```js
/** @type {import('./$types').PageLoad} */
export async function load({ params, fetch }) {
	// ...
}
```
Load return types are `PageData` / `LayoutData`; the union of action returns is `ActionData`. From 2.16.0, `PageProps` (`data`, plus `form` when actions exist) and `LayoutProps` (`data` and `children: Snippet`):
```svelte
<script>
	/** @type {import('./$types').PageProps} */
	let { data, form } = $props();
</script>
```
Before 2.16.0 type the props as `{ data: PageData, form: ActionData }`; in Svelte 4 use `export let data` / `export let form` with the same types.

## $app/types (since 2.26)
`import type { RouteId, PageRouteId, EndpointRouteId, RouteParams, LayoutParams } from '$app/types'`.
- `RouteId` = `PageRouteId` | `EndpointRouteId` (used for `page.route.id` and `event.route.id`); one route can be in both.
- `RouteParams<'/blog/[slug]'>` gives `{ slug: string }`; `LayoutParams` also includes optional params of child routes.
- `AssetPath` (files in `static`, relative to `base`), `Path` (valid paths relative to `base`), `ResolvedPathname` (prefixed with the base path; used for `page.url.pathname`).

## app.d.ts
Holds ambient types; it always contains the `App` namespace, whose types influence the shape of certain SvelteKit features.

## Checked

Checked 2026-11-07.

Method: documentation only; no commands were run.

Read 98-reference/20-$app-tsconfig.md, 22-$app-types.md, 54-types.md and 52-cli.md in full. One trim: the app.d.ts description of App namespace contents is now generic, because the page body there is only a generated placeholder.
