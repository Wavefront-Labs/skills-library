---
id: computing-software.web-development.sveltekit.sveltekit-accessibility
name: sveltekit-accessibility
category: computing-software
field: web-development
product: sveltekit
tags: [sveltekit, accessibility, a11y, focus-management, route-announcements, lang, title]
level: intro
status: docs-checked
description: "Support SvelteKit's built-in accessibility: unique page titles for route announcements, custom focus after navigation, and a correct per-page lang attribute."
sources:
  - https://github.com/sveltejs/kit/blob/main/documentation/docs/40-best-practices/10-accessibility.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SvelteKit accessibility

SvelteKit provides an accessible foundation (plus Svelte's compile-time a11y checks), but your application code is still your responsibility.

## Route announcements

Client-side routing means no page reload, so SvelteKit injects a live region that reads out the new page name after each navigation, taken from the `<title>`. Give every page a unique, descriptive title:

```svelte
<svelte:head>
	<title>Todo List</title>
</svelte:head>
```

This also helps SEO.

## Focus management

After each navigation and enhanced form submission SvelteKit focuses `<body>`, simulating a full page load. Exception: an element with the `autofocus` attribute is focused instead (consider the assistive technology implications). To customise, use `afterNavigate`:

```js
import { afterNavigate } from '$app/navigation';

afterNavigate(() => {
	/** @type {HTMLElement | null} */
	const to_focus = document.querySelector('.focus-me');
	to_focus?.focus();
});
```

`goto` behaves like a link click by default, but accepts `reset: false` to preserve scroll position and the focused element. If you use it, make sure that element still exists after navigation, otherwise focus is lost and assistive technology users are confused.

## The lang attribute

The default page template sets the document language to English. For other languages, edit `<html>` in `src/app.html`, e.g. `<html lang="de">`. For multiple languages, use a placeholder and fill it in `handle`:

```html
<html lang="%lang%">
```

```js
/** @type {import('@sveltejs/kit/hooks').Handle} */
export function handle({ event, resolve }) {
	return resolve(event, {
		transformPageChunk: ({ html }) => html.replace('%lang%', get_lang(event))
	});
}
```

(`get_lang` is your own function returning the language code for the request.)

## Checked

2026-11-07. Read in full from the sveltejs/kit docs source (including inline snippets; the pages have no external include files): `40-best-practices/10-accessibility.md`. Every remaining claim, name, default and option was compared line by line with that text. Removed or reworded: nothing; every claim matched the pages.

Method: documentation only; no commands were run.
