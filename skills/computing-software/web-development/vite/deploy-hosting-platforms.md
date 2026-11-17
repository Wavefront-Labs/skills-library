---
id: computing-software.web-development.vite.deploy-hosting-platforms
name: deploy-hosting-platforms
category: computing-software
field: web-development
product: vite
tags: [netlify-deploy, vercel-deploy, firebase-hosting, surge-deploy]
level: intro
status: docs-checked
description: "Deploy Vite builds to Netlify, Vercel, Cloudflare Pages, Firebase, Surge and Render using the documented CLI commands, build settings and rewrites."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/static-deploy.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
- Netlify CLI: `npm install -g netlify-cli`, `netlify init`, `netlify deploy`, then `netlify deploy --prod`. With Git: import the project, choose branch and output directory.
- Vercel: `npm i -g vercel`, run `vercel`; it detects Vite and sets the right settings. Git import works the same way.
- Cloudflare Pages with Git: pick the framework preset or enter build command and output directory; branches get preview deployments.
- Firebase: `npm i -g firebase-tools`; `firebase.json` hosting with `"public": "dist"` and a rewrite of `**` to `/index.html`; a `.firebaserc` with the project id; then `firebase deploy` after the build.
- Surge: `npm i -g surge`, build, then `surge dist` (add `yourdomain.com` for a custom domain).
- Render static site: Build Command `npm install && npm run build`, Publish Directory `dist`.

The docs also list Azure Static Web Apps, Flightcontrol, xmit, Zephyr Cloud and EdgeOne Pages.

## Checked

Date: 2026-11-07. Read static-deploy.md in full (Netlify, Vercel, Cloudflare Pages, Firebase, Surge, Azure Static Web Apps, Render, and the one-line sections for Flightcontrol, xmit, Zephyr Cloud, EdgeOne Pages). Commands, Firebase rewrite and `.firebaserc`, Render build and publish settings all matched; nothing trimmed.

Method: documentation only; no commands were run.
