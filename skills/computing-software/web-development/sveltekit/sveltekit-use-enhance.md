---
id: computing-software.web-development.sveltekit.sveltekit-use-enhance
name: sveltekit-use-enhance
category: computing-software
field: web-development
product: sveltekit
tags: [sveltekit, forms, form-actions, use-enhance, progressive-enhancement, svelte]
level: practitioner
status: docs-checked
description: "Progressively enhance SvelteKit forms with use:enhance, a custom SubmitFunction, update options and applyAction behaviour."
sources:
  - https://github.com/sveltejs/kit/blob/main/documentation/docs/20-core-concepts/30-form-actions.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: submit action forms without full page reloads when JavaScript is available.

```svelte
<script>
	import { enhance } from '$app/forms';
	let { form } = $props();
</script>
<form method="POST" use:enhance>
```

`use:enhance` only works on forms with `method="POST"` that point to actions in a `+page.server.js`. Using it on a GET form or on a form posting to a `+server.js` endpoint errors.

## Default behaviour (no argument)

- Action on the same page: emulates a reload, updating `form`, `page.form` and `page.status` on success or invalid result.
- Action on a different page: navigates to the action URL on success or invalid response, populating that page's `form` and `page.status`; a history entry is pushed.
- Resets the `<form>`, runs `refreshAll` on success, calls `goto` on redirect, renders the nearest `+error` boundary on unexpected error, and resets focus.

The landing URL is `result.location`: the form action with the `?/actionName` parameter removed (`/login?/do-login` lands on `/login`; other query params stay). A relative `action="?/delete"` on `/items?page=2` drops `page=2`; write `action="?page=2&/delete"` to keep it.

To stay on the current page for a cross-page submission:

```svelte
<form method="POST" action="/other/page?/subscribe"
	use:enhance={() => async ({ update }) => {
		await update({ navigate: false });
	}}>
```

## Customising

```svelte
use:enhance={({ formElement, formData, action, cancel, submitter }) => {
	// cancel() prevents the submission
	return async ({ result, update }) => {
		// result is an ActionResult; update runs the default logic
	};
}}
```

Use this for loading UI. Returning a callback overrides the default post-submit behaviour; restore it by calling `update`, or use `applyAction(result)` from `$app/forms`.

`update` options: `reset: false` keeps form values; `refreshAll` (default true on success, false on failure; `invalidateAll` is a deprecated alias); `navigate: false` applies a non-redirect result to the current page (redirects are always followed).

## applyAction by result.type

- `success`, `failure`: sets `page.status` to `result.status`, updates `form` and `page.form` to `result.data`.
- `redirect`: calls `goto(result.location, { refreshAll: true })`.
- `error`: renders the nearest `+error` boundary.

Focus is reset in all cases. `applyAction` does not navigate to a non-redirect result's `location` or refresh data; use `update` for the full default.

## Checked

Checked 2026-11-07.

Method: documentation only; no commands were run.

Read 20-core-concepts/30-form-actions.md in full, with focus on use:enhance, update options, applyAction and the result.location note. $app/forms reference page not opened; no claim depends on it. No claims trimmed.
