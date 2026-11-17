---
id: computing-software.software-engineering.typescript.formatting-with-prettier-and-biome
name: formatting-with-prettier-and-biome
category: computing-software
field: software-engineering
product: typescript
tags: [typescript, typescript-quality, prettier, biome, formatter, code-style, eslint, editorconfig]
level: practitioner
status: verified
description: "Standardise TypeScript/JavaScript formatting with Prettier or Biome: config, ignoring generated files, ESLint coexistence, editor/pre-commit/CI enforcement and migration."
sources:
  - https://prettier.io/docs/en/
  - https://prettier.io/docs/en/integrating-with-linters.html
  - https://biomejs.dev/guides/getting-started/
  - https://biomejs.dev/guides/migrate-eslint-prettier/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Formatting with Prettier or Biome

**Goal:** zero formatting discussions in review: one formatter, applied on save, checked in CI.

## 1. Prettier
```json
// .prettierrc.json - keep it small; every option is a debate
{ "printWidth": 100, "singleQuote": true, "trailingComma": "all" }
```
```
# .prettierignore
dist/
coverage/
pnpm-lock.yaml
*.generated.ts
```
```bash
npx prettier . --write
npx prettier . --check          # CI
```
Pin the exact version (`"prettier": "3.9.10"`, no caret; the Prettier install docs say to install an exact version): minor releases change output.

## 2. Prettier with ESLint
Do not run Prettier as an ESLint rule (the Prettier docs call `eslint-plugin-prettier` slower than running Prettier directly, noisy in editors and "generally not recommended"). Use `eslint-config-prettier` to turn off ESLint's stylistic rules and run the two tools separately.

## 3. Biome: formatter and linter in one binary
```bash
npm i -D -E @biomejs/biome
npx biome init                          # 2.5 writes tabs, double quotes and "preset": "recommended"; the biome.json below overrides them
npx biome migrate prettier --write      # import .prettierrc options
npx biome migrate eslint --write        # map supported ESLint rules
npx biome check --write .               # format + lint + organise imports
npx biome ci .                          # CI mode, no writes
```
```json
// biome.json
{
  "formatter": { "indentStyle": "space", "lineWidth": 100 },
  "javascript": { "formatter": { "quoteStyle": "single" } },
  "files": { "includes": ["src/**", "test/**"] },
  "linter": { "rules": { "recommended": true } }
}
```
Biome formats like Prettier in most cases but deliberately differs in some (see its "differences with Prettier" page; the old "~97% compatible" figure is not on that page); it lacks some ESLint plugin ecosystems (framework-specific rules, type-aware rules), so some teams run Biome for formatting plus ESLint for type-aware linting.

## 4. Enforcement
- Editor: format on save with the project's local formatter (VS Code `editor.defaultFormatter`, commit `.vscode/settings.json`).
- `.editorconfig` for indentation/EOL in tools that do not read formatter configs.
- pre-commit: lint-staged `"*.{ts,tsx,js,json,md}": "prettier --write"` (or `biome check --write --staged`).
- CI: `--check` / `biome ci`.

## 5. Adopting on an existing repo
One commit that only reformats everything, add its hash to `.git-blame-ignore-revs`, merge quickly to minimise conflicts, then turn on the CI check.

## Gotchas
- Two formatters fighting (Prettier + ESLint stylistic, or editor's built-in TS formatter) cause flip-flopping diffs.
- Formatting generated files and lockfiles creates noise; ignore them.
- Markdown/YAML formatting can change meaning in edge cases (embedded code, comments); review the first run.

## Verify
- `prettier --check .` (or `biome ci .`) passes in CI; a deliberately mis-formatted file is fixed on save and blocked by the hook.
