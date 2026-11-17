---
id: computing-software.web-development.frontend-development.spa-history-fallback-hosting
name: spa-history-fallback-hosting
category: computing-software
field: web-development
product: frontend-development
tags: [spa-fallback, hash-routing, history-api-fallback, try-files, spa-hosting, client-side-routing]
level: practitioner
status: docs-checked
description: "Serving single-page apps with history routing: index.html fallback on nginx, Netlify, Vercel, S3/CloudFront and Apache, base paths, and not masking missing assets."
sources:
  - https://router.vuejs.org/guide/essentials/history-mode.html#Example-Server-Configurations
  - https://docs.netlify.com/routing/redirects/rewrites-proxies/#history-pushstate-and-single-page-apps
  - https://nginx.org/en/docs/http/ngx_http_core_module.html#try_files
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SPA history fallback hosting

History-mode routes (`/settings/billing`) exist only in JS. A refresh or deep link asks the server for that path; without a fallback you get 404.

## 1. Configs
```nginx
location /assets/ { try_files $uri =404; add_header Cache-Control "public, max-age=31536000, immutable"; }
location / { try_files $uri $uri/ /index.html; add_header Cache-Control "no-cache"; }
```
```
# Netlify _redirects
/*    /index.html   200
```
```json
// vercel.json
{ "rewrites": [{ "source": "/:path*", "destination": "/index.html" }] }
```
```apache
FallbackResource /index.html
```
- Other hosts (S3 + CloudFront, Firebase Hosting, and so on) need an equivalent rewrite; check the host's docs, and make sure real missing files still return 404.

## 2. Do not fall back for assets
If `/assets/app-3f9a.js` (an old chunk after deploy) falls back to `index.html`, the browser gets HTML where it expects JavaScript and the import fails. Keep assets on a strict 404 path, keep old hashed assets for a while after deploy, and reload the page on chunk-load errors.

## 3. Sub-path deployments
App at `/app/`: set the bundler's public base path and the router's base path, and scope the fallback to `/app/index.html`.

## 4. Hash routing
`/#/settings` never reaches the server, so no config is needed (GitHub Pages, file shares, embedded webviews). Downsides: ugly URLs and fragments are unavailable for in-page anchors.

## Verify
- [ ] Hard-refresh on a deep route returns 200 and the app.
- [ ] `curl -I /assets/does-not-exist.js` returns 404, not HTML.

## Checked
2026-10-28. Confirmed on the Vue Router history-mode page: catch-all fallback to index.html, nginx `try_files $uri $uri/ /index.html`, Apache `FallbackResource`, Netlify `_redirects` with `/* /index.html 200`, Vercel `rewrites` to /index.html. Removed: S3/CloudFront and Firebase specifics, the Vite and React Router base options, `vite:preloadError`, GitHub Pages 404.html trick, SEO claim.
Method: documentation only; no commands were run.
