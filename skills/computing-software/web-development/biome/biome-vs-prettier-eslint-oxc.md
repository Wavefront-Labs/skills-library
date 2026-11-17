---
id: computing-software.web-development.biome.biome-vs-prettier-eslint-oxc
name: biome-vs-prettier-eslint-oxc
category: computing-software
field: web-development
product: biome
tags: [biome, prettier, eslint, oxc, oxlint, oxfmt, comparison, migration-decision, type-aware-linting, gritql]
level: practitioner
status: docs-checked
description: "Compare Biome with Prettier, ESLint and Oxc on compatibility, speed, plugins, language coverage and type-aware linting to decide on adoption."
sources:
  - https://raw.githubusercontent.com/biomejs/website/main/src/content/docs/en/introduction/comparison-with-other-tools.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Biome vs Prettier.** Biome's formatter is built as a drop-in replacement. It matches Prettier output in about 97 percent of cases and won the Prettier challenge. Intentional differences are listed on the Differences with Prettier page, and default options differ (Biome indents with tabs, Prettier with spaces). Benchmarked about 25x faster, which matters on save, in pre-commit hooks and CI. Prettier still has more stable HTML and HTML super-language support (Vue, Angular) and a large plugin ecosystem. Convert config with `biome migrate prettier`.

**Biome vs ESLint.** Biome's linter is not a drop-in replacement. Most rules are ported from ESLint and plugins such as react, jsx-a11y, import and unicorn, but the rules are curated and follow the rule pillars, so some have different names, fewer options or slightly different behaviour. Names are camelCase, not kebab-case: ESLint `eqeqeq` is Biome `noDoubleEquals`. Origins are on the Rule sources page. About 15x faster. Config is just `@biomejs/biome` and optional `biome.json` instead of parser, TypeScript plugin, framework plugins and eslint-config-prettier. ESLint's JavaScript plugins cannot run in Biome; Biome plugins are written in GritQL. Convert config with `biome migrate eslint`.

**Type-aware linting.** ESLint needs typescript-eslint and the TypeScript compiler. Biome has its own type-aware rules (domain `types`, added in v2) that do not require the `typescript` package; the rule count is smaller but growing.

**Biome vs Oxc.** Oxc's tools (oxlint, oxfmt) are each drop-in replacements with their own config; oxlint keeps ESLint rule names and has an ESLint-compatible alpha plugin API. Biome ships all tools in one package sharing one config and is more opinionated. In Oxc's benchmark its parser is about 5x faster and oxfmt about 3x faster than Biome's formatter; Biome's parser builds a resilient concrete syntax tree so it can format and lint malformed code as you type. Oxlint lints only JavaScript and TypeScript, Biome also lints CSS, JSON, GraphQL and HTML. Oxfmt bundles Prettier for languages not yet native; Biome implements all its languages natively.

## Checked

2026-11-04: every remaining claim, flag, default and example was compared with the cited page(s) read in full and confirmed. Removed: the invented Verify step.

Method: fetched the cited pages with tools/review/fetch_pages.py, read them in full, ran tools/review/phrase_check.py and compared the remaining misses by hand.
