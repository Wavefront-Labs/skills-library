---
id: computing-software.web-development.svelte.v4-migration
name: v4-migration
category: computing-software
field: web-development
product: svelte
tags: [svelte-4-migration, browser-condition-bundlers, transitions-local-default, preprocessor-order, custom-element-option]
level: practitioner
status: docs-checked
description: "Svelte 3 to 4 migration: minimum versions, browser bundler condition, CJS removal, stricter types, customElement option, local transitions and preprocessor order."
sources:
  - https://raw.githubusercontent.com/sveltejs/svelte/main/documentation/docs/07-misc/06-v4-migration-guide.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Automate part of it with `npx svelte-migrate@latest svelte-4`. Library authors should update the `peerDependencies` range.

Minimums: Node 16, SvelteKit 1.20.4, `vite-plugin-svelte` 2.4.1, webpack 5 with `svelte-loader` 3.1.8, `rollup-plugin-svelte` 7.1.5, TypeScript 5.

Changes:
- Bundlers must set the `browser` condition, or `onMount` will not run. Rollup: `browser: true` in `@rollup/plugin-node-resolve`. Webpack: add `"browser"` to `conditionNames`.
- CommonJS output, `svelte/register` and the CJS runtime are removed.
- Stricter types: `createEventDispatcher` checks payload presence; `Action` defaults to `undefined` params, so write `Action<HTMLElement, string>`; `onMount` errors if you return a function asynchronously.
- `<svelte:options tag="my-component" />` becomes `customElement="my-component"`.
- `SvelteComponentTyped` is deprecated; use `SvelteComponent`, and `typeof SvelteComponent<any>` for instance-type variables.
- Transitions are local by default: they do not play when only a block above the direct parent is created or destroyed. Add `|global` to restore.
- Default slot bindings are no longer exposed to named slots, and vice versa.
- Preprocessors run in order, with markup, script, style within each group. Put `mdsvex` before `vitePreprocess()`. Each needs a name.
- Replace `eslint-plugin-svelte3` with `eslint-plugin-svelte`.
- Outroing elements get `inert`; the runtime uses `classList.toggle(name, boolean)` and `CustomEvent`; `derived` throws on falsy non-store arguments; `svelte.JSX` typings move to `svelteHTML` and `svelte/elements`.

## Checked

Read the full Svelte 4 migration guide source page. Confirmed the svelte-migrate command, every minimum version (Node 16, SvelteKit 1.20.4, vite-plugin-svelte 2.4.1, svelte-loader 3.1.8, rollup-plugin-svelte 7.1.5, TypeScript 5), the browser condition for Rollup and webpack, CJS removal, stricter types, customElement option, SvelteComponentTyped, local transitions with |global, slot bindings, preprocessor order and names, eslint-plugin-svelte, and the other breaking changes. No claims removed.

Method: docs-only read of cited pages, 2026-11-08
