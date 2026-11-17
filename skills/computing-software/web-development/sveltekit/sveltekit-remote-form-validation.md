---
id: computing-software.web-development.sveltekit.sveltekit-remote-form-validation
name: sveltekit-remote-form-validation
category: computing-software
field: web-development
product: sveltekit
tags: [sveltekit, remote-functions, remote-form-validation, validation, preflight, issues]
level: practitioner
status: docs-checked
description: "Show remote form validation issues, validate on input, add client-side preflight schemas, raise invalid() issues and keep passwords out of repopulation."
sources:
  - https://github.com/sveltejs/kit/blob/main/documentation/docs/20-core-concepts/60-remote-functions.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: surface and control validation for a `form` remote function.

## Declarative issues

If data fails the schema the handler does not run. Each field's `issues()` returns `{ message: string }[]` and `aria-invalid` is set; if valid or not yet validated it returns `undefined`:

```svelte
{#each createPost.fields.title.issues() as issue}
	<p class="issue">{issue.message}</p>
{/each}
```

`createPost.fields.allIssues()` lists all issues (also `undefined` when valid or unvalidated).

## Validate early

```svelte
<form {...createPost} oninput={() => createPost.validate()}>
```

Issues on controls the user has not touched are ignored by default; use `validate({ includeUntouched: true })` to check everything.

## Preflight (client-side)

```svelte
<form {...createPost.preflight(schema)}>
```

A preflight schema fills `issues()` and stops invalid data being sent. It can be the same object as the server schema but cannot do server checks. You cannot export a schema from a `.remote.ts`/`.remote.js` file: export it from a shared module or a `<script module>` block.

## Programmatic invalid()

For failures only known after trying (e.g. out of stock), call `invalid` from `@sveltejs/kit` in the handler. It throws like `redirect`/`error`; string arguments are form-wide (only in `fields.allIssues()`), Standard Schema issues target a field via the `issue` helper (second handler parameter):

```js
async (data, issue) => {
	try {
		await db.buy(data.qty);
	} catch (e) {
		if (e.code === 'OUT_OF_STOCK') {
			invalid(issue.qty(`we don't have enough hotcakes`));
		}
	}
}
```

## Reading and setting values

`fields.title.value()` is live; `fields.value()` returns `{ title, content }`. Set with `fields.title.set('...')` or `fields.set({ title, content })`. `value()` ignores `as(...)` defaults until edited or submitted.

## Sensitive data

Without JS, `value()` is repopulated after an invalid submit. Prefix a field name with an underscore (`fields._password.as('password')`) to stop it being sent back.

## Checked

Checked 2026-11-07.

Method: documentation only; no commands were run.

Read 60-remote-functions.md (all 1353 lines, every code block): issues(), allIssues(), validate(), preflight, invalid(), value() and set. No claims trimmed.
