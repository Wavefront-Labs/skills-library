---
id: computing-software.web-development.biome.javascript-formatter-options-reference
name: javascript-formatter-options-reference
category: computing-software
field: web-development
product: biome
tags: [biome, javascript-formatter, quotestyle, jsxquotestyle, quoteproperties, trailingcommas, semicolons, arrowparentheses, operatorlinebreak, bracketspacing]
level: practitioner
status: docs-checked
description: "Reference for javascript.formatter options and defaults: quotes, semicolons, trailing commas, arrow parens, expand, operator line breaks and spacing."
sources:
  - https://raw.githubusercontent.com/biomejs/website/main/src/content/docs/en/reference/configuration.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Defaults and values under `javascript.formatter` (applies to JS, TS, JSX, TSX and languages embedding JavaScript; these override the global `formatter` options):

- `quoteStyle`: `double` (default) or `single`; Biome uses the other quote when that avoids extra escaping.
- `jsxQuoteStyle`: `double` (default) or `single` for JSX attribute values.
- `quoteProperties`: `asNeeded` (default; removes quotes where the name is valid unquoted) or `preserve`.
- `trailingCommas`: `all` (default; including function parameters and calls), `es5` (array/object literals only, excluding parameters, calls and TypeScript type parameters), `none`.
- `semicolons`: `always` (default) or `asNeeded` (omit except where needed to avoid ASI hazards).
- `arrowParentheses`: `always` (default) or `asNeeded` (omit for a single parameter when allowed).
- `operatorLinebreak`: `after` (default; operator ends the line) or `before` (operator starts the next line).
- `bracketSameLine` (false): JSX closing bracket at the end of the last attribute line when true; self-closing JSX unaffected.
- `bracketSpacing` (true): `{ value: 1 }` versus `{value: 1}`.
- `delimiterSpacing` (false): spaces inside parentheses, square brackets, template interpolations, TypeScript angle brackets and JSX expression braces; also spacing after logical NOT (in a chain only the final operator gets a space). Empty delimiters unchanged.
- `attributePosition`: `auto` or `multiline` for JSX.
- `expand`: `auto`, `always`, `never` for arrays and objects.
- `enabled`, `indentStyle` (default tab), `indentWidth` (default 2, 0-24), `lineEnding` (default lf), `lineWidth` (default 80, 1-320), `trailingNewline` (default true).

```json
{ "javascript": { "formatter": { "quoteStyle": "single", "semicolons": "asNeeded", "trailingCommas": "es5" } } }
```

## Checked

2026-11-04: every remaining claim, flag, default and example was compared with the cited page(s) read in full and confirmed. Removed: the invented Verify step.

Method: fetched the cited pages with tools/review/fetch_pages.py, read them in full, ran tools/review/phrase_check.py and compared the remaining misses by hand.
