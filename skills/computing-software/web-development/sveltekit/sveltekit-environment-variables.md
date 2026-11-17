---
id: computing-software.web-development.sveltekit.sveltekit-environment-variables
name: sveltekit-environment-variables
category: computing-software
field: web-development
product: sveltekit
tags: [sveltekit, env, environment-variables, define-env-vars, private, public, static, validation]
level: practitioner
status: docs-checked
description: "Declare SvelteKit environment variables in src/env.ts with defineEnvVars: private, public, static, schema-validated and documented."
sources:
  - https://github.com/sveltejs/kit/blob/main/documentation/docs/20-core-concepts/70-environment-variables.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: define typed, validated env vars and import them safely. This page documents the explicit-variables approach; the older `$env/*` modules and `$app/environment` are deprecated in SvelteKit 3 (removal in 4).

## Sources and setup
In development and at build time, `.env` and `.env.local` values are added to the environment (`API_KEY=...`). Create `src/env.ts` (or `.js`) exporting `variables`; `defineEnvVars` returns its argument unchanged and exists for type safety:
```ts
import { defineEnvVars } from '@sveltejs/kit/env';

export const variables = defineEnvVars({
	API_KEY: {}
});
```
Each value is an `EnvVarConfig`.

## Private (default) and public
Variables are private by default: `import { API_KEY } from '$app/env/private';`. That module cannot be imported into browser code.

Expose with `public: true`, then import from `$app/env/public` or use `%sveltekit.env.NAME%` in `src/app.html`:
```ts
GOOGLE_ANALYTICS_ID: { public: true }
```
```html
<script async src="https://www.googletagmanager.com/gtag/js?id=%sveltekit.env.GOOGLE_ANALYTICS_ID%"></script>
```

## Validation
`schema` takes a Standard Schema validator (Zod, Valibot) or a function returning the possibly transformed value or throwing:
```ts
import * as v from 'valibot';

GOOGLE_ANALYTICS_ID: { public: true, schema: v.pipe(v.string(), v.regex(/G-[A-Z0-9]+/)) }
```
```ts
schema: (value) => {
	if (!value?.startsWith('G-')) throw new Error('expected a Google Analytics ID');
	return value;
}
```
An invalid value makes the app fail to start (or build). To require a value only at runtime, use `building` from `$app/env`:
```ts
import { building } from '$app/env';
SECRET: { schema: building ? v.optional(v.string()) : v.string() }
```
Validators can also make values optional or transform them (string to boolean, parse JSON).

## Static variables
`static: true` inlines the value into the code, allowing dead-code elimination (default is dynamic):
```ts
SHOW_DEBUG_OVERLAY: {
	public: true,
	static: true,
	schema: v.pipe(v.optional(v.string(), ''), v.transform((str) => str !== ''))
}
```
With `{#if SHOW_DEBUG_OVERLAY}<DebugOverlay />{/if}` (imported from `$app/env/public`), the component is left out of the bundle unless the variable is set when building: `SHOW_DEBUG_OVERLAY=true npm run build`.

## Description
`CACHE_TTL_SECONDS: { description: 'How long to cache responses, in seconds' }` shows on hover in your editor.

## Checked

2026-11-07. Read in full from the sveltejs/kit docs source (including inline snippets; the pages have no external include files): `20-core-concepts/70-environment-variables.md`. Every remaining claim, name, default and option was compared line by line with that text. Removed or reworded: nothing; every claim matched the pages.

Method: documentation only; no commands were run.
