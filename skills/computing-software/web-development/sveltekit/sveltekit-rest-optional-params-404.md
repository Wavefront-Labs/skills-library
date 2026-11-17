---
id: computing-software.web-development.sveltekit.sveltekit-rest-optional-params-404
name: sveltekit-rest-optional-params-404
category: computing-software
field: web-development
product: sveltekit
tags: [sveltekit, rest-params, optional-params, catch-all, 404, routing, dynamic-routes]
level: practitioner
status: docs-checked
description: "Use SvelteKit rest ([...file]) and optional ([[lang]]) route parameters, including custom nested 404 pages via a catch-all route."
sources:
  - https://github.com/sveltejs/kit/blob/main/documentation/docs/30-advanced/10-advanced-routing.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: handle variable path depth, optional segments, and nested 404s.

## Rest parameters
```sh
/[org]/[repo]/tree/[branch]/[...file]
```
A request for `/sveltejs/kit/tree/main/documentation/docs/04-advanced-routing.md` yields:
```js
{
	org: 'sveltejs',
	repo: 'kit',
	branch: 'main',
	file: 'documentation/docs/04-advanced-routing.md'
}
```
Gotcha: `src/routes/a/[...rest]/z/+page.svelte` also matches `/a/z` (no parameter) as well as `/a/b/z`, `/a/b/c/z`. Validate the rest value, e.g. with a matcher.

## Custom nested 404
With `marx-brothers/+error.svelte` and `+error.svelte` at the root, visiting `/marx-brothers/karl` does not render the nested error page because no route matched. Add a catch-all route that returns 404:
```js
/// file: src/routes/marx-brothers/[...path]/+page.js
import { error } from '@sveltejs/kit';

/** @type {import('./$types').PageLoad} */
export function load(event) {
	error(404, 'Not Found');
}
```
Unhandled 404s reach `handleError` as framework errors with `kind: 'framework'`; handled ones appear with `kind: 'app'`.

## Optional parameters
`[lang]/home` requires `lang`. Wrap in a second bracket pair, `[[lang]]/home`, so both `home` and `en/home` hit the same page. An optional parameter cannot follow a rest parameter (`[...rest]/[[optional]]`) because matching is greedy and it would always be unused.

## Checked

Checked 2026-11-07.

Method: documentation only; no commands were run.

Read 30-advanced/10-advanced-routing.md in full: rest parameters, 404 handling, optional parameters. No claims trimmed.
