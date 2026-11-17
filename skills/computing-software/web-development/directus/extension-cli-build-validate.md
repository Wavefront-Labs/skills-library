---
id: computing-software.web-development.directus.extension-cli-build-validate
name: extension-cli-build-validate
category: computing-software
field: web-development
product: directus
tags: [extension-scaffold, extension-build, extension-validate, extensions-auto-reload]
level: practitioner
status: docs-checked
description: "Scaffold, build, watch, validate and link a Directus extension with create-directus-extension and directus-extension, plus EXTENSIONS_AUTO_RELOAD."
sources:
  - https://raw.githubusercontent.com/directus/docs/main/content/guides/09.extensions/6.cli.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Scaffold (prompts for name, type, language):

```shell
npx create-directus-extension@latest
```

Build (extensions must be built before Directus can use them). The generated script is `"build": "directus-extension build"` from `@directus/extensions-sdk`; Rollup bundles to one entrypoint.

```bash
npm run build
```

Add `--watch` to rebuild on change (`directus-extension build --watch`); `--help` lists options. To reload without restarting Directus set `EXTENSIONS_AUTO_RELOAD=true` in your `docker-compose.yml`.

Validate:

```shell
npx create-directus-extension@latest validate
```

Checks: `built-code`, `directus-config`, `license`, `readme`. Run one with `-c <VALIDATION_NAME>`; `-v` gives a verbose report.

Link into a local Directus project:

```shell
npx create-directus-extension@latest link
```

Optional `extension.config.js` at the package root: `export default { plugins: [], watch: { clearScreen: false } };`

## Checked

2026-11-04: scaffold, build script and Rollup, --watch, EXTENSIONS_AUTO_RELOAD, validate checks, -c and -v flags, link command and extension.config.js example confirmed against the Directus Extension CLI page. Removed a Verify line the page does not state.

Method: documentation only; no commands were run.
