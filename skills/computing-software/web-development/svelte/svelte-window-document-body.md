---
id: computing-software.web-development.svelte.svelte-window-document-body
name: svelte-window-document-body
category: computing-software
field: web-development
product: svelte
tags: [svelte-window, svelte-document, svelte-body, global-event-listeners, scroll-binding]
level: practitioner
status: docs-checked
description: "svelte:window, svelte:document and svelte:body: top-level-only elements for global listeners and bindings (scrollY, activeElement) with automatic cleanup and SSR safety."
sources:
  - https://raw.githubusercontent.com/sveltejs/svelte/main/documentation/docs/05-special-elements/02-svelte-window.md
  - https://raw.githubusercontent.com/sveltejs/svelte/main/documentation/docs/05-special-elements/03-svelte-document.md
  - https://raw.githubusercontent.com/sveltejs/svelte/main/documentation/docs/05-special-elements/04-svelte-body.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
All three may only appear at the top level of a component, never inside a block or element.

`<svelte:window>` adds listeners to `window` without manual removal on destroy and without checking for `window` during server-side rendering.

```svelte
<svelte:window onkeydown={handleKeydown} />
<svelte:window bind:scrollY={y} />
```

Bindable properties: `innerWidth`, `innerHeight`, `outerWidth`, `outerHeight`, `scrollX`, `scrollY`, `online` (alias for `window.navigator.onLine`), `devicePixelRatio`. All are readonly except `scrollX` and `scrollY`. The page is not scrolled to the initial value (accessibility); only later changes to the bound variable scroll. To scroll on render call `scrollTo()` in an `$effect`.

`<svelte:document>` listens to `document` events that do not fire on `window`, such as `visibilitychange`, and accepts attachments:

```svelte
<svelte:document onvisibilitychange={handleVisibilityChange} {@attach someAttachment} />
```

Readonly bindings: `activeElement`, `fullscreenElement`, `pointerLockElement`, `visibilityState`.

`<svelte:body>` listens to `document.body` events such as `mouseenter` and `mouseleave` that do not fire on `window`, and accepts actions:

```svelte
<svelte:body onmouseenter={handleMouseenter} onmouseleave={handleMouseleave} use:someAction />
```

## Checked

2026-11-08: Read the svelte:window and svelte:document pages and the svelte:body page (top-level only, bindable and readonly properties, scroll binding note, attachments on document, actions on body). Every claim was located; nothing removed.

Method: docs-only read of cited pages, 2026-11-08
