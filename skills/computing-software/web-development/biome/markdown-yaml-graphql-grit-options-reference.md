---
id: computing-software.web-development.biome.markdown-yaml-graphql-grit-options-reference
name: markdown-yaml-graphql-grit-options-reference
category: computing-software
field: web-development
product: biome
tags: [biome, markdown-config, frontmatter, gfm, cjk-friendly-emphasis, prosewrap, formatembeds, analyzeembeds, yaml-formatter, graphql-formatter]
level: advanced
status: docs-checked
description: "Reference for markdown (frontmatter, GFM, CJK emphasis, proseWrap, embeds), yaml, graphql and grit options with their defaults and gotchas."
sources:
  - https://raw.githubusercontent.com/biomejs/website/main/src/content/docs/en/reference/configuration.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Markdown parser**
- `markdown.parser.frontmatter` (false): parse a leading `---` block and format and lint it as YAML (`file:   "Lorem ipsum"` becomes `file: "Lorem ipsum"`).
- `markdown.parser.gfm` (true): task lists, strikethrough, tables.
- `markdown.parser.cjkFriendlyEmphasis` (false): recognise `*`, `_`, `~~` markers adjacent to Chinese, Japanese or Korean text per the CommonMark CJK-friendly amendments. Enable only if your renderer supports the same amendments; otherwise Biome may treat text as bold that your renderer shows with literal `**`, and formatting can change what readers see. It can also change markers not near CJK text within the same paragraph, heading or table cell.

**Markdown formatter**
- `enabled` (true), `formatEmbeds` (true; formats code in fenced blocks, frontmatter and HTML blocks with that language's formatter; a block with a syntax error is formatted verbatim while the rest is formatted; `false` keeps every block as written), indent/line options, `trailingNewline`.
- `proseWrap`: `preserve` (default), `always` (wrap to lineWidth) or `never` (join paragraphs into one line).
- `markdown.linter.enabled` (true) and `markdown.analyzeEmbeds` (false; runs the linter and assist of the embedded code's language on fenced blocks, frontmatter and HTML blocks).

**YAML:** `yaml.formatter.enabled`, `indentWidth`, `lineEnding`, `lineWidth`, `quoteStyle` (`double` default), `bracketSpacing`, `trailingNewline`, and `yaml.linter.enabled`.

**GraphQL:** formatter `enabled`, `indentStyle`, `indentWidth`, `lineEnding`, `lineWidth`, `bracketSpacing` (true), `trailingNewline`; `quoteStyle` is reserved (the formatter preserves standard double-quoted strings). `graphql.assist.enabled` defaults to **false**.

**GritQL (`grit`)**: formatter and linter default to enabled; `grit.assist.enabled` true.

Verify: with `proseWrap: "always"` and `lineWidth: 30`, a sentence wraps at 30 columns.

## Checked

2026-11-08. Read the graphql, grit, markdown and yaml sections of the Biome configuration reference; other sections were not read for this skill. Confirmed all defaults listed. Corrected the CJK marker list to *, _ and ~~, and reworded the formatEmbeds syntax-error behaviour to match the page wording.

Method: documentation only; no commands were run.
