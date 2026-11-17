---
id: computing-software.web-development.eleventy.commonjs-esm-typescript
name: commonjs-esm-typescript
category: computing-software
field: web-development
product: eleventy
tags: [commonjs, esm, typescript, require-esm, dynamic-import, node-versions]
level: practitioner
status: docs-checked
description: "Mix CommonJS, ESM and TypeScript in an Eleventy project: file extensions, package.json type, requiring Eleventy plugins, and Node version limits."
sources:
  - https://www.11ty.dev/docs/cjs-esm/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
ESM is recommended, but CommonJS keeps working; ESM needs Eleventy v3+ (CommonJS v0+).

| Flavor | Explicit extension | Node |
|---|---|---|
| CommonJS | `.cjs` | any |
| ESM | `.mjs` | v12.20+ |
| TypeScript | `.cts` / `.mts` | v22.6+ (needs extra config) |

Switch the whole project with `"type": "module"` in package.json (`.cjs` then marks single CommonJS files), or migrate file by file with `.mjs`. Config files, JS data files, `.11ty.js` templates and JS front matter can each use any flavor.

**Bundled plugins in config** (I18nPlugin, RenderPlugin, HtmlBasePlugin):

```js
// ESM
import { I18nPlugin } from "@11ty/eleventy";
// CommonJS, Node 20.19+
const { I18nPlugin } = require("@11ty/eleventy");
// CommonJS, older Node: async config + dynamic import
module.exports = async function (eleventyConfig) {
  const { I18nPlugin } = await import("@11ty/eleventy");
};
```

ESM plugin default export in old-Node CommonJS: `const { default: myPlugin } = await import("my-eleventy-plugin");`.

Write plugins in ESM if Eleventy 3+ and Node 20.19+ are fine; use CommonJS for Eleventy 2 or Node 20.18 and older. Deno 2+ supports CommonJS; ESM is its default.

## Checked

2026-11-04. Confirmed against the Eleventy page CommonJS, ESM, and TypeScript: the compatibility table (Eleventy v0+ for CommonJS, v3+ for ESM and TypeScript, extensions .cjs/.mjs/.cts/.mts, Node v12.20+ for ESM, v22.6+ for TypeScript, Deno v2+), the package.json type switch, the mixable file types, bundled plugin imports, require(ESM) on Node 20.19+, the dynamic import fallback, the default property for ESM plugins and the plugin-format guidance. Nothing removed.

Method: documentation only; no commands were run.
