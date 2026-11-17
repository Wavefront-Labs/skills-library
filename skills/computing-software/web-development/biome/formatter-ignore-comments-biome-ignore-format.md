---
id: computing-software.web-development.biome.formatter-ignore-comments-biome-ignore-format
name: formatter-ignore-comments-biome-ignore-format
category: computing-software
field: web-development
product: biome
tags: [biome, biome-ignore, biome-ignore-all, ignore-format, suppress-formatter, generated-files, format-comments]
level: practitioner
status: docs-checked
description: "Skip formatting for a whole file with biome-ignore-all format at the top or a single node with biome-ignore format, always with a reason."
sources:
  - https://raw.githubusercontent.com/biomejs/website/main/src/content/docs/en/formatter/index.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Sometimes formatted code is not ideal (matrices, aligned tables, generated output). Biome has two formatter suppressions.

**Whole file.** Put `biome-ignore-all format: <reason>` at the top of the file:

```js
// biome-ignore-all format: generated file
const expr1 =
  [
    (2 * n) / (r - l),
    0,
  ];
```

The comment must be **at the top of the file** to apply to the entire file.

**A single node.** Place `biome-ignore format: <reason>` immediately before the node:

```js
const expr =
  // biome-ignore format: the array should not be formatted
  [
    (2 * n) / (r - l), 0, (r + l) / (r - l), 0,
    0, (2 * n) / (t - b), (t + b) / (t - b), 0,
  ];
```

## Checked

2026-11-04: every remaining claim, flag, default and example was compared with the cited page(s) read in full and confirmed. Removed: the 'mandatory explanation' paragraph and the advice to prefer `formatter.includes` and the invented Verify step.

Method: fetched the cited pages with tools/review/fetch_pages.py, read them in full, ran tools/review/phrase_check.py and compared the remaining misses by hand.
