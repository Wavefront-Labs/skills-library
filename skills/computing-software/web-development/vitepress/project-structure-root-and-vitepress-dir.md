---
id: computing-software.web-development.vitepress.project-structure-root-and-vitepress-dir
name: project-structure-root-and-vitepress-dir
category: computing-software
field: web-development
product: vitepress
tags: [vitepress, project-structure, project-root, vitepress-directory, srcdir, file-based-routing, source-files]
level: practitioner
status: docs-checked
description: "Understand the project root, the reserved .vitepress folder, source directory, cache and dist locations, and what to gitignore."
sources:
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/guide/getting-started.md
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/guide/routing.md
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/reference/site-config.md
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/guide/asset-handling.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Project root.** The directory VitePress treats as root is where it looks for the special `.vitepress` folder. Running `vitepress dev docs` makes `docs` the root; with no argument the current directory is used.

**`.vitepress` is reserved** for: the config file (`config.js`/`.ts`/`.mjs`/`.mts`), the dev-server cache (`.vitepress/cache`), the production build output (`.vitepress/dist`), and the optional theme folder (`.vitepress/theme`). If you use Git, add `cache` and `dist` to `.gitignore`. Both are movable via `cacheDir` and `outDir`.

**Source files.** Markdown files outside `.vitepress` are source files. Each `.md` becomes a same-path `.html` (file-based routing): `index.md` becomes `/`, `guide/getting-started.md` becomes `/guide/getting-started.html`.

**Source directory vs root.** By default they are the same. Set `srcDir` (resolved relative to root) to keep content in a subfolder, for example `srcDir: 'src'` maps `src/index.md` to `/index.html` while `.vitepress` stays at the root. `srcExclude` takes globs to drop files such as `**/README.md`. The `public` folder lives under the source directory (`docs/public` when root is `docs` and srcDir is default).

```
.                    # project root
├─ .vitepress        # config dir
└─ src               # source dir (srcDir: 'src')
   ├─ getting-started.md
   └─ index.md
```

Rule of thumb: when embedding in an existing repo, scaffold into `./docs`, run commands as `vitepress dev docs`, and keep the repo root clean.

Verify: the page URL tree you see in dev matches your Markdown file tree after applying `srcDir` and any `rewrites`.

## Checked

2026-11-08. Read the VitePress docs source pages getting-started, routing, site-config (config resolution, srcDir, srcExclude, outDir, cacheDir) and asset-handling (public directory). Confirmed the root and source directory rules, the reserved .vitepress contents, gitignore advice, supported config extensions, file-based routing examples, and the public directory location. Added site-config and asset-handling as sources. No claims removed.

Method: docs-only read of cited pages, 2026-11-08
