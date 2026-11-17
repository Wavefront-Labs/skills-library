---
id: computing-software.web-development.frontend-development.eslint-flat-config-and-prettier
name: eslint-flat-config-and-prettier
category: computing-software
field: web-development
product: frontend-development
tags: [build-tooling, eslint-flat-config, prettier, linting, typescript-eslint, code-quality]
level: practitioner
status: verified
description: "Configuring ESLint 9 flat config with typescript-eslint and framework plugins, running Prettier separately, and wiring both into editors, pre-commit and CI."
sources:
  - https://eslint.org/docs/latest/use/configure/configuration-files
  - https://typescript-eslint.io/getting-started
  - https://prettier.io/docs/integrating-with-linters
  - https://eslint.org/docs/latest/use/configure/migration-guide
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ESLint flat config and Prettier

## 1. `eslint.config.js`
```js
import js from "@eslint/js";
import tseslint from "typescript-eslint";
import reactHooks from "eslint-plugin-react-hooks";
import globals from "globals";
import prettier from "eslint-config-prettier";
import { defineConfig, globalIgnores } from "eslint/config";

export default defineConfig([
  globalIgnores(["dist/", "coverage/", ".next/"]),
  js.configs.recommended,
  {
    files: ["**/*.{ts,tsx}"],              // type-aware rules only where a tsconfig covers the file
    extends: [tseslint.configs.recommendedTypeChecked],
    languageOptions: { parserOptions: { projectService: true, tsconfigRootDir: import.meta.dirname } },
  },
  { languageOptions: { globals: globals.browser } },
  reactHooks.configs.flat["recommended-latest"],   // v7 plugin: `configs.flat.*` is the flat-config form
  { files: ["**/*.test.ts"], rules: { "@typescript-eslint/no-floating-promises": "off" } },
  prettier,                 // last: turns off rules that conflict with formatting
]);
```
- Flat config is an array; later objects override earlier ones for matching `files`. No more `.eslintrc`, `extends` strings or `.eslintignore` (default in ESLint 9; the eslintrc system was removed in v10.0.0).
- Migrate: `npx @eslint/migrate-config .eslintrc.json`; inspect with `npx eslint --inspect-config`.
- Type-aware rules (`no-floating-promises`, `no-misused-promises`) catch real bugs but are slower - scope them to TS source files. Applied to every file (including `eslint.config.js` itself) they fail with "was not found by the project service" unless the file is in a tsconfig.
- `eslint-plugin-react-hooks` 7.x: `configs.recommended` / `configs["recommended-latest"]` are legacy eslintrc objects (`plugins` is an array) and make flat config throw; use `configs.flat.recommended` or `configs.flat["recommended-latest"]`.
- typescript-eslint 8.x refuses TypeScript 7.0 ("does not support TS 7.0"): pin `typescript@6` for linting until it supports 7.1+.

## 2. Prettier separately
Do not run Prettier as an ESLint rule (`eslint-plugin-prettier`) - slow and noisy. Use `eslint-config-prettier` to disable conflicting stylistic rules and run `prettier --check .` as its own step. Commit `.prettierrc` and `.prettierignore`; pin the exact Prettier version (output changes between minors).

## 3. Wiring
- Editor: format on save with Prettier; ESLint fix on save for `source.fixAll.eslint`.
- Pre-commit: `lint-staged` + husky/lefthook: `"*.{ts,tsx}": ["eslint --fix", "prettier --write"]`.
- CI: `eslint . --max-warnings 0` and `prettier --check .`. Cache: `eslint --cache --cache-location node_modules/.cache/eslint`.
- Alternative all-in-one: Biome (fast, fewer plugins).

## 4. Pitfalls
- Disabling rules inline without reason - require `--report-unused-disable-directives` and the `require-description` rule of `@eslint-community/eslint-plugin-eslint-comments`.
- Monorepos: one root config with `files` globs per package beats many configs.

## Verify
`npx eslint --inspect-config` opens the config inspector; CI fails on a deliberately unformatted file.
