---
id: computing-software.web-development.sveltekit.sveltekit-form-action-custom-fetch
name: sveltekit-form-action-custom-fetch
category: computing-software
field: web-development
product: sveltekit
tags: [sveltekit, forms, form-actions, action-custom-fetch, deserialize, fetch]
level: advanced
status: docs-checked
description: "Enhance a SvelteKit form by hand with fetch, deserialize and applyAction, and target a page action when a +server.js sits alongside it."
sources:
  - https://github.com/sveltejs/kit/blob/main/documentation/docs/20-core-concepts/30-form-actions.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: implement progressive enhancement without `use:enhance`.

```svelte
<script>
	import { refreshAll, goto } from '$app/navigation';
	import { applyAction, deserialize } from '$app/forms';

	async function handleSubmit(event) {
		event.preventDefault();
		const data = new FormData(event.currentTarget, event.submitter);

		const response = await fetch(event.currentTarget.action, {
			method: 'POST',
			body: data
		});

		/** @type {import('$app/forms').ActionResult} */
		const result = deserialize(await response.text());

		if (result.type !== 'redirect' && result.location !== undefined) {
			if (result.location === location.pathname + location.search) {
				if (result.type === 'success') await refreshAll();
			} else {
				await goto(result.location, { refreshAll: result.type === 'success' });
			}
		}

		await applyAction(result);
	}
</script>

<form method="POST" onsubmit={handleSubmit}>
```


## Rules

- Use `deserialize` from `$app/forms`, not `JSON.parse()`: actions, like `load`, can return `Date` or `BigInt` values.
- If a `+server.js` lives next to the `+page.server.js`, `fetch` requests go to the `+server.js` by default. To POST to the page's action instead, add the header `'x-sveltekit-action': 'true'`:

```js
const response = await fetch(this.action, {
	method: 'POST',
	body: data,
	headers: { 'x-sveltekit-action': 'true' }
});
```

- `applyAction` alone does not navigate or refresh data; inspect `result.location` and use `goto` or `refreshAll` as the example does.

## Alternative: +server.js

Form actions are the preferred way to send data because they can be progressively enhanced, but a `+server.js` can expose a JSON API: export `POST()` from `src/routes/api/ci/+server.js` and call `fetch('/api/ci', { method: 'POST' })` from a click handler.

## Checked

2026-11-07. Read in full from the sveltejs/kit docs source (including inline snippets; the pages have no external include files): `20-core-concepts/30-form-actions.md`. Every remaining claim, name, default and option was compared line by line with that text. Removed or reworded: the sentence that passing `event.submitter` to `FormData` includes the clicked button's value (the page shows the call but does not state this).

Method: documentation only; no commands were run.
