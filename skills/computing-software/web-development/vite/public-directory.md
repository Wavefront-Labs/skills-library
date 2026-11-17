---
id: computing-software.web-development.vite.public-directory
name: public-directory
category: computing-software
field: web-development
product: vite
tags: [public-dir, unhashed-assets, root-absolute-path]
level: intro
status: docs-checked
description: "When to use the public directory: assets never imported or needing exact filenames are served at / and copied as-is; reference them by root absolute path."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/assets.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Put an asset in `public` when it is:
- never referenced in source code (for example `robots.txt`),
- required to keep its exact file name (no hashing), or
- something you do not want to import just to get its URL.

Files are served at `/` in dev and copied to the root of the dist directory as-is. The default is `<root>/public`; change it with the `publicDir` option.

Always reference them by root absolute path: `public/icon.png` is `/icon.png` in source.

```html
<link rel="icon" href="/icon.png" />
```

Guidance from the docs: prefer importing assets unless you specifically need the guarantees of `public`.

## Checked

2026-11-07. Re-read the Vite Static Asset Handling guide (docs/guide/assets.md) in full. Confirmed the three public-directory criteria, served at / in dev and copied to the dist root as-is, the default <root>/public with the publicDir option, root absolute path referencing, and the prefer-importing tip. Changed the HTML example href from /favicon.ico (not on this page) to /icon.png, matching the page's own example.

Method: documentation only; no commands were run.
