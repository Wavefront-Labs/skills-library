---
id: computing-software.web-development.vite.library-package-json
name: library-package-json
category: computing-software
field: web-development
product: vite
tags: [library-exports, library-css, library-env-replacement, css-file-name]
level: advanced
status: docs-checked
description: "Wire a Vite-built library into package.json exports for single and multiple entries, export the extracted CSS, and note env replacement in library mode."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/build.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Recommended `package.json` for a single entry:

```json
{
  "name": "my-lib",
  "type": "module",
  "files": ["dist"],
  "main": "./dist/my-lib.umd.cjs",
  "module": "./dist/my-lib.js",
  "exports": {
    ".": {
      "import": "./dist/my-lib.js",
      "require": "./dist/my-lib.umd.cjs"
    }
  }
}
```

For multiple entries the require side is `.cjs` (`./dist/my-lib.cjs`) and each extra entry gets its own `exports` key, such as `./secondary`.

CSS imported by the library is bundled into one CSS file next to the JS, for example `dist/my-lib.css`. Its name defaults to `build.lib.fileName`; change it with `build.lib.cssFileName`. Export it for users:

```json
"./style.css": "./dist/my-lib.css"
```

Env: in library mode all `import.meta.env.*` are statically replaced in production builds, but `process.env.*` is not, so consumers can change it. To replace it, use `define: { 'process.env.NODE_ENV': '"production"' }` or `esm-env`.

## Checked

Date: 2026-11-07

Read build.md in full. Confirmed against its "Recommended package.json" code group (single and multiple entries, ./secondary), "CSS support" (single CSS file, build.lib.fileName default, build.lib.cssFileName, ./style.css export) and the Environment Variables tip (import.meta.env replaced, process.env not, define and esm-env). Nothing removed.

Method: documentation only; no commands were run.
