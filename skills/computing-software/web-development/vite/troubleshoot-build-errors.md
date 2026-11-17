---
id: computing-software.web-development.vite.troubleshoot-build-errors
name: troubleshoot-build-errors
category: computing-software
field: web-development
product: vite
tags: [file-protocol-cors, case-sensitivity-build, dynamic-import-fetch-failed, version-skew]
level: practitioner
status: docs-checked
description: "Fix build output errors: file:// CORS failures, ENOENT from case-sensitive Linux builds, and 'Failed to fetch dynamically imported module' from version skew or blockers."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/troubleshooting.md
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/build.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
CORS error on built HTML: opening output over the `file` protocol blocks scripts. Serve over http; the easiest is `npx vite preview`.

`ENOENT: no such file or directory` or `Module not found`: usually developed on a case-insensitive filesystem (Windows/macOS) and built on a case-sensitive one (Linux). Fix import casing.

`TypeError: Failed to fetch dynamically imported module` has three causes:
- Version skew: a new deploy deleted old chunks that cached HTML still references. Frameworks may have a built-in fix. Otherwise keep previous chunks for a while, use a service worker to prefetch and cache assets, prefetch dynamic chunks (no help if the HTML itself is cached), or reload on error (see `vite:preloadError`).
- Poor network: browsers with retriable module loading let you retry the import; older ones cache the failure so reload. Retrying cannot fix removed chunks.
- Extensions such as ad-blockers block by file name (for example names containing `ad` or `track`). Pick different names through `build.rolldownOptions.output.chunkFileNames`.

## Checked

2026-11-07. Re-read the Vite Troubleshooting guide (docs/guide/troubleshooting.md) in full, Build section. Confirmed the file protocol CORS error and npx vite preview, the case-sensitivity ENOENT note, and the three causes of 'Failed to fetch dynamically imported module' with their remedies and the chunkFileNames workaround. The vite:preloadError event name is not on that page (it points to Load Error Handling), so the Building for Production guide (docs/guide/build.md, Load Error Handling) was read and added to sources.

Method: documentation only; no commands were run.
