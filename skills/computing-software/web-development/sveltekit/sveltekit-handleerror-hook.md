---
id: computing-software.web-development.sveltekit.sveltekit-handleerror-hook
name: sveltekit-handleerror-hook
category: computing-software
field: web-development
product: sveltekit
tags: [sveltekit, hooks, handleerror, errors, app-error, sentry, logging]
level: practitioner
status: docs-checked
description: "Implement SvelteKit handleError in server and client hooks to log unexpected errors and return a safe App.Error shape, with an error ID for support."
sources:
  - https://github.com/sveltejs/kit/blob/main/documentation/docs/30-advanced/20-hooks.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SvelteKit handleError hook

Goal: log every error and control what users see, without leaking messages or stack traces.

`handleError` can be added to `src/hooks.server.js` and `src/hooks.client.js`. It is called for every error thrown while loading, rendering or responding to a request. Redirects are not errors and never reach it.

## What the hook receives

`{ kind, error, event }`, where `kind` is one of:

- `'app'` - created by your code with `error(...)`; `error` is the body matching `App.Error`; default is the body itself.
- `'framework'` - from SvelteKit (404, 405, 413...); `error` is `{ status, message }` with safe text; default is that same object.
- `'validation'` (server only) - a remote function argument failed Standard Schema validation; `error` is `{ status: 400, message: 'Bad Request' }` and `issues` holds the validation issues. Issues are not exposed unless you return them. Use `HandleServerError<CustomIssue>` to type library-specific issue properties.
- `'unknown'` - thrown by your code or code it calls; `error` may contain unsafe information; default is `{ status: 500, message: 'Internal Error' }`.

Return an object matching `App.Error`. `status` and `message` are optional; return them only to override the defaults. If you add _required_ properties to `App.Error`, the hook must return them.

## Adding a tracking ID

Augment the interface in `src/app.d.ts`:

```ts
declare global {
	namespace App {
		interface Error {
			errorId: string;
		}
	}
}

export {};
```

Then in `src/hooks.server.js`:

```js
import * as Sentry from '@sentry/sveltekit';

Sentry.init({/*...*/})

/** @type {import('@sveltejs/kit/hooks').HandleServerError} */
export async function handleError({ kind, error, event }) {
	if (kind === 'app') return error;

	const errorId = crypto.randomUUID();

	if (kind === 'framework') return { ...error, errorId };

	Sentry.captureException(error, { extra: { event, errorId } });

	return { message: 'Whoops!', errorId };
}
```

The client version is identical in structure but typed `HandleClientError`, and `event` is a `NavigationEvent` rather than a `RequestEvent`.

## Gotchas

- Make sure `handleError` never throws.
- Errors already transformed by the server hook are not passed to the client hook a second time.
- In development, a Svelte syntax error arrives with a `frame` property highlighting the location.

## Checked

2026-11-07. Read in full from the sveltejs/kit docs source (including inline snippets; the pages have no external include files): `30-advanced/20-hooks.md`. Every remaining claim, name, default and option was compared line by line with that text. Removed or reworded: nothing; every claim matched the pages.

Method: documentation only; no commands were run.
