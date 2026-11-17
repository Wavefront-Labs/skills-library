---
id: computing-software.web-development.sveltekit.sveltekit-link-options
name: sveltekit-link-options
category: computing-software
field: web-development
product: sveltekit
tags: [sveltekit, link-options, data-sveltekit, preload-data, preload-code, navigation, reload]
level: practitioner
status: docs-checked
description: "Control SvelteKit link behaviour with data-sveltekit-preload-data, preload-code, reload, replacestate and reset attributes, and how to disable them."
sources:
  - https://github.com/sveltejs/kit/blob/main/documentation/docs/30-advanced/30-link-options.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: tune how `<a>` (and `<form method="GET">`) navigation behaves. Set `data-sveltekit-*` attributes on the element or any parent.

## data-sveltekit-preload-data
- `"hover"`: start when the mouse rests over the link (touchstart on mobile).
- `"tap"`: start on `touchstart` or `mousedown`.

The default template puts `data-sveltekit-preload-data="hover"` on `<body>` in `src/app.html`:
```html
<body data-sveltekit-preload-data="hover">
	<div style="display: contents">%sveltekit.body%</div>
</body>
```
Use `"tap"` for fast-changing data or when hover causes false positives:
```html
<a data-sveltekit-preload-data="tap" href="/stonks">Get current stonk values</a>
```
`preloadData` from `$app/navigation` does it programmatically. Never preloads when `navigator.connection.saveData` is true.

## data-sveltekit-preload-code
Values from most to least eager: `"eager"`, `"viewport"`, `"hover"`, `"tap"` (hover/tap preload only code). `eager` and `viewport` only apply to links in the DOM right after navigation, not ones added later (e.g. in `{#if}`). It only has an effect if more eager than any `preload-data` value. Ignored under reduced data usage.

## data-sveltekit-reload
Full-page navigation instead of client routing:
```html
<a data-sveltekit-reload href="/path">Path</a>
```
`rel="external"` does the same and is also skipped during prerendering.

## data-sveltekit-replacestate
Replaces the current history entry instead of `pushState`:
```html
<a data-sveltekit-replacestate href="/path">Path</a>
```

## data-sveltekit-reset
By default navigation scrolls to 0,0 (or the `#hash` element) and resets focus. `data-sveltekit-reset="false"` keeps scroll position and focused element; also usable on `<form method="GET">`, e.g. a live search form:
```html
<form data-sveltekit-reset="false">
	<input type="text" name="query">
</form>
```
Avoid it on links (assistive technology users expect focus to move) and only use it on elements that still exist after navigation, or focus is lost.

## Disabling
Use `"false"` inside an enabled region, or conditionally:
```svelte
<div data-sveltekit-preload-data={condition ? 'hover' : false}>
```

## Checked

2026-11-07. Read in full from the sveltejs/kit docs source (including inline snippets; the pages have no external include files): `30-advanced/30-link-options.md`. Every remaining claim, name, default and option was compared line by line with that text. Removed or reworded: nothing; every claim matched the pages.

Method: documentation only; no commands were run.
