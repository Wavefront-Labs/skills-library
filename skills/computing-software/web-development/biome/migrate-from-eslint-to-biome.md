---
id: computing-software.web-development.biome.migrate-from-eslint-to-biome
name: migrate-from-eslint-to-biome
category: computing-software
field: web-development
product: biome
tags: [biome, migrate-eslint, eslint, flat-config, include-inspired, cyclic-references, rule-presets, eslintignore]
level: practitioner
status: docs-checked
description: "Run biome migrate eslint --write to port rules, globals, overrides and ignores, with --include-inspired and a fix for cyclic-reference errors."
sources:
  - https://raw.githubusercontent.com/biomejs/website/main/src/content/docs/en/installation/migrate-from-other-tools.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`biome migrate eslint --write` ports rules, globals, overrides and ignore patterns from your ESLint setup. It reads legacy and flat configs, follows `extends`, loads shared and plugin configs, and migrates `.eslintignore`.

Example: an `.eslintrc.json` with `globals: { Global1: "readonly" }`, rules `eqeqeq` and `no-var` as errors, and an override turning `eqeqeq` off for `tests/**` produces a `biome.json` with `linter.rules.preset: "none"`, `suspicious.noDoubleEquals` and `suspicious.noVar` set to `error`, `javascript.globals: ["Global1"]`, and an `overrides` entry with `includes: ["tests/**"]` setting `noDoubleEquals` to `off`.

The command **replaces the linter settings** in your existing `biome.json`: it sets the preset to `none` and enables only the rules it migrated. Review the result before relying on it.

**Inspired rules.** Each Biome rule is either identical to its ESLint source or only inspired by it (see Rule sources). By default only identical rules migrate; add `--include-inspired` for the rest. Even then behaviour is not exactly ESLint's, because some options are not implemented and some rules deliberately differ.

**Cyclic references.** Some plugins and shared configs export objects with cyclic references, which Biome cannot load. Comment out the plugins and shared configs in `eslint.config.js`, run the migration, then restore them one at a time to find the culprit. Configure those plugins' rules by hand in `biome.json` afterwards.

**After migrating.** ESLint skips `.gitignore` files by default but Biome does so only when VCS integration is enabled, so enable it. Then remove ESLint, its plugins and its editor extension, and use Biome's.

## Checked

2026-11-08. Read the migrate-from-other-tools page in full. Unchanged: what migrate eslint ports, the worked example, the preset none replacement behaviour, inspired rules, cyclic references and the .gitignore note. Removed: the invented Verify step.

Method: documentation only; no commands were run.
