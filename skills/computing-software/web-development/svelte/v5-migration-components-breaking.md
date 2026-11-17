---
id: computing-software.web-development.svelte.v5-migration-components-breaking
name: v5-migration-components-breaking
category: computing-software
field: web-development
product: svelte
tags: [mount-hydrate-migration, components-not-classes, runes-mode-breaking-changes, whitespace-handling, scoped-css-where]
level: advanced
status: docs-checked
description: "Svelte 5 breaking changes: components are functions (mount, unmount, render), bind:this, bindable props, class reactivity, whitespace, CSS :where, hydration and more."
sources:
  - https://raw.githubusercontent.com/sveltejs/svelte/main/documentation/docs/07-misc/07-v5-migration-guide.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Components are functions, not classes:
- `new App({ target })` becomes `mount(App, { target })` from `svelte`; `hydrate` has the same API for server-rendered HTML. Neither is synchronous; call `flushSync` if you need `onMount` to have run.
- `$on` becomes the `events` option (discouraged; use callbacks). `$set` becomes a `$state` props object you mutate. `$destroy` becomes `unmount(app)`.
- Stop-gaps: `createClassComponent` / `asClassComponent` from `svelte/legacy`, or the `compatibility.componentApi: 4` compiler option.
- Server: `App.render(...)` becomes `render(App, { props })` from `svelte/server`. CSS is no longer returned unless the `css` option is `'injected'`.
- Types: `Component` replaces `SvelteComponent`; `ComponentEvents` and `ComponentType` are deprecated. `bind:this` returns only the instance exports.
- `<svelte:component>` is unnecessary; `<foo.bar>` is a component.

Runes-mode breaks:
- No `bind:` to component exports; use `bind:this`.
- Props are bindable only with `$bindable()`.
- `accessors` and `immutable` options are ignored.
- Classes are not auto-reactive: declare `$state` fields.
- `ontouchstart`/`ontouchmove` are passive.
- Concatenated attribute values need quotes: `prop="this{is}valid"`.
- Stricter HTML structure (no auto-inserted `tbody`).

Other changes:
- `children` is a reserved prop name.
- Whitespace collapses to one space and is trimmed at tag edges.
- `null` and `undefined` render as empty string.
- Scoped CSS uses `:where(.svelte-xyz123)`; `:is`, `:has`, `:where` selectors are now scoped.
- `onevent` attributes no longer take strings.
- Hydration relies on comments in server output.
- `--style-props` wrap in `svelte-css-wrapper`.
- Namespaces limited to `html`, `mathml`, `svg`.

## Checked

2026-11-08: Read the Svelte 5 migration guide (components are no longer classes, mount/hydrate/unmount/flushSync, server render and css option, Component typing, bind:this, runes-mode breaking changes, whitespace, :where scoping, namespaces, hydration comments, svelte-css-wrapper). Every claim was located in the page; nothing removed.

Method: docs-only read of cited pages, 2026-11-08
