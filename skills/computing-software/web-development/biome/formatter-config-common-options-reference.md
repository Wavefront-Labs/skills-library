---
id: computing-software.web-development.biome.formatter-config-common-options-reference
name: formatter-config-common-options-reference
category: computing-software
field: web-development
product: biome
tags: [biome, formatter-config, indentstyle, indentwidth, lineending, linewidth, expand, trailingnewline, useeditorconfig, attributeposition, bracketsameline, formatwitherrors]
level: practitioner
status: docs-checked
description: "Reference for general formatter options: defaults and ranges for indent, line width, line ending, expand, bracket options, editorconfig and trailing newline."
sources:
  - https://raw.githubusercontent.com/biomejs/website/main/src/content/docs/en/reference/configuration.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Options under `formatter` apply to all languages unless a language block overrides them.

- `enabled` (true), `includes` (only narrows `files.includes`).
- `formatWithErrors` (false): whether files with syntax errors are formatted.
- `indentStyle`: `tab` (default) or `space`.
- `indentWidth` (default 2, range 0-24): spaces per level with `space`; with `tab` one tab per level and this value is the tab's display width for line-length calculation.
- `lineEnding`: `lf` (default), `crlf`, `cr`, `auto` (CRLF on Windows, LF elsewhere).
- `lineWidth` (default 80, range 1-320): preferred maximum; unbreakable content can exceed it.
- `attributePosition`: `auto` (default) or `multiline` for HTML-like languages.
- `bracketSameLine` (false): closing bracket of a multiline HTML/JSX opening tag on the last attribute line; affects self-closing HTML elements but not self-closing JSX.
- `bracketSpacing` (true): spaces inside braces in supported single-line structures.
- `delimiterSpacing` (false): spaces just inside supported delimiters when content fits on one line; never before opening delimiters or inside empty ones.
- `expand`: `auto` (default; objects go multiline if the first property has a leading newline, arrays stay on one line if they fit), `always`, `never`. `package.json` uses `always` unless configured.
- `trailingNewline` (true): turning it off is strongly discouraged because missing final newlines break text-processing tools and make confusing VCS output.
- `useEditorconfig` (false): loads `indent_style`, `indent_size`, `end_of_line`, `insert_final_newline` from `.editorconfig`. Biome config takes precedence. Only one `.editorconfig` is loaded; cascading nested files and the EditorConfig `root` property are not supported.

## Checked

2026-11-04: every remaining claim, flag, default and example was compared with the cited page(s) read in full and confirmed. Removed: the invented Verify step.

Method: fetched the cited pages with tools/review/fetch_pages.py, read them in full, ran tools/review/phrase_check.py and compared the remaining misses by hand.
