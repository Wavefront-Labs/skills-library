---
id: computing-software.web-development.sveltekit.sveltekit-param-matchers-and-route-sorting
name: sveltekit-param-matchers-and-route-sorting
category: computing-software
field: web-development
product: sveltekit
tags: [sveltekit, param-matchers, params-js, route-sorting, standard-schema, valibot, routing]
level: advanced
status: docs-checked
description: "Validate SvelteKit route params with matchers in src/params.js (or Standard Schema) and predict which route wins when several match."
sources:
  - https://github.com/sveltejs/kit/blob/main/documentation/docs/30-advanced/10-advanced-routing.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: stop `[page]` matching junk like `/fruits/rocketship`, and understand route priority.

## Matcher
Define matchers in `src/params.js` (or `.ts`) with `defineParams`; return the value to accept, nothing to reject:
```js
/// file: src/params.js
import { defineParams } from '@sveltejs/kit/params';

export const params = defineParams({
	fruit: (param) => {
		if (param !== 'apple' && param !== 'orange') return;
		return param;
	}
});
```
Use it in the route name: `src/routes/fruits/[page=fruit]`. A non-match falls through to other routes by sort order, finally 404. A match passes the returned value as the param.

## Standard Schema
```js
/// file: src/params.js
import { defineParams } from '@sveltejs/kit/params';
import * as v from 'valibot';

export const params = defineParams({
	number: v.pipe(v.string(), v.toNumber())
});
```
Failure means no match. On success the param is typed with the schema output, which must extend `string`, `boolean`, `number` or `bigint`; in `src/routes/items/[id=number]/+page.js`, `typeof params.id` is `'number'`.

Transforms must be symmetrical (`toString()` of the number returns the original string) so `resolve` from `$app/paths` can build paths: `resolve('/blog/[id=number]', { id: 1 })`.

Matchers run on server and in the browser. Before SvelteKit 3, each matcher was a separate file under a `params` folder (`src/params/foo.js` exporting `match`), where a truthy return meant a match with no transformation.

## Sorting rules
1. More specific routes win (no params beats one dynamic param).
2. Params with matchers (`[name=type]`) beat those without.
3. `[[optional]]` and `[...rest]` are ignored unless last, where they have lowest priority (`x/[[y]]/z` sorts like `x/z`).
4. Ties break alphabetically.

For `/foo-abc` the order is:
```sh
src/routes/foo-abc/+page.svelte
src/routes/foo-[c]/+page.svelte
src/routes/[[a=x]]/+page.svelte
src/routes/[b]/+page.svelte
src/routes/[...catchall]/+page.svelte
```
So `/foo-def` hits `foo-[c]`.

## Checked

Checked 2026-11-07.

Method: documentation only; no commands were run.

Read 30-advanced/10-advanced-routing.md in full: matchers, Standard Schema, sorting rules and order, encoding. No claims trimmed.
