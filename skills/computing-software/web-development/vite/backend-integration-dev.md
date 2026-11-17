---
id: computing-software.web-development.vite.backend-integration-dev
name: backend-integration-dev
category: computing-software
field: web-development
product: vite
tags: [backend-integration, server-origin, vite-client-script, react-refresh-preamble]
level: advanced
status: docs-checked
description: "Integrate Vite with a traditional backend in dev: config entry, CORS origin, modulepreload polyfill, injecting @vite/client, server.origin and the React refresh preamble."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/backend-integration.md
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/config/shared-options.md
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/config/build-options.md
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/config/server-options.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
For Rails, Laravel and the like, check Awesome Vite for existing integrations first; otherwise configure manually.

Config (the top-level `input` entry replaces the default `.html`; `build.rolldownOptions.input`, if set, overrides it for build only; CORS allows the backend origin; manifest on):

```js
export default defineConfig({
  input: '/path/to/main.js',
  server: { cors: { origin: 'http://my-backend.example.com' } },
  build: { manifest: true },
})
```

Unless you disabled the module preload polyfill (`build.modulePreload.polyfill`; the older `build.polyfillModulePreload` is deprecated), import `vite/modulepreload-polyfill` at the top of your entry.

In your server's dev HTML template (use the URL Vite runs at):

```html
<script type="module" src="http://localhost:5173/@vite/client"></script>
<script type="module" src="http://localhost:5173/main.js"></script>
```

For assets (images) to load, either proxy static asset requests to Vite, or set `server.origin` so generated asset URLs use the back-end server URL.

With `@vitejs/plugin-react` it cannot modify your HTML, so add a script before the others that imports `RefreshRuntime` from `http://localhost:5173/@react-refresh`, calls `injectIntoGlobalHook(window)`, defines `window.$RefreshReg$` and `window.$RefreshSig$`, and sets `window.__vite_plugin_react_preamble_installed__ = true`.

## Checked

Date: 2026-11-07. Read backend-integration.md in full (steps 1-2, React preamble snippet, manifest steps). Confirmed top-level `input` in shared-options.md (read in full) and its relation to `build.rolldownOptions.input` in build-options.md (read in full). Confirmed `build.modulePreload` (polyfill default true) in build-options.md. Corrected the polyfill option: the page's link points at `build.polyfillModulePreload`, but build-options.md marks that option deprecated in favour of `build.modulePreload.polyfill`. server-options.md was NOT read in full; only the `server.cors` and `server.origin` sections were opened and match the skill.

Method: documentation only; no commands were run.
