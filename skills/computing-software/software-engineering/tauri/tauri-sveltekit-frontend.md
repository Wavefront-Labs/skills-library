---
id: computing-software.software-engineering.tauri.tauri-sveltekit-frontend
name: tauri-sveltekit-frontend
category: computing-software
field: software-engineering
product: tauri
tags: [sveltekit-frontend, tauri]
level: practitioner
status: draft
description: "Configure SvelteKit for Tauri with adapter-static in SPA mode, frontendDist set to build, and SSR disabled in a root layout."
sources:
  - "https://v2.tauri.app/start/frontend/sveltekit/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Tauri with SvelteKit

Goal: run SvelteKit inside Tauri. The page is accurate as of SvelteKit 2.20.4 / Svelte 5.25.8.

## Checklist

- Use SSG and SPA via `static-adapter`. Tauri does not support server-based solutions.
- With SSG and prerendering, `load` functions have no access to Tauri APIs during the build. SPA mode (without prerendering) is recommended, since `load` functions then run only in the webview with access to Tauri APIs.
- Use `build/` as `frontendDist` in `tauri.conf.json`.

## Steps

1. Install the adapter: `npm install --save-dev @sveltejs/adapter-static` (yarn: `yarn add -D`, pnpm: `pnpm add -D`, deno: `deno add -D npm:@sveltejs/adapter-static`).
2. Update `tauri.conf.json` (npm shown; other package managers use their own run commands):

```json
{
  "build": {
    "beforeDevCommand": "npm run dev",
    "beforeBuildCommand": "npm run build",
    "devUrl": "http://localhost:5173",
    "frontendDist": "../build"
  }
}
```

3. Update `svelte.config.js` to use the static adapter with a fallback page:

```js
import adapter from '@sveltejs/adapter-static';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

/** @type {import('@sveltejs/kit').Config} */
const config = {
  preprocess: vitePreprocess(),
  kit: {
    adapter: adapter({
      fallback: 'index.html',
    }),
  },
};

export default config;
```

4. Disable SSR with a root `src/routes/+layout.ts` (or `+layout.js`):

```ts
export const ssr = false;
```

`static-adapter` does not require disabling SSR for the whole app, but doing so lets you use APIs that depend on the global window object, like Tauri's API, without client-side checks. To prefer SSG over SPA mode, change the adapter configuration and `+layout.ts` according to the adapter docs.
