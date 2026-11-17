---
id: computing-software.web-development.biome.formatter-cli-usage-and-default-options
name: formatter-cli-usage-and-default-options
category: computing-software
field: web-development
product: biome
tags: [biome, formatter, biome-format, format-write, formatter-defaults, editorconfig, shell-glob-expansion, opinionated-formatter]
level: intro
status: docs-checked
description: "Run biome format to check or --write, know the default formatter settings, language-agnostic options, and why shell globs can bite."
sources:
  - https://raw.githubusercontent.com/biomejs/website/main/src/content/docs/en/formatter/index.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Biome's formatter is opinionated, follows Prettier's philosophy of few options, and deliberately resists adding options to prevent bike-shedding.

**CLI.**

```sh
biome format ./src            # emits text diffs for unformatted code
biome format --write ./src    # apply the formatting
```

It accepts files and directories. Caution: if you pass a glob, your shell expands it, and results depend on the shell. Some shells do not support recursive `**` or `{}` alternation in `biome format ./src/**/*.test.{js,ts}`; shell expansion also costs performance and limits how many files you can pass.

**Options.** Biome separates language-agnostic options from language-specific ones. Options can be set on the CLI or in the configuration file; use the configuration file so the CLI and the LSP apply the same options. Since v1.9 `.editorconfig` files can be loaded. Documented defaults:

```json
{
  "formatter": { "enabled": true, "formatWithErrors": false, "attributePosition": "auto",
                 "indentStyle": "tab", "indentWidth": 2, "lineWidth": 80, "lineEnding": "lf" },
  "javascript": { "formatter": { "arrowParentheses": "always", "bracketSameLine": false,
                 "bracketSpacing": true, "delimiterSpacing": false, "jsxQuoteStyle": "double",
                 "quoteProperties": "asNeeded", "semicolons": "always", "trailingCommas": "all" } },
  "json": { "formatter": { "trailingCommas": "none" } }
}
```

The main language-agnostic options: indent style (tab), indent width (2) and line width (80).

Related skills cover the full option reference, suppression comments and Prettier differences.

## Checked

2026-11-04: every remaining claim, flag, default and example was compared with the cited page(s) read in full and confirmed. Removed: the invented Verify step.

Method: fetched the cited pages with tools/review/fetch_pages.py, read them in full, ran tools/review/phrase_check.py and compared the remaining misses by hand.
