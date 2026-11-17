---
id: computing-software.web-development.sveltekit.sveltekit-migrate-v3-runtime-security-adapters
name: sveltekit-migrate-v3-runtime-security-adapters
category: computing-software
field: web-development
product: sveltekit
tags: [sveltekit, migrate-v3, migration, csrf, error-handling, remote-functions, adapters, params]
level: advanced
status: docs-checked
description: "SvelteKit 3 upgrade items for cookies, errors, CSRF, params, server-only files, remote functions, redirects and first-party adapters."
sources:
  - https://github.com/sveltejs/kit/blob/main/documentation/docs/60-appendix/35-migrating-to-sveltekit-3.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: handle the non-`$app` breaking changes when upgrading to SvelteKit 3 (config and `$app/*` changes are in sveltekit-migrate-v2-to-v3-config-and-modules).

## Kit imports
- `json()`/`text()` are deprecated: use `Response.json(...)` / `new Response(text)`.
- Moved: `defineParams` to `@sveltejs/kit/params`; env types and `defineEnvVars` to `@sveltejs/kit/env`; hook types like `Handle` to `@sveltejs/kit/hooks`; remote types (`RemoteQuery`, `RemoteForm`, `RemoteCommand`) to `$app/server`.
- `getRequest`/`setResponse` are synchronous: drop `await`. Remove `import '@sveltejs/kit/node/polyfills'`.
- Use `isHttpError`/`isRedirect` instead of `instanceof` on the internal classes.

## Security
- `csrf.checkOrigin: false` is gone; CSRF is always on. Use `csrf: { trustedOrigins: ['https://trusted-site.com'] }`. Set `paths.origin` if the public origin cannot be derived (reverse proxy); with adapter-node it takes precedence over `ORIGIN`.
- Cross-origin mutative requests without a `Content-Type` header are rejected.
- Dev no longer sends `access-control-allow-origin: *` for static assets; set `server: { cors: { origin: '*' } }` in the Vite config if you need it.
- External redirects need opt-in: `redirect(307, 'https://example.com', { external: true })`, or an array of allowed origins (`javascript:` URLs stay blocked with `true`).

## Cookies and errors
- `cookie` v2: ASCII-only names; types renamed to `SerializeOptions` and `ParseOptions`. Cookie `path` now defaults to `'/'`.
- `error(status, message, extra)`: the second argument must be a string; extra `app.d.ts` properties go third.
- `handleValidationError` is removed; validation errors reach `handleError` with `kind: 'validation'`. `handleError` now sees all errors (including expected ones) and may return `status`. `App.Error` always has `status`.
- Rendering errors go through `handleError` to the nearest error boundary. With an async `handleError` in `hooks.client.ts`, enable `compilerOptions.experimental.async`.
- Enhanced form responses use the `fail(...)` status instead of 200. Sourcemaps are generated and applied by default.

## Params and files
- Matchers live in one `src/params.js` / `src/params.ts`; a matcher is a function returning the parsed value (or `undefined`) or a Standard Schema:
```js
import { defineParams } from '@sveltejs/kit/params';
import * as v from 'valibot';

export const params = defineParams({
	integer: v.pipe(v.string(), v.toNumber()),
	fruit: (param) => {
		if (param === 'apple' || param === 'orange') {
			return param;
		}
	}
});
```
- Server-only: any filename with a `server` segment (`stuff.server.ts`, `server.ts`), and any `server` directory except in `src/routes` and `static`.
- Observability: `src/instrumentation.server.js` is picked up automatically; opt into OpenTelemetry with `tracing: { server: true }`.

## Responses and misc
- An empty 2xx (e.g. 204) from `+server.js` has no body. `resolve` in `handle` is typed `Promise<Response>`.
- Links to the current page run `refreshAll()`. `data-sveltekit-*="off"` becomes `"false"`. Route `config` in `+page.js`/`+layout.js` beats the server file. Service workers register as modules.

## Remote functions (experimental)
Enable `experimental.remoteFunctions: true` together with `compilerOptions.experimental.async: true`. Files with a `remote` segment are remote modules (an error if the flag is off). `event.url`, `params`, `route` throw inside queries. Form inputs must spread `myform.fields.message.as('text')`; a hand-written `name` is rejected.

## Adapters
- cloudflare: import `env`, `waitUntil` from `cloudflare:workers`; `cf` is on `request`; `caches` is global; run `wrangler types`; wrangler `^4.67.0`.
- node: rolldown bundling; static assets are listed at build time (files added later are not served); content-hash ETags, no `Last-Modified`; non-GET/HEAD requests to assets get 405.
- netlify: Frameworks API output, Netlify CLI 17.31.0+, `es2022` edge target, publish directory is an adapter option.
- vercel: the `edge` runtime is no longer supported.

## Checked

Checked 2026-11-07.

Method: documentation only; no commands were run.

Read 60-appendix/35-migrating-to-sveltekit-3.md in full (all sections and code blocks): json/text deprecation, moved imports, CSRF and trustedOrigins, redirects, cookies, error and handleError changes, params.js, instrumentation, remote flags and adapter notes. No claims trimmed.
