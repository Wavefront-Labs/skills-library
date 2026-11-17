---
id: computing-software.web-development.vite.build-license-file
name: build-license-file
category: computing-software
field: web-development
product: vite
tags: [build-license, dependency-licenses, license-md]
level: intro
status: docs-checked
description: "Generate a dependency license file from the build with build.license, written to .vite/license.md or a custom fileName so it can be served."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/features.md
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/config/build-options.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`build.license` makes the build write a file listing the licenses of dependencies used in the bundle, which you can host to acknowledge them.

```js
import { defineConfig } from 'vite'

export default defineConfig({
  build: {
    license: true,
  },
})
```

Output goes to `.vite/license.md` with a heading per dependency, version and license identifier, followed by the license text.

To serve it at a path such as `https://example.com/license.md`, pass an object:

```js
build: { license: { fileName: 'license.md' } }
```

`build.license` is `boolean | { fileName?: string }`, default `false`. `fileName` is relative to `outDir`; if it ends with `.json`, raw JSON metadata (`name`, `version`, `identifier`, `text` per dependency) is generated instead of markdown.

## Checked

Date: 2026-11-07. Read the License section of features.md (features.md read in full) and the `build.license` section of build-options.md (read in full). Added the type, default, `fileName` relative to `outDir` and the `.json` variant from build-options.md. Existing claims (`.vite/license.md`, per-dependency heading, `fileName: 'license.md'`) matched.

Method: documentation only; no commands were run.
