---
id: computing-software.web-development.biome.json-options-parser-and-formatter
name: json-options-parser-and-formatter
category: computing-software
field: web-development
product: biome
tags: [biome, json-formatter, json-parser, allowcomments, allowtrailingcommas, trailingcommas, package-json, expand, bracketspacing]
level: practitioner
status: docs-checked
description: "Reference for json.parser and json.formatter options: defaults, when explicit parser flags override file-type defaults, package.json expand."
sources:
  - https://raw.githubusercontent.com/biomejs/website/main/src/content/docs/en/reference/configuration.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Parser**
- `json.parser.allowComments` (default false) and `json.parser.allowTrailingCommas` (default false). When unset Biome follows the file type's behaviour (see well-known files); an explicit value overrides it, except that `biome.jsonc` always allows comments and trailing commas.

**Formatter** (`json.formatter.*`, applying to JSON, JSONC and recognised JSON-based config files)
- `enabled` (true), `indentStyle` (tab), `indentWidth` (2, 0-24), `lineEnding` (lf), `lineWidth` (80), `trailingNewline` (true).
- `trailingCommas`: `none` (default) or `all`. Use `all` only for JSON variants that allow trailing commas and make sure `allowTrailingCommas` is on or auto-detected for those files.
- `bracketSpacing` (true): `{ "name": "Biome" }` versus `{"name": "Biome"}` for single-line objects.
- `delimiterSpacing` (false): `[ 1, 2, 3 ]` versus `[1, 2, 3]`; empty arrays unchanged.
- `expand`: `auto` (default), `always`, `never`. Biome uses `always` for `package.json` unless expansion is configured explicitly.

`json.linter.enabled` and `json.assist.enabled` default to true.

Example overriding package.json:

```json
{ "overrides": [{ "includes": ["package.json"], "json": { "formatter": { "expand": "auto" } } }] }
```

Example enabling comments for editor settings: an override for `.vscode/**` with `json.parser.allowComments` and `allowTrailingCommas` true.

Verify: `biome format tsconfig.json` accepts comments with no config.

## Checked

2026-11-08. Read the json section of the Biome configuration reference (json.parser through json.assist); the rest of that page was not read for this skill. Confirmed every default, the indentWidth range, trailingCommas guidance, bracketSpacing, delimiterSpacing, expand and the package.json behaviour. Nothing removed.

Method: documentation only; no commands were run.
