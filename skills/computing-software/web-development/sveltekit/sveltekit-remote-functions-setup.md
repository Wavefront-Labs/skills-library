---
id: computing-software.web-development.sveltekit.sveltekit-remote-functions-setup
name: sveltekit-remote-functions-setup
category: computing-software
field: web-development
product: sveltekit
tags: [sveltekit, remote-functions, remote-functions-setup, experimental, vite, svelte]
level: practitioner
status: docs-checked
description: "Enable experimental remote functions, validate arguments with Standard Schema, handle validation errors, getRequestEvent limits and redirects."
sources:
  - https://github.com/sveltejs/kit/blob/main/documentation/docs/20-core-concepts/60-remote-functions.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: turn on remote functions (available since 2.27, experimental) and use them safely.

## Opt in

```js
// vite.config.js
export default defineConfig({
	plugins: [
		sveltekit({
			experimental: { remoteFunctions: true },
			compilerOptions: { experimental: { async: true } }
		})
	]
});
```

## Remote modules

Exports live in a file whose name has a `remote` segment (`remote.ts`, `data.remote.ts`). Four flavours: `query`, `form`, `command`, `prerender`. They always run on the server; on the client they become `fetch` wrappers over a generated HTTP endpoint. Place modules anywhere in `src` except inside a `server` directory.

## Validate arguments

Because each function is an HTTP endpoint, pass a Standard Schema (Zod, Valibot...) as the first argument: `query(v.string(), async (slug) => { ... })`. Invalid input produces a generic 400 Bad Request. The failure goes through the server `handleError` hook with `kind: 'validation'`, an `error` of `{ status, message }`, and `issues`:

```js
export function handleError({ kind, issues }) {
	if (kind === 'validation') {
		console.error(issues);
		return { message: 'Nice try, hacker!' };
	}
}
```

Be careful exposing `issues` to clients; returning `error` unchanged is safe. To opt out, pass `'unchecked'` instead of a schema: `query('unchecked', async ({ id }) => { ... })`.

## getRequestEvent

Inside `query`, `form` and `command`, call `getRequestEvent()` from `$app/server`, e.g. `const { cookies } = getRequestEvent();`. Differences:

- You cannot set headers (cookies may be written, only in `form` and `command`).
- In `query` (including `batch` and `live`), reading `route`, `params` or `url` throws; pass page values as arguments.
- In `form`/`command`, `route`, `params` and `url` describe the calling page and can be manipulated: never use them for authorization.

## Redirects

`redirect(...)` works inside `query`, `form` and `prerender`, not `command` (return `{ redirect: location }` and handle it on the client if you must).

## Checked

Checked 2026-11-07.

Method: documentation only; no commands were run.

Read 60-remote-functions.md (all 1353 lines, every code block) plus the setup, validation error and getRequestEvent sections. No claims trimmed.
