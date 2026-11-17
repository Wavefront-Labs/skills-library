---
id: computing-software.web-development.vitepress.clean-urls-setup
name: clean-urls-setup
category: computing-software
field: web-development
product: vitepress
tags: [vitepress, cleanurls, clean-urls, html-suffix, netlify, vercel, github-pages, nginx-try-files]
level: practitioner
status: docs-checked
description: "Enable cleanUrls to drop .html from URLs, and check the host can serve /foo as /foo.html without a redirect."
sources:
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/guide/routing.md
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/reference/site-config.md
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/guide/deploy.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
By default VitePress generates pages and internal links ending in `.html`. `cleanUrls: true` removes the suffix: inbound links are generated without `.html`, and if the current path ends in `.html` the router performs a client-side redirect to the extension-less path.

```ts
export default { cleanUrls: true }
```

**Server support is required.** The host must serve `/foo.html` when the browser requests `/foo` **without a redirect**:
- Netlify and GitHub Pages support this by default.
- Vercel needs `cleanUrls` enabled in `vercel.json`.
- nginx: the deploy guide's block uses `try_files $uri $uri.html $uri/index.html =404;` plus a `location ~ ^(?<page>.+)/$` rule that 301-redirects `/page/` to `/page` when `page.html` exists.

If your server cannot do this, do not turn on cleanUrls. Instead, use the directory layout fallback where each page is `name/index.md`:

```
getting-started/index.md
installation/index.md
index.md
```

so URLs are `/getting-started/` and work on any static server.

Do not combine `cleanUrls` with a relocatable `base: './'` build, which needs `.html` links.

## Checked

2026-11-04. Confirmed against the VitePress routing guide (Generating Clean URLs, directory fallback), the site-config page (cleanUrls warning), and the deploy guide (nginx block, relocatable builds needing .html links). Removed: the Verify step.

Method: documentation only; no commands were run.
