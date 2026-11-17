---
id: computing-software.web-development.sveltekit.sveltekit-adapter-netlify
name: sveltekit-adapter-netlify
category: computing-software
field: web-development
product: sveltekit
tags: [sveltekit, adapter-netlify, netlify, edge-functions, netlify-forms]
level: practitioner
status: docs-checked
description: "Deploy SvelteKit to Netlify with adapter-netlify: edge, split and publish options, _headers/_redirects, Netlify Forms, function context and fs limits."
sources:
  - https://github.com/sveltejs/kit/blob/main/documentation/docs/25-build-and-deploy/80-adapter-netlify.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: deploy to Netlify and use Netlify-specific features. `adapter-auto` installs this adapter automatically, but adding it yourself lets you set options.

## Setup
`npx sv add sveltekit-adapter="adapter:netlify"` or `npm i -D @sveltejs/adapter-netlify`, then:
```js
adapter({
	edge: false,
	split: false,
	publish: 'build'
})
```
- `edge: true` deploys as a Netlify Edge Function instead of the standard Node-based function.
- `split: true` splits the app into multiple functions instead of one.
- `publish`: directory for prerendered pages and static assets (default `build`).

## Prefer SvelteKit features
Built-in SvelteKit features work in dev mode, can be integration-tested, and survive a switch of adapter. Netlify equivalents are useful mainly when migrating an app already on Netlify.

- `_headers` and `_redirects` in the project root apply to static asset responses; `[[redirects]]` in `netlify.toml` also works.
- Netlify Forms: (1) create the HTML form (e.g. `/routes/contact/+page.svelte`) including the hidden `form-name` input; (2) Netlify's build bot parses HTML at deploy time, so prerender the page: `export const prerender = true` on it, or set `prerender.force: true` to prerender everything; (3) if the form has a custom success `action="/success"`, make sure that route exists and is prerendered too.

## Functions context
Endpoints run as Netlify Functions (serverless when `edge` is `false`, edge functions when `true`). Context, including Netlify Identity info, is at `event.platform.context` in hooks and server endpoints:
```js
export const load = async (event) => {
	const context = event.platform?.context;
	console.log(context); // shows up in your functions log in the Netlify app
};
```
Add your own Netlify functions via a directory configured in `netlify.toml`:
```toml
[build]
	command = "npm run build"
	publish = "build"

[functions]
	directory = "functions"
```

## Gotcha: file system
`fs` cannot be used in edge deployments. In serverless deployments it does not work as expected because project files are not copied into the deployment. Use `read` from `$app/server` (it also works in edge by fetching from the deployed public assets), or prerender the routes.

## Checked

2026-11-07. Read in full from the sveltejs/kit docs source (including inline snippets; the pages have no external include files): `25-build-and-deploy/80-adapter-netlify.md`. Every remaining claim, name, default and option was compared line by line with that text. Removed or reworded: nothing; every claim matched the pages.

Method: documentation only; no commands were run.
