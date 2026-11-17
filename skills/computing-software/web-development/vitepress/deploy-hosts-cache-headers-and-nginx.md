---
id: computing-software.web-development.vitepress.deploy-hosts-cache-headers-and-nginx
name: deploy-hosts-cache-headers-and-nginx
category: computing-software
field: web-development
product: vitepress
tags: [vitepress, deploy-netlify, deploy-vercel, cloudflare-pages, firebase, cache-control, immutable, nginx, surge, hydration-mismatch]
level: advanced
status: docs-checked
description: "Deploy to generic static hosts, Firebase, Heroku, Surge and others, set immutable cache headers for assets, and use the nginx recipe."
sources:
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/guide/deploy.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Local check first.** `npm run docs:build`, then `npm run docs:preview` serves `.vitepress/dist` at `http://localhost:4173`; add `--port 8080` to change it.

**Generic hosts** (Netlify, Vercel, Cloudflare Pages, AWS Amplify, Render): Build command `npm run docs:build`, output directory `docs/.vitepress/dist`, Node 20 or above. Warning: do not enable HTML "Auto Minify" options; stripping HTML comments that Vue relies on causes hydration mismatch errors.

**Other platforms** (from the guide):
- Azure Static Web Apps: `app_location: /`, `output_location: docs/.vitepress/dist`, `app_build_command: npm run docs:build`.
- Firebase: `firebase.json` with `{"hosting":{"public":"docs/.vitepress/dist","ignore":[]}}` plus `.firebaserc` default project; build then `firebase deploy`.
- Heroku: follow `heroku-buildpack-static` and add `static.json` with `{"root":"docs/.vitepress/dist"}`.
- Surge: `npx surge docs/.vitepress/dist`. The guide also lists harvis (`npx harvis docs/.vitepress/dist`), Hostinger, Lizard, Pethost, Stormkit, CloudRay and deed.page, each with its own instructions or vendor link.

**Cache headers.** Build output uses content-hashed file names under `assets/` (for example `app.4f283b18.js`), so the strongest policy is safe: `Cache-Control: max-age=31536000,immutable`. On Netlify put a `_headers` file in `docs/public/` with a `/assets/*` rule; on Vercel add `headers` to `vercel.json` at the repository root, source `/assets/(.*)`.

**nginx.** The documented server block gzips text assets, sets `Cache-Control` via a `map` ($uri starting with /assets/ gets `public, max-age=31536000, immutable`, everything else `no-cache`), adds security headers, and handles clean URLs with `try_files $uri $uri.html $uri/index.html =404` plus a rule that 301-redirects `/page/` to `/page` when `page.html` exists, and `error_page 404 /404.html`.

## Checked

2026-11-04. Confirmed against the VitePress deploy guide (Build and Test Locally, HTTP Cache Headers with the Netlify and Vercel examples, generic platform settings and Auto Minify warning, Azure, Firebase, Heroku, Surge, harvis, nginx). Removed: the Verify step.

Method: documentation only; no commands were run.
