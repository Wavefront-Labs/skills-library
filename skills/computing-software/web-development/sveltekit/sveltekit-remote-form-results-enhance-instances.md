---
id: computing-software.web-development.sveltekit.sveltekit-remote-form-results-enhance-instances
name: sveltekit-remote-form-results-enhance-instances
category: computing-software
field: web-development
product: sveltekit
tags: [sveltekit, remote-functions, remote-form-enhance, form, enhance, svelte]
level: advanced
status: docs-checked
description: "Use a remote form's result, custom enhance callback, for(id) instances and multiple submit buttons in SvelteKit."
sources:
  - https://github.com/sveltejs/kit/blob/main/documentation/docs/20-core-concepts/60-remote-functions.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: control what happens after a remote `form` submits.

## Results

Instead of redirecting, the handler can return data, available as `createPost.result`:

```svelte
{#if createPost.result?.success}<p>Successfully published!</p>{/if}
```

It is ephemeral: it disappears on resubmit, navigation or reload. It can also carry validation errors or data to repopulate the form. If an error occurs during submission, the nearest `+error.svelte` renders.

## enhance

```svelte
<form {...createPost.enhance(async (form) => {
	try {
		if (await form.submit()) {
			form.element.reset();
			showToast('Successfully published!');
		} else {
			showToast('Invalid data!');
		}
	} catch (error) {
		showToast('Oh no! Something went wrong');
	}
})}>
```

With `enhance` the form is not reset automatically; call `form.element.reset()`. The callback gets a copy of the form with everything except `enhance`; `form.submit()` submits directly without rerunning the callback, and `form.element` is always defined there.

## Multiple instances

For forms repeated in a list, `modifyTodo.for(todo.id)` creates an isolated instance. Pass per-item values as the second argument to `.as`:

```svelte
{#each await getTodos() as todo}
	{const modify = modifyTodo.for(todo.id)}
	<form {...modify}>
		<input {...modify.fields.description.as('text', todo.description)} />
		<button disabled={!!modify.pending}>save changes</button>
	</form>
{/each}
```

## Multiple submit buttons

Add a schema field for the button (`action: v.picklist(['login', 'register'])`), bind with `as('submit', value)`:

```svelte
<button {...loginOrRegister.fields.action.as('submit', 'login')}>login</button>
<button {...loginOrRegister.fields.action.as('submit', 'register')}>register</button>
```

Then branch on `action` in the handler. A field named with a leading underscore, such as `_password`, is not sent back to repopulate the form after an invalid non-JavaScript submission.

## Checked

Checked 2026-11-07.

Method: documentation only; no commands were run.

Read 60-remote-functions.md (all 1353 lines, every code block). One trim: the leading-underscore field note now states what the page says (not sent back to repopulate the form after an invalid no-JavaScript submission).
