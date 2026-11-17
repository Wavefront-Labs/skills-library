---
id: computing-software.web-development.sveltekit.sveltekit-form-actions-default-named
name: sveltekit-form-actions-default-named
category: computing-software
field: web-development
product: sveltekit
tags: [sveltekit, forms, form-actions, form-actions-default-named, post, svelte]
level: intro
status: docs-checked
description: "Declare default and named form actions in +page.server.js and invoke them from forms with action and formaction attributes."
sources:
  - https://github.com/sveltejs/kit/blob/main/documentation/docs/20-core-concepts/30-form-actions.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: let a page accept `POST` form data on the server, with or without client-side JavaScript.

## Default action

Export `actions` from `+page.server.js`:

```js
/** @satisfies {import('./$types').Actions} */
export const actions = {
	default: async (event) => {
		// TODO log the user in
	}
};
```

```svelte
<form method="POST">
	<input name="email" type="email">
	<input name="password" type="password">
	<button>Log in</button>
</form>
```

Actions always use `POST`, since `GET` requests should never have side-effects. To invoke the action from a different page (e.g. a login widget in the root layout), add an `action` attribute pointing to the page: `<form method="POST" action="/login">`.

## Named actions

Give the object several keys instead of `default`:

```js
export const actions = {
	login: async (event) => { /* ... */ },
	register: async (event) => { /* ... */ }
};
```

Invoke one by prefixing its name with `/` in a query parameter: `action="?/register"` on the same page, or `action="/login?/register"` from elsewhere.

A button can send the same form data to a different action than its parent form using `formaction`:

```svelte
<form method="POST" action="?/login">
	<!-- inputs -->
	<button>Log in</button>
	<button formaction="?/register">Register</button>
</form>
```

## Gotchas

- You cannot have a `default` action next to named actions. If you POST to a named action without a redirect, the query parameter stays in the URL, so the next default POST would hit the earlier named action.
- Submitting a form that targets another page takes you to that page whether the action succeeds or fails; that is browser behaviour, which `use:enhance` emulates.

## GET forms are not actions

A form with `method="GET"` (or no `method`) never invokes an action. SvelteKit treats it like an `<a>` element, using the client-side router, e.g. `<form action="/search">` navigates to `/search?q=...` and runs `load`. As with links, `data-sveltekit-reload`, `data-sveltekit-replacestate` and `data-sveltekit-reset` can be set on the `<form>`.

## Checked

2026-11-07. Read in full from the sveltejs/kit docs source (including inline snippets; the pages have no external include files): `20-core-concepts/30-form-actions.md`. Every remaining claim, name, default and option was compared line by line with that text. Removed or reworded: nothing; every claim matched the pages.

Method: documentation only; no commands were run.
