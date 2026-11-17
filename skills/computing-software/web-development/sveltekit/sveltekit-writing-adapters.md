---
id: computing-software.web-development.sveltekit.sveltekit-writing-adapters
name: sveltekit-writing-adapters
category: computing-software
field: web-development
product: sveltekit
tags: [sveltekit, writing-adapters, adapter-api, builder, custom-adapter]
level: sme
status: docs-checked
description: "Build a custom SvelteKit adapter: the Adapter object shape, what adapt must do with the builder, and the optional emulate, supports and vite hooks."
sources:
  - https://github.com/sveltejs/kit/blob/main/documentation/docs/25-build-and-deploy/99-writing-adapters.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: create an adapter for a platform with no existing one. Start by copying the source of an official adapter for a similar platform.

## Shape
```js
import { getRequest, setResponse } from '@sveltejs/kit/node';

/** @param {AdapterSpecificOptions} options */
export default function (options) {
	/** @type {import('@sveltejs/kit').Adapter} */
	const adapter = {
		name: 'adapter-package-name',
		async adapt(builder) {
			// adapter implementation
		},
		async emulate() {
			return {
				async platform({ config, prerender }) {
					// the returned object becomes `event.platform` during dev, build and
					// preview. Its shape is that of `App.Platform`
				}
			}
		},
		supports: {
			read: ({ config, route }) => {
				// return true if the route with this `config` can use `read` from
				// `$app/server` in production, false if not, or throw a descriptive error
			},
			instrumentation: () => {
				// return true if loading `instrumentation.server.js` is supported,
				// false if not, or throw a descriptive error
			}
		},
		vite: {
			getRequest(options) {
				const request = getRequest(options);
				// modify the Request object here if needed
				return request;
			},
			setResponse(res, response) {
				// handle WebSockets here, for example
				setResponse(res, response);
			},
			plugins: {
				// add plugins here to integrate with Vite
				pre: [],
				post: []
			}
		}
	};

	return adapter;
}
```
`name` and `adapt` are required; `emulate`, `vite` and `supports` are optional.

## What adapt should do
- Clear the build directory.
- Write SvelteKit output with `builder.writeClient`, `builder.writeServer` and `builder.writePrerendered`.
- Output code that imports a `server` instance from `${builder.generateServerInstance()}`, runs `await server.init({ env, read })`, listens for platform requests, converts them to a standard `Request` if needed, calls `server.respond(request, { getClientAddress })` to get a `Response` and returns it, and passes any platform-specific information to SvelteKit through the `platform` option of `server.respond`.
- Bundle the output if the target platform should not need installed dependencies.
- Place static files and generated JS/CSS where the platform expects them.

Recommended layout: final output under `build/`, intermediate output under `.svelte-kit/[adapter-name]`.

## Checked

Checked 2026-11-07.

Method: documentation only; no commands were run.

Read 25-build-and-deploy/99-writing-adapters.md in full. The builder reference page was not opened; the skill makes no claim about builder methods beyond those named on this page. No claims trimmed.
