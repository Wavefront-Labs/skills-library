---
id: computing-software.web-development.sveltekit.sveltekit-auth-overview
name: sveltekit-auth-overview
category: computing-software
field: web-development
product: sveltekit
tags: [sveltekit, auth, sessions, jwt, cookies, locals, better-auth]
level: intro
status: docs-checked
description: "Choose between session IDs and JWTs for SvelteKit auth, and wire authentication into the handle hook through cookies and event.locals."
sources:
  - https://github.com/sveltejs/kit/blob/main/documentation/docs/40-best-practices/03-auth.md
  - https://github.com/sveltejs/kit/blob/main/documentation/docs/30-advanced/20-hooks.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SvelteKit auth overview

Goal: decide how to keep users signed in and where to check it.

Authentication verifies who the user is; authorization decides what they may do. After credentials are provided, later requests are usually authenticated by a session ID or a signed token such as a JWT.

## Sessions vs tokens

- Session IDs are typically stored in a database. They can be revoked immediately, at the cost of a database query on every request.
- JWTs generally are not checked against a datastore, so they cannot be revoked immediately. In return you get lower latency and less load on the datastore.

## Where to check

Check auth cookies inside the `handle` hook (`src/hooks.server.js`). If a user matches the credentials, store the user information in `event.locals` so server `load` functions and `+server.js` handlers can use it:

```js
export async function handle({ event, resolve }) {
	event.locals.user = await getUserInformation(event.cookies.get('sessionid'));
	return resolve(event);
}
```

(Augment `App.Locals` in `src/app.d.ts` to type it.) For remote function requests, do not base authorization on `route`, `params` or `url` in `handle`, as they describe the calling page and could be manipulated.

## Libraries and guides

- The Svelte CLI (`sv`) offers to set up Better Auth in a new or existing project.
- To build your own, the Lucia auth guide is a reference for session-based auth with SvelteKit examples.

## Checked

2026-11-07. Read in full from the sveltejs/kit docs source (including inline snippets; the pages have no external include files): `40-best-practices/03-auth.md`, `30-advanced/20-hooks.md`. Every remaining claim, name, default and option was compared line by line with that text. Removed or reworded: nothing; added the hooks page to sources because the `handle`/`locals` claim comes from it.

Method: documentation only; no commands were run.
