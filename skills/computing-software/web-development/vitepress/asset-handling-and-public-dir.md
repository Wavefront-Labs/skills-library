---
id: computing-software.web-development.vitepress.asset-handling-and-public-dir
name: asset-handling-and-public-dir
category: computing-software
field: web-development
product: vitepress
tags: [vitepress, assets, static-assets, public-directory, image-handling, hashed-assets, inline-limit]
level: practitioner
status: docs-checked
description: "Reference images and media with relative paths, use the public directory for robots.txt/favicons, and know hashing and 4 kB inlining."
sources:
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/guide/asset-handling.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
All Markdown compiles to Vue components processed by Vite, so reference assets with **relative URLs**, which the docs say you can and should do:

```md
![An image](./image.png)
```

Absolute paths (based on project root) and relative paths both work in Markdown, theme `.vue` files, styles and plain `.css`. Common image, media and font types are detected automatically. All referenced assets, including absolute ones, are copied to the output directory with a **hashed filename** in production builds; never-referenced assets are not copied. Images smaller than 4 kB are inlined as base64 (configurable through the `vite` option, or `--assetsInlineLimit`).

**Linked files are not assets.** PDFs or other documents referenced by plain links are not processed; put them in `public`.

**The public directory.** Files that are not referenced from content, or that need their original name (`robots.txt`, favicons, PWA icons), go in `public` under the source directory (`docs/public` when root is `docs`). They are copied to the output root as-is, and must be referenced with a root-absolute path: `public/icon.png` is `/icon.png` in source.

**Base URL.** Absolute references to `public` files adapt to `base` automatically. For paths built at runtime (theme config), use `withBase`.

## Checked

2026-11-04. Confirmed against the VitePress asset-handling guide (relative URLs, hashed filenames, 4kb inlining via the vite option, linked files not assets, public directory, root-absolute references, base and withBase) and the CLI reference (--assetsInlineLimit, default 4096 bytes). Removed: the cache-header advice about unhashed public files and the Verify step.

Method: documentation only; no commands were run.
