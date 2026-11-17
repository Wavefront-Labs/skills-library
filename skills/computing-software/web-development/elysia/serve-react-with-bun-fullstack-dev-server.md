---
id: computing-software.web-development.elysia.serve-react-with-bun-fullstack-dev-server
name: serve-react-with-bun-fullstack-dev-server
category: computing-software
field: web-development
product: elysia
tags: [fullstack-dev-server, static-plugin, react, hmr, tailwind, path-alias, bun-1-3]
level: practitioner
status: docs-checked
description: "Serve a React frontend from an Elysia server with Bun 1.3 Fullstack Dev Server, @elysia/static, HMR, Tailwind 4 and path aliases, no bundler."
sources:
  - https://elysiajs.com/patterns/fullstack-dev-server.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: develop frontend and backend in one Elysia project on Bun 1.3 with hot module replacement and no Vite/Webpack.

## Steps

1. Register the static plugin, and note the `await`; it is required to set up HMR hooks:

```ts
import { Elysia } from 'elysia'
import { staticPlugin } from '@elysia/static'

new Elysia().use(await staticPlugin()).listen(3000)
```

2. Create `public/index.html` with `<div id="root"></div>` and `<script type="module" src="./index.tsx"></script>`, and `public/index.tsx` using `createRoot` from `react-dom/client`.
3. Enable JSX in tsconfig.json: `"compilerOptions": { "jsx": "react-jsx" }`.
4. Open `http://localhost:3000/public`.

Verified by the docs to work with HMR, Tailwind, Tanstack Query, Eden Treaty and path alias.

## Serve at the root

`staticPlugin({ prefix: '/' })` serves files at `/` instead of the default `/public`.

## Tailwind CSS

1. `bun add tailwindcss@4` and `bun add -d bun-plugin-tailwind`.
2. `bunfig.toml`:
```toml
[serve.static]
plugins = ["bun-plugin-tailwind"]
```
3. Create `public/global.css` containing `@tailwind base;`.
4. Reference it from HTML with `<link rel="stylesheet" href="tailwindcss">` or `import './global.css'` in the TSX entry.

## Path alias

In tsconfig.json add `"baseUrl": "."` and `"paths": { "@public/*": ["public/*"] }`, then `import '@public/global.css'`. No extra config is needed.

## Production

Build like any Elysia server: `bun build --compile --target bun --outfile server src/index.ts`. The page says to include the `public` folder when running the executable, similar to the development environment (it does not say where relative to the binary). See the deploy skill for flags and Docker.

## Checked

2026-11-07. Read in full: patterns/fullstack-dev-server (the repo has no include files). Confirmed Bun 1.3, `await staticPlugin()` for the HMR hooks, the `public/index.html` and `index.tsx` files, `"jsx": "react-jsx"`, the `/public` URL, the verified-with list (HMR, Tailwind, Tanstack Query, Eden Treaty, path alias), `prefix: '/'`, the Tailwind steps (`tailwindcss@4`, `bun-plugin-tailwind`, `[serve.static]` in `bunfig.toml`, `@tailwind base;`, the `tailwindcss` link or CSS import), the `@public/*` alias, and the compile command. Reworded the production note: "must sit next to the executable" was stronger than the page.

Method: documentation only; no commands were run.
