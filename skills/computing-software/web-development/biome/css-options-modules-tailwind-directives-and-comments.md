---
id: computing-software.web-development.biome.css-options-modules-tailwind-directives-and-comments
name: css-options-modules-tailwind-directives-and-comments
category: computing-software
field: web-development
product: biome
tags: [biome, css-formatter, css-parser, css-modules, tailwind-directives, line-comments, scss, delimiterspacing, quotestyle]
level: practitioner
status: docs-checked
description: "Reference for css.parser and css.formatter: CSS Modules syntax, Tailwind 4 directives, // comments, quote style and delimiter spacing."
sources:
  - https://raw.githubusercontent.com/biomejs/website/main/src/content/docs/en/reference/configuration.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Parser**
- `css.parser.allowWrongLineComments` (default false): accept `//` comments in plain CSS (standard CSS treats `//` as delimiter characters). SCSS accepts them regardless.
- `css.parser.cssModules` (default false): enable `:local`, `:global`, `composes` and `@value`. Unset, Biome turns it on automatically for files named `*.module.css`, so enable explicitly only for other naming conventions.
- `css.parser.tailwindDirectives` (default false): parse Tailwind CSS 4 directives and functions such as `@theme`, `@utility`, `@variant`, `@source`, `@apply`. Unset, it is enabled automatically when `tailwind.stylesheet` is set.

**Formatter** (`css.formatter.*`)
- `enabled` (true), `indentStyle` (tab), `indentWidth` (2), `lineEnding` (lf), `lineWidth` (80), `trailingNewline` (true).
- `quoteStyle`: `double` (default) or `single`; may use the other when it avoids escaping; quotes in `@charset` are preserved.
- `delimiterSpacing` (false): when enabled, `rgb(0, 0, 0)` becomes `rgb( 0, 0, 0 )` and `[data-attr]` becomes `[ data-attr ]`; empty delimiters unchanged.

`css.linter.enabled` and `css.assist.enabled` default to true. `css.globals` is reserved for future analyzer support and currently has no effect.

Example:

```json
{ "css": { "parser": { "cssModules": true, "tailwindDirectives": true }, "formatter": { "quoteStyle": "single" } } }
```

## Checked

2026-11-04: every remaining claim, flag, default and example was compared with the cited page(s) read in full and confirmed. Removed: the invented Verify step.

Method: fetched the cited pages with tools/review/fetch_pages.py, read them in full, ran tools/review/phrase_check.py and compared the remaining misses by hand.
