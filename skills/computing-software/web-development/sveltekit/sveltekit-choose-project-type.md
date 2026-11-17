---
id: computing-software.web-development.sveltekit.sveltekit-choose-project-type
name: sveltekit-choose-project-type
category: computing-software
field: web-development
product: sveltekit
tags: [sveltekit, project-types, adapter, ssr, spa, static-site, deployment]
level: intro
status: docs-checked
description: "Pick a SvelteKit rendering and deployment style (SSR, static, SPA, serverless, node, mobile, desktop) and the adapter or option that goes with it."
sources:
  - https://github.com/sveltejs/kit/blob/main/documentation/docs/10-getting-started/25-project-types.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: choose how a SvelteKit app is built, deployed and rendered. This is controlled by the chosen adapter plus a little configuration, and can be changed later. Project structure and routing are the same for every type. Rendering settings are not mutually exclusive, so different parts of the app can render differently.

| Want | Use |
|---|---|
| Default | First page SSR, later pages CSR (hybrid, "transitional app") |
| Static site (SSG) | `adapter-static` to prerender everything; or the `prerender` page option for some pages plus another adapter for the rest |
| Very large static site | Incremental Static Regeneration if using `adapter-vercel` |
| Single-page app | CSR only, see the single-page-apps docs |
| Multi-page app | `data-sveltekit-reload` on `<body>` (or specific links); `csr = false` removes all JS on a page and links then render on the server |
| Separate backend (Go, Java, PHP, Ruby, Rust, C#) | Recommended: deploy the frontend separately with `adapter-node` or a serverless adapter. Alternative: SPA served by the backend (worse SEO and performance) |
| Serverless | `adapter-auto` (zero config), or `adapter-vercel`, `adapter-netlify`, `adapter-cloudflare`; vercel/netlify offer an `edge` option |
| Own server / VPS | `adapter-node` |
| Container (Docker, LXC) | `adapter-node` |
| Library | choose the library option in `sv create`, uses `@sveltejs/package` |
| Offline / PWA | service workers |
| Mobile app | SvelteKit SPA wrapped with Tauri or Capacitor |
| Desktop app | SvelteKit SPA wrapped with Tauri, Wails or Electron |
| Browser extension | `adapter-static` or a community extension adapter |
| Embedded device | Svelte runs on low-power devices |

## Gotchas stated by the page
- With an external backend or a pure SPA you can ignore the docs about `server` files.
- Mobile local servers (Capacitor uses HTTP/1) and embedded devices limit concurrent connections: `bundleStrategy: 'single'` in the kit config's `output` option can help by reducing requests.
- Mobile platforms serve your app like a static host on the phone.

## Checked

2026-11-07. Read in full from the sveltejs/kit docs source (including inline snippets; the pages have no external include files): `10-getting-started/25-project-types.md`. Every remaining claim, name, default and option was compared line by line with that text. Removed or reworded: nothing; every claim matched the pages.

Method: documentation only; no commands were run.
