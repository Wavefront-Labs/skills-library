---
id: computing-software.software-engineering.javascript.js-prettier-eslint-husky
name: js-prettier-eslint-husky
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, prettier-integration, js-linting]
level: practitioner
status: draft
description: "Split formatting (Prettier) from linting and run both on staged files."
sources: ["https://prettier.io/docs/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Prettier and pre-commit integration

- Prettier formats, ESLint finds bugs: disable stylistic ESLint rules with `eslint-config-prettier` and do not run Prettier inside ESLint.
- `.prettierrc`: `{ "singleQuote": true, "trailingComma": "all" }`; `.prettierignore` for build output; `npx prettier --check .` in CI, `--write` locally.
- Pre-commit: `lint-staged` config `{ "*.{js,ts}": ["eslint --fix", "prettier --write"] }` run by Husky or `simple-git-hooks`.
- Pin versions: formatting changes between Prettier majors.
- Add `.editorconfig` for editor consistency.
- Biome is an alternative single-tool formatter/linter.

Self-check: a commit with a badly formatted file is auto-fixed or rejected.
