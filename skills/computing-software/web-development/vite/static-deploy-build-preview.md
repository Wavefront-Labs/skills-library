---
id: computing-software.web-development.vite.static-deploy-build-preview
name: static-deploy-build-preview
category: computing-software
field: web-development
product: vite
tags: [static-deploy, dist-folder, preview-port-4173, static-vs-ssr]
level: intro
status: docs-checked
description: "Deploy a Vite site statically: build into dist, test with vite preview on its default port, set a preview port, and choose between static, SSR and backend integration."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/static-deploy.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Assumptions in the guides: default output `dist` (change with `build.outDir`), npm, and these scripts:

```json
{ "scripts": { "build": "vite build", "preview": "vite preview" } }
```

`npm run build` writes `dist`, which you deploy to any platform. `npm run preview` serves it locally at `http://localhost:4173`. Change the port with a flag:

```json
{ "scripts": { "preview": "vite preview --port 8080" } }
```

`vite preview` previews the build locally and is not a production server.

Which guide to use: static deployment here; for front-end frameworks that pre-render in Node.js and hydrate, see the SSR guide; for traditional server-side frameworks, see Backend Integration.

## Checked

2026-11-07. Read the opening of the Deploying a Static Site guide (docs/guide/static-deploy.md) through Testing the App Locally; the per-platform sections (about 14k characters in all) were not read and the skill makes no platform claims. Confirmed the dist default and build.outDir, the npm assumption, the build and preview scripts, the http://localhost:4173 default, the --port flag, the not-a-production-server note and the SSR and Backend Integration pointers. Nothing removed.

Method: documentation only; no commands were run.
