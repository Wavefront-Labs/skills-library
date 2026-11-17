---
id: computing-software.data-engineering.kestra.pebble-expression-syntax
name: pebble-expression-syntax
category: computing-software
field: data-engineering
product: kestra
tags: [pebble, expressions, templating, operators, fallback, render]
level: practitioner
status: docs-checked
description: "Pebble expression syntax in Kestra: delimiters, bracket notation, render(), operators and precedence, fallbacks, tags, tests and multiline JSON bodies."
sources:
  - https://kestra.io/docs/expressions/syntax
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Delimiters: `{{ ... }}` output, `{% ... %}` tags (`if`, `for`, `set`), `{# ... #}` comments. Use `raw` to print Pebble literally.

Access: `{{ foo.bar }}`, `{{ foo['foo-bar'] }}`, `{{ items[0] }}`. Hyphenated task IDs or keys need bracket notation.

Expressions render once; wrap deferred ones in `render()`, e.g. `{{ render(vars.trigger_or_yesterday) }}`.

Build JSON bodies as one expression piped to `toJson`:

```yaml
body: |
  {{ {
    "title": inputs.title,
    "priority": inputs.priority
  } | toJson }}
```

Operators: `== != < > <= >=`, `and or not is contains`, `isIn`, `+ - * / %`, `~` (concatenate). Precedence high to low starts with `.`, then `% / *`, `- +`, comparisons, `is`, `and`, `or`.

Fallbacks:

- `??` first non-null value.
- `???` fallback only if undefined.
- `? :` ternary.
- `?? raise` throws if all undefined.

Loops: `loop.index` is zero-based; also `loop.length`, `first`, `last`, `revindex`.

Tests with `is`: `defined`, `empty`, `null`, `even`, `odd`, `iterable`, `json`, `map`.

Macros see only their own arguments unless you pass `_context`.

## Checked

2026-11-04. Confirmed against the Kestra expression syntax page: delimiters and comments, raw, bracket notation, render(), the single-expression toJson body, operators, fallbacks, loop variables, tests and macro _context. Removed: the filter pipe from the precedence list, because the page text renders that list item blank.

Method: documentation only; no commands were run.
