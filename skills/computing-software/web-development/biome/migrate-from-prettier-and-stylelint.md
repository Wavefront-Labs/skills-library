---
id: computing-software.web-development.biome.migrate-from-prettier-and-stylelint
name: migrate-from-prettier-and-stylelint
category: computing-software
field: web-development
product: biome
tags: [biome, migrate-prettier, migrate-stylelint, prettierrc, prettierignore, stylelint, formatter-defaults, css-rules]
level: practitioner
status: docs-checked
description: "Use biome migrate prettier and stylelint to carry options and ignore patterns into biome.json, keeping the same formatting output."
sources:
  - https://raw.githubusercontent.com/biomejs/website/main/src/content/docs/en/installation/migrate-from-other-tools.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Prettier.** `biome migrate prettier --write` ports options from the Prettier configuration and patterns from `.prettierignore`. Biome's defaults differ from Prettier's, so the command writes **every option explicitly** to keep your current output. Example: `.prettierrc.json` with `useTabs: false`, `singleQuote: true` and a `*.json` override with `tabWidth: 2` yields `formatter.indentStyle: "space"`, `indentWidth: 2`, `lineWidth: 80`, `lineEnding: "lf"`, `useEditorconfig: true`, `javascript.formatter.quoteStyle: "single"`, `semicolons: "asNeeded"`, `trailingCommas: "all"`, `arrowParentheses: "always"`, plus an `overrides` entry for `*.json` with `indentWidth: 2`. Remaining differences are listed in the Differences with Prettier page.

**Stylelint.** `biome migrate stylelint --write` ports rules, overrides and ignore patterns, follows `extends`, loads shared and plugin configs, and migrates `ignoreFiles` and `.stylelintignore`. Example: `block-no-empty`, `font-family-no-duplicate-names`, `keyframe-declaration-no-important` become `suspicious.noEmptyBlock`, `noDuplicateFontNames`, `noImportantInKeyframe`; an override setting `block-no-empty: null` for `*.scss` becomes `off`; `ignoreFiles: ["dist/**"]` becomes `linter.includes: ["**", "!dist/**"]`. The result is merged into the existing `biome.json`, so earlier ESLint migrations are kept, and the preset is `none`, so only the explicitly enabled rules run. Only JSON or JavaScript Stylelint configs are supported; YAML is not.

**Inspired rules** work as for ESLint: `--include-inspired` migrates rules that are only inspired by their Stylelint source, which still will not behave identically.

**After migrating.** The old tools skip `.gitignore` files by default; Biome does so only with VCS integration enabled. Once satisfied, remove ESLint, Prettier, Stylelint and their plugins from dependencies and replace the editor extensions with Biome's.

## Checked

2026-11-08. Read the migrate-from-other-tools page in full. Unchanged: explicit option output for Prettier, the Stylelint mapping example, merge behaviour, YAML not supported, inspired rules and the after-migrating notes. Removed: the invented Verify step.

Method: documentation only; no commands were run.
