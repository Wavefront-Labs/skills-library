---
id: computing-software.web-development.sveltekit.sveltekit-form-action-data-validation-redirects
name: sveltekit-form-action-data-validation-redirects
category: computing-software
field: web-development
product: sveltekit
tags: [sveltekit, forms, form-actions, form-action-fail, validation, redirect, locals]
level: practitioner
status: docs-checked
description: "Read form data in a SvelteKit action, return values or fail() validation errors to the page's form prop, redirect, and keep event.locals in sync after login."
sources:
  - https://github.com/sveltejs/kit/blob/main/documentation/docs/20-core-concepts/30-form-actions.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: handle submitted data in an action and report the outcome back to the page.

## Reading data and returning a result

Each action receives a `RequestEvent`. Read with `request.formData()`; the returned object appears as the `form` prop of the page (and `page.form` app-wide) until the next update:

```js
login: async ({ cookies, request }) => {
	const data = await request.formData();
	const email = data.get('email');
	const password = data.get('password');
	const user = await db.getUser(email);
	cookies.set('sessionid', await db.createSession(user));
	return { success: true };
}
```

```svelte
<script>
	/** @type {import('./$types').PageProps} */
	let { data, form } = $props();
</script>
{#if form?.success}<p>Successfully logged in!</p>{/if}
```

`form` is ephemeral: it vanishes if the user reloads. `PageProps` exists since 2.16.0; before that, type `data` as `PageData` and `form` as `ActionData` separately.

## Validation errors with fail

```js
import { fail } from '@sveltejs/kit';
// inside the action:
if (!email) return fail(400, { email, missing: true });
if (!user || user.password !== db.hash(password)) {
	return fail(400, { email, incorrect: true });
}
```

The status (typically 400 or 422) is available as `page.status`, the data as `form`. Return only the email back, never the password. Repopulate with `value={form?.email ?? ''}` and show `{#if form?.missing}` / `{#if form?.incorrect}` messages. Returned data must be JSON-serializable; with several forms on a page, add an `id` property to tell which `<form>` the data refers to.

With `use:enhance` (or `fetch` with the `accept: application/json` header) the HTTP status matches the `fail` status; returning data gives 200 and returning nothing gives 204.

## Redirects and errors

Work as in `load`: `redirect(303, url.searchParams.get('redirectTo'))` after setting the cookie.

## Loading data after an action

The page re-renders after the action (unless a redirect or unexpected error), so `load` functions rerun. `handle` runs before the action and does not rerun before `load`. So if `handle` fills `event.locals` from a cookie, update `event.locals` when the action changes the cookie:

```js
logout: async (event) => {
	event.cookies.delete('sessionid');
	event.locals.user = null;
}
```

## Checked

2026-11-07. Read in full from the sveltejs/kit docs source (including inline snippets; the pages have no external include files): `20-core-concepts/30-form-actions.md`. Every remaining claim, name, default and option was compared line by line with that text. Removed or reworded: nothing; every claim matched the pages.

Method: documentation only; no commands were run.
