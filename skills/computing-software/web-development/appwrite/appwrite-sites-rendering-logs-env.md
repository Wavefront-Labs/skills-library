---
id: computing-software.web-development.appwrite.appwrite-sites-rendering-logs-env
name: appwrite-sites-rendering-logs-env
category: computing-software
field: web-development
product: appwrite
tags: [appwrite, sites, rendering, ssr, logs, environment-variables]
level: advanced
status: docs-checked
description: "Configure SSR or static rendering for a site, read request logs, and manage site environment variables."
sources:
  - https://github.com/appwrite/website/blob/main/src/routes/docs/products/sites/rendering/+page.markdoc
  - https://github.com/appwrite/website/blob/main/src/routes/docs/products/sites/logs/+page.markdoc
  - https://github.com/appwrite/website/blob/main/src/routes/docs/products/sites/environment-variables/+page.markdoc
  - https://github.com/appwrite/website/blob/main/src/routes/docs/products/sites/rendering/ssr/+page.markdoc
  - https://github.com/appwrite/website/blob/main/src/routes/docs/products/sites/rendering/static/+page.markdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: tune a site's runtime behavior.

Rendering: in Settings > Build settings tick "Server side rendering" or "Static site", then Update and redeploy.
- Static: Next.js set `output: export` in `next.config.js`; SvelteKit use `@sveltejs/adapter-static`; Astro set no `adapter`; Remix set `ssr: false` in the `remix` plugin in `vite.config.ts`. Single page apps are a static site plus a fallback file for routing.
- SSR: Next.js works with default mode, or set `output` to `standalone`; SvelteKit uses `@sveltejs/adapter-node`; Astro uses `@astrojs/node`.

Logs: the table shows Log ID, Status code, Created, Method, Path and Duration. SSR `console.log` and `console.error` output appears in the response logs. Logging can be disabled in Settings > Logging. Retention is 24 hours on Free and 7 days on Pro.

Environment variables: precedence is project, then site, then variables Appwrite injects (for example `APPWRITE_SITE_PROJECT_ID`, which cannot be overridden). Server SDK scopes are `sites.write` and `sites.read`. Secret variables are one-way. Changes take effect on the next deployment. SSR reads variables at runtime; a static site has them inlined at build. Limits: key 255 characters, value 8192 characters.

## Checked

Date: 2026-11-07. Read in full on the appwrite/website docs source (Markdoc): products/sites/rendering, products/sites/logs, products/sites/environment-variables, products/sites/rendering/ssr, products/sites/rendering/static. Code tabs for non-JavaScript SDKs were collapsed when read and Markdoc partials (shared include files) were not opened; all prose and the JavaScript examples were read. Corrections: Added the rendering/ssr and rendering/static pages as sources (read in full); rendering location, framework adjustments, log columns, environment-variable precedence, scopes, limits and one-way secrets now follow the pages; removed the SSR timeout claim (15 s default, 30 s max is on the develop page, not cited here), the client-bundled-variables gotcha and the invented Verify; env vars now described as taking effect on the next deployment.

Method: documentation only; no commands were run.
