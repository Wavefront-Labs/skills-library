---
id: computing-software.web-development.sveltekit.sveltekit-service-worker
name: sveltekit-service-worker
category: computing-software
field: web-development
product: sveltekit
tags: [sveltekit, service-workers, offline, caching, precache, pwa, registration]
level: advanced
status: docs-checked
description: "Add a SvelteKit service worker that precaches build assets, set up its TypeScript config, register it manually, and trigger update checks on navigation."
sources:
  - https://github.com/sveltejs/kit/blob/main/documentation/docs/30-advanced/40-service-workers.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SvelteKit service workers

Goal: speed up navigation (and optionally work offline) by precaching built JS/CSS.

If `src/service-worker/index.ts` exists it is bundled and registered automatically. (`src/service-worker.ts` or `.js` also works; see type safety below.) The worker is bundled for production but not during development.

## Imports

- `$app/service-worker` exports `self` (`globalThis` typed as `ServiceWorkerGlobalScope`).
- `$app/env` exports `version`, useful for deployment-scoped caches.
- `$app/manifest` exports `immutable` build files, `assets`, and `prerendered` content.

## Typical worker

```js
import { self } from '$app/service-worker';
import { version } from '$app/env';
import { immutable, assets } from '$app/manifest';
import { resolve } from '$app/paths';

const CACHE = `cache-${version}`;

// manifest paths are relative to the base path; resolve to absolute pathnames
const ASSETS = [
	...immutable.map((asset) => resolve(asset.path)),
	...assets.map((asset) => resolve(asset.path))
];

self.addEventListener('install', (event) => {
	async function addFilesToCache() {
		const cache = await caches.open(CACHE);
		await cache.addAll(ASSETS);
	}
	event.waitUntil(addFilesToCache());
});

self.addEventListener('activate', (event) => {
	async function deleteOldCaches() {
		for (const key of await caches.keys()) {
			if (key !== CACHE) await caches.delete(key);
		}
	}
	event.waitUntil(deleteOldCaches());
});
```

The docs' full example also adds a `fetch` handler: ignore non-GET requests, serve `ASSETS` from cache, otherwise try the network first, cache 200 responses without `cache-control: no-store` in the background, and fall back to the cache on failure.

Be careful caching: stale data can be worse than unavailable data offline, and browsers empty caches when full, so avoid caching large files such as video.

## Type safety

Exclude the worker from the root `tsconfig.json` (`"exclude": ["src/service-worker"]`) and give it its own `src/service-worker/tsconfig.json`:

```json
{
	"extends": "$app/tsconfig/service-worker"
}
```

## Manual registration

You can disable automatic registration (the `serviceWorker` option in the Vite plugin config) and register yourself with `navigator.serviceWorker.register(url, { type: 'module' })`.

## Updating

Browsers check for a new worker on full-page navigations and after functional events like `push` and `sync`, not on client-side navigations. SvelteKit only calls `registration.update()` during error recovery after detecting a redeploy. To check more eagerly, in the root layout:

```js
import { afterNavigate } from '$app/navigation';

afterNavigate(async () => {
	if ('serviceWorker' in navigator) {
		const registration = await navigator.serviceWorker.getRegistration();
		await registration?.update();
	}
});
```

A new worker installs in the background and takes over once the number of tabs managed by the old one drops to zero. For Workbox-style PWAs the docs point to the Vite PWA plugin.

## Checked

Checked 2026-11-07.

Method: documentation only; no commands were run.

Read 30-advanced/40-service-workers.md in full. The serviceWorker config option appears on that page only as a link anchor, so its name and default were checked in packages/kit/src/exports/vite/public.d.ts of the sveltejs/kit repo. No claims trimmed.
