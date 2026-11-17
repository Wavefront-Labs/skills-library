---
id: computing-software.web-development.biome.biome-json-structure-and-tool-language-options
name: biome-json-structure-and-tool-language-options
category: computing-software
field: web-development
product: biome
tags: [biome, configuration, biome-json, biome-jsonc, formatter, linter, assist, schema, language-options, javascript-key]
level: intro
status: docs-checked
description: "Structure biome.json around tools (formatter, linter, assist) and language-specific blocks that override general options."
sources:
  - https://raw.githubusercontent.com/biomejs/website/main/src/content/docs/en/configuration/configure-biome.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Biome is configured by CLI options or a file named `biome.json` or `biome.jsonc`. The docs recommend one config file per project so every team member and every editor integration sees the same settings; many options also exist as CLI flags.

The file usually sits in the project root next to `package.json`. Its structure follows the tools Biome provides: the formatter, the linter and the assist. All three are enabled by default and can be turned off with `<tool>.enabled`:

```json
{
  "$schema": "https://biomejs.dev/schemas/<version>/schema.json",
  "formatter": { "enabled": false },
  "linter": { "enabled": false },
  "assist": { "enabled": false }
}
```

Options that apply to several languages go in the tool field. Language-specific options go under `<language>.<tool>`, which can also override the general options and enable or disable a tool per language:

```jsonc
{
  "formatter": { "indentStyle": "space", "lineWidth": 100 },   // defaults: tab, 80
  "javascript": { "formatter": { "quoteStyle": "single", "lineWidth": 120 } },
  "json": { "formatter": { "enabled": false } }
}
```

Here JavaScript gets line width 120 and single quotes, everything else line width 100 with spaces, and JSON is not formatted. Note that Biome calls every JavaScript variant `javascript`, including TypeScript, JSX and TSX.

The full list of options is in the configuration reference.

## Checked

2026-11-04: every remaining claim, flag, default and example was compared with the cited page(s) read in full and confirmed. Removed: the claim that the `$schema` line gives editors completion and the invented Verify step. The `$schema` URL form is confirmed by configuration.mdx (biomejs.dev/schemas/ itself returns 404).

Method: fetched the cited pages with tools/review/fetch_pages.py, read them in full, ran tools/review/phrase_check.py and compared the remaining misses by hand.
