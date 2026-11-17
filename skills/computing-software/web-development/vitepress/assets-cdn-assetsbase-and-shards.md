---
id: computing-software.web-development.vitepress.assets-cdn-assetsbase-and-shards
name: assets-cdn-assetsbase-and-shards
category: computing-software
field: web-development
product: vitepress
tags: [vitepress, assetsbase, cdn, assetsdir, assetsshards, cors, static-hosting-limits, file-per-directory]
level: sme
status: docs-checked
description: "Serve built assets from a CDN with assetsBase, rename assetsDir, and spread files with assetsShards for host directory limits."
sources:
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/reference/site-config.md
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/guide/asset-handling.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**`assetsBase`** (default undefined) is the URL prefix for everything under `assetsDir` (scripts, styles, fonts, imported images). It must be an absolute URL, a protocol-relative URL or a root-absolute path; a trailing slash is appended if missing.

```ts
export default {
  base: '/',
  assetsBase: 'https://cdn.example.com/'
}
```

Upload the `assets` directory of the build output so it is reachable at `https://cdn.example.com/assets/`, and deploy the rest as usual. HTML pages, Markdown links, `public` files and `hashmap.json` stay on `base`. The CDN should mirror the layout of `outDir`.

CORS: module scripts are always fetched in CORS mode, so a cross-origin CDN must send `Access-Control-Allow-Origin`; VitePress adds `crossorigin` to the emitted script and preload tags when `assetsBase` is another origin.

Only production builds are affected. CLI form: `vitepress build docs --assetsBase "$CDN_URL"`. `vitepress preview` serves a root-absolute value like `/cdn/` from the local dist; an external one is requested from the real URL.

**`assetsDir`** (default `assets`) renames the folder that generated assets live under; it must be inside `outDir`.

**`assetsShards`** (number) spreads assets across `assets/0/` to `assets/N-1/` for hosts that cap files per directory (Netlify allows 54,000). Each page emits two JS files, so a 60,000-page site needs at least three shards plus headroom because files are placed by a hash of their names. Shared chunks stay in `assets/chunks/`; a file's shard depends only on its name, so unchanged files keep their URL across builds.

## Checked

2026-11-04. Confirmed against the VitePress site-config page (assetsBase, assetsDir, assetsShards sections), the asset-handling guide (Serving Assets from a CDN) and the CLI reference (--assetsBase). Removed: the Verify step; every other claim matched the pages.

Method: documentation only; no commands were run.
