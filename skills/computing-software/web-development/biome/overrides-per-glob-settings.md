---
id: computing-software.web-development.biome.overrides-per-glob-settings
name: overrides-per-glob-settings
category: computing-software
field: web-development
product: biome
tags: [biome, overrides, overrides-includes, per-file-config, last-match-wins, disable-linter-for-path, language-overrides]
level: practitioner
status: docs-checked
description: "Apply different formatter, linter, assist, plugin and language settings to globbed files with overrides; last matching override wins."
sources:
  - https://raw.githubusercontent.com/biomejs/website/main/src/content/docs/en/reference/configuration.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`overrides` is an array; each entry has `includes` plus any of `formatter`, `linter`, `assist`, `files`, `plugins`, `javascript`, `json`, `css`, `graphql`, `grit`, `html`, `markdown`, `yaml`. When several overrides set the same single-value option, the **last matching override wins**.

- `includes`: globs choosing files. Omitted applies to every file; `[]` applies to none.
- `formatter`: `enabled`, `formatWithErrors`, `indentStyle`, `indentWidth`, `lineEnding`, `lineWidth`, `attributePosition`, `bracketSameLine`, `bracketSpacing`, `delimiterSpacing`, `expand`, `trailingCommas`, `trailingNewline`.
- `linter`: `enabled`, `domains`, `rules`. `assist`: `enabled`, `actions`. `files`: `maxSize`. `plugins`: extra plugins that run in addition to top-level ones.
- Language blocks: `javascript` (parser, formatter, linter, assist, resolver, globals, jsxRuntime, embedded snippets), `json`, `css`, `graphql`, `grit`, `html` (including `experimentalFullSupportEnabled`), `markdown` (including `analyzeEmbeds`), `yaml`.

Examples:

```jsonc
{ "overrides": [
  { "includes": ["scripts/*.js"], "formatter": { "lineWidth": 100 } },
  { "includes": ["lib/**"], "linter": { "rules": { "suspicious": { "noDebugger": "off" } } } },
  { "includes": ["shims/**"], "linter": { "enabled": false } },
  { "includes": [".vscode/**"], "json": { "parser": { "allowComments": true, "allowTrailingCommas": true } } },
  { "includes": ["lib/**"], "javascript": { "formatter": { "quoteStyle": "double" } } }
] }
```

The last one overrides a top-level `javascript.formatter.quoteStyle: "single"` for files in `lib/`. Per-rule `fix` settings are also valid inside overrides.

Verify: lint a file in an overridden path and confirm the rule is silent there only.

## Checked

2026-11-08. Read the overrides section (and linter rule fix text) of the Biome configuration reference; the rest of that 70 KB page was not read for this skill. Confirmed includes semantics, last-match-wins, the per-tool and per-language fields, and the example overrides. Nothing removed.

Method: documentation only; no commands were run.
