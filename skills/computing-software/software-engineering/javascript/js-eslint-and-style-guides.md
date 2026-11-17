---
id: computing-software.software-engineering.javascript.js-eslint-and-style-guides
name: js-eslint-and-style-guides
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, js-eslint, flat-config, style-guide, code-linting]
level: practitioner
status: docs-checked
description: "Configure ESLint with a flat config file, the recommended rule set and CLI flags, and keep formatting rules out of the linter."
sources: ["https://eslint.org/docs/latest/use/configure/configuration-files", "https://eslint.org/docs/latest/use/configure/language-options", "https://eslint.org/docs/latest/use/configure/migration-guide", "https://eslint.org/docs/latest/use/configure/rules", "https://eslint.org/docs/latest/use/command-line-interface", "https://prettier.io/docs/integrating-with-linters"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ESLint and style

- Flat config: put `eslint.config.js` (or `.mjs`, `.cjs`) in the project root; it exports an array of configuration objects (the `defineConfig()` helper from `eslint/config` builds one). A project with `"type": "commonjs"` must write the file in CommonJS.
- The recommended rules ship in the `@eslint/js` package: install it and either add `js.configs.recommended` as an entry or use `plugins: { js }` with `extends: ["js/recommended"]` (give that object a `files` key). `js/all` is not recommended for production because it changes with every release.
- Rules are set per configuration object, e.g. `rules: { eqeqeq: "error", "no-var": "error", "prefer-const": "error" }`. Rules that catch real bugs and exist in the rule reference include `no-undef`, `no-unused-vars`, `no-unreachable`, `require-atomic-updates` and `no-prototype-builtins`.
- Language options live under `languageOptions`: `ecmaVersion` (default `"latest"`), `sourceType` (default `"module"` for `.js` files), and `globals`. Groups of runtime globals come from the `globals` npm package, which ESLint does not install for you.
- Migrating from eslintrc: `npx @eslint/migrate-config .eslintrc.json` converts a config; it does not handle `.eslintrc.js` files well.
- Let a formatter own style. Prettier says to use it for formatting and linters for code quality, and to turn off conflicting stylistic rules with `eslint-config-prettier`.
- CLI: `--fix` applies fixes (`--fix-type` limits kinds, `--fix-dry-run` does not write). `--max-warnings 0` makes any warning exit non-zero, which suits CI.
- Disable a line with `// eslint-disable-next-line rule-name -- reason`; the description after two or more `-` characters documents why.
- Pick one style guide per repository and do not mix them.

## Checked

Confirmed on the cited ESLint pages (configuration files, language options, migration guide, rules, CLI) and the Prettier "Integrating with Linters" page. Removed: the claims that ESLint 9 made flat config the default and that `ESLINT_USE_FLAT_CONFIG=false` restores the old format (the migration page only mentions setting it to true for v8), `no-floating-promises` (typescript-eslint page could not be read), and the named style guides Airbnb, Google and StandardJS (no cited source). The old sources tc39 and MDN did not cover ESLint.

Method: docs-only read of cited pages, 2026-11-08
