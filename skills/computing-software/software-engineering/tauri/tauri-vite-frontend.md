---
id: computing-software.software-engineering.tauri.tauri-vite-frontend
name: tauri-vite-frontend
category: computing-software
field: software-engineering
product: tauri
tags: [vite-frontend, tauri]
level: practitioner
status: draft
description: "Configure a Vite frontend for Tauri: tauri.conf.json build hooks, frontendDist, a fixed dev port and TAURI_DEV_HOST for iOS devices."
sources:
  - "https://v2.tauri.app/start/frontend/vite/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Tauri with Vite

Goal: point the Tauri CLI at a Vite dev server and build output. The page is accurate as of Vite 8.

## Checklist

- Use `../dist` as `frontendDist` in `src-tauri/tauri.conf.json`.
- Use `process.env.TAURI_DEV_HOST` as the dev server host IP when set, to run on iOS physical devices.

## Tauri configuration

Given `package.json` scripts `dev` (`vite`), `build` (`tsc && vite build`), `preview` and `tauri` (`tauri`), set (npm shown; yarn, pnpm use `yarn dev`/`pnpm dev` etc., deno uses `deno task dev`):

```json
{
  "build": {
    "beforeDevCommand": "npm run dev",
    "beforeBuildCommand": "npm run build",
    "devUrl": "http://localhost:5173",
    "frontendDist": "../dist"
  }
}
```

## Vite configuration

```js
import { defineConfig } from 'vite';

const host = process.env.TAURI_DEV_HOST;

export default defineConfig({
  // prevent vite from obscuring rust errors
  clearScreen: false,
  server: {
    // make sure this port matches the devUrl port in tauri.conf.json file
    port: 5173,
    // Tauri expects a fixed port, fail if that port is not available
    strictPort: true,
    // if the host Tauri is expecting is set, use it
    host: host || false,
    hmr: host ? { protocol: 'ws', host, port: 1421 } : undefined,
    // tell vite to ignore watching `src-tauri`
    watch: { ignored: ['**/src-tauri/**'] },
  },
  // Env variables starting with these are exposed via `import.meta.env`.
  envPrefix: ['VITE_', 'TAURI_ENV_*'],
  build: {
    // Tauri uses Chromium on Windows and WebKit on macOS and Linux
    target: process.env.TAURI_ENV_PLATFORM == 'windows' ? 'chrome105' : 'safari13',
    // don't minify for debug builds
    minify: !process.env.TAURI_ENV_DEBUG,
    // produce sourcemaps for debug builds
    sourcemap: !!process.env.TAURI_ENV_DEBUG,
  },
});
```
