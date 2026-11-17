---
id: computing-software.software-engineering.javascript.js-eslint-flat-config
name: js-eslint-flat-config
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, eslint-flat-config, js-linting]
level: practitioner
status: docs-checked
description: "Configure ESLint with eslint.config.js: config objects, files and ignores (global vs non-global), languageOptions, globals, plugins, extends."
sources: ["https://eslint.org/docs/latest/use/configure/configuration-files"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ESLint flat config

Facts from the ESLint "Configuration Files" page:

- The config file is `eslint.config.js`, `.mjs` or `.cjs` (`.ts` needs extra setup). If your `package.json` has `"type": "commonjs"`, `eslint.config.js` must use CommonJS (`require("eslint/config")`).
- It exports an array of configuration objects; `defineConfig()` from `eslint/config` is the helper:
```js
// eslint.config.js
import { defineConfig, globalIgnores } from "eslint/config";

export default defineConfig([
  globalIgnores(["dist/"]),
  {
    files: ["**/*.js"],
    languageOptions: {
      ecmaVersion: "latest",
      sourceType: "module",
      globals: { window: "readonly" },
    },
    rules: { eqeqeq: ["error", "always", { null: "ignore" }] },
  },
]);
```
- Configuration object keys: `name`, `basePath`, `files`, `ignores`, `extends`, `language` (default `js/js`), `languageOptions`, `linterOptions`, `processor`, `plugins`, `rules`, `settings`.
- `languageOptions` for JavaScript: `ecmaVersion` (default `"latest"`), `sourceType` (`"script"`, `"module"` or `"commonjs"`; default `"module"` for `.js`/`.mjs`, `"commonjs"` for `.cjs`), `globals`, `parser` (default espree), `parserOptions`.
- By default ESLint lints `**/*.js`, `**/*.cjs`, `**/*.mjs`. A config object without `files` or `ignores` applies to every file matched by any other object.
- `ignores` with no other keys (besides `name`) is a **global** ignore and may match directories (`dist/`). With other keys it is non-global and matches only files or files within directories: `"dir-to-exclude/"` ignores nothing, use `"dir-to-exclude/**"`. `globalIgnores([...])` makes the intent explicit.
- `plugins` is an object mapping plugin names to plugin objects (imported, not strings). `extends` takes strings, config objects or config arrays; the docs recommend always setting `files` when using `extends`.
- `linterOptions.reportUnusedDisableDirectives` defaults to `"warn"`.

## Self-check
Lint a file under the glob and confirm a rule value from your config applies; the page links the config inspector for debugging which config object matched.

## Checked
Confirmed on the ESLint Configuration Files page: file names, config object keys, language options and defaults, files/ignores semantics, globalIgnores, plugins and extends.
Removed: the ESLint 9 default claim and `ESLINT_USE_FLAT_CONFIG`, the `@eslint/js` and `globals` package examples, and the CLI flags (`--fix`, `--max-warnings`, `--print-config`, `--debug`), which are not on the cited page.
Method: docs-only read of cited pages, 2026-11-08
