---
id: computing-software.web-development.sveltekit.sveltekit-remote-form-fields
name: sveltekit-remote-form-fields
category: computing-software
field: web-development
product: sveltekit
tags: [sveltekit, remote-functions, remote-form-fields, form, valibot, svelte]
level: practitioner
status: docs-checked
description: "Build a SvelteKit remote form with a schema and bind inputs via fields.x.as(type), including nested fields, files, checkboxes, radios and selects."
sources:
  - https://github.com/sveltejs/kit/blob/main/documentation/docs/20-core-concepts/60-remote-functions.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: define a `form` remote function and render its fields.

```js
export const createPost = form(
	v.object({
		title: v.pipe(v.string(), v.nonEmpty()),
		content: v.pipe(v.string(), v.nonEmpty())
	}),
	async ({ title, content }) => {
		const user = await auth.getUser();
		if (!user) error(401, 'Unauthorized');
		const slug = title.toLowerCase().replace(/ /g, '-');
			// insert into the database...
		redirect(303, `/blog/${slug}`);
	}
);
```

Spread the result onto a form: `<form {...createPost}>`. It carries `method` and `action` (works without JavaScript, reloading the page) plus an attachment that enhances it when JS is available. Pass a Standard Schema first if the callback uses `data`.

## Fields

Each schema key is a field. `.as(type)` returns the attributes (type, `name`, repopulated `value`, `aria-invalid`):

```svelte
<input {...createPost.fields.title.as('text')} />
<textarea {...createPost.fields.content.as('text')}></textarea>
```

`.as(type, value)` sets the rendered value, and the value on reset. `radio`, `submit` and `hidden` always need it; `checkbox` needs it when it is one option of an array field. For those, add the checked state as a third argument: `.as('radio', option, settings.visibility === option)`. `file` inputs cannot be populated.

## Nested values, files

Fields nest in objects and arrays (strings, numbers, booleans, `File`). Destructure `const { name, photo, info, attributes } = createProfile.fields;`, then `info.height.as('number')`, `info.likesDogs.as('checkbox')`, `attributes[0].as('text')`. A `file` input needs `enctype="multipart/form-data"` on the form. Names use JS notation (`nested.array[0].value`); quoted keys like `object['nested-array']` are unsupported. Boolean and number names are prefixed `b:` and `n:` so values are coerced before validation.

## Checkbox / select gotchas

- An unchecked checkbox is absent from `FormData`: use `v.optional(v.boolean(), false)` (Zod: `z.boolean().default(false)`).
- Groups of radio/checkbox inputs: `survey.fields.operatingSystem.as('radio', os)`, `survey.fields.languages.as('checkbox', language)`. Alternatively `as('select')` and `as('select multiple')`.
- No selections gives `undefined`, so use `v.optional(v.array(...), [])`.

## Checked

Checked 2026-11-07.

Method: documentation only; no commands were run.

Read 60-remote-functions.md (all 1353 lines, every code block). One fix: the example handler used an undefined slug, so the page's slug line was added.
