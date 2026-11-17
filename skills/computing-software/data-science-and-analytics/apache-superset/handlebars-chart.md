---
id: computing-software.data-science-and-analytics.apache-superset.handlebars-chart
name: handlebars-chart
category: computing-software
field: data-science-and-analytics
product: apache-superset
tags: [handlebars, custom-chart, templates, helpers, data-variable]
level: practitioner
status: docs-checked
description: "Build custom Superset visuals with the Handlebars chart: the data variable, dateFormat and formatNumber helpers, just-handlebars-helpers names and gotchas."
sources:
  - https://github.com/apache/superset/blob/master/docs/docs/using-superset/handlebars-chart.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: render query results as custom HTML.

Write the template in the chart editor's Template field. Query results are available as `data`, an array of row objects:

```handlebars
{{#each data}}
  <p>{{this.name}}: {{this.value}}</p>
{{/each}}
```

Superset helpers:
- `dateFormat`: `{{dateFormat my_date format='MMMM YYYY'}}`; Day.js format string, default `YYYY-MM-DD`.
- `stringify`: object to JSON string, anything else to its string form.
- `formatNumber`: locale-aware, `{{formatNumber myNumber 'en-US'}}`; the locale is a BCP 47 tag, default `en-US`. It is not a D3 format.
- `parseJson`: parse a JSON string into an object.
- `group`: groups by a key via handlebars-group-by, `{{#group data by="department"}}` with `{{value}}` and `{{#each items}}` inside.

Superset also registers every helper from just-handlebars-helpers. Its names differ from the handlebars-helpers library (which spells math helpers add, subtract, multiply, divide). Calling an unregistered helper raises `Missing helper: "..."` and the chart renders blank. Documented names:
- Comparison: `eq`, `eqw`, `neq`, `neqw`, `lt`, `lte`, `gt`, `gte`.
- Logical: `and`, `or`, `not`, `ifx`, `coalesce`.
- String: `capitalizeFirst`, `capitalizeEach`, `uppercase`, `lowercase`, `excerpt`, `sprintf`, `concat`, `join`, `first`, `last`, `newLineToBr` (needs triple braces).
- Math: `sum`, `difference`, `multiplication`, `division`, `remainder`, `abs`, `ceil`, `floor`.
- Arrays: `includes`, `empty`, `count`.
- Formatting: `formatCurrency`.

Gotchas:
- `sum` takes exactly two arguments and does not total an array.
- There is no `round` helper; use `{{sprintf "%.0f" value}}`.
- `includes` tests array membership and returns false for a string, so it cannot check substrings.
- Comparison helpers inside `#if` need a subexpression: `{{#if (eq myVal "foo")}}`.
- Use raw blocks to show literal double curly braces.
- HTML output is sanitized by default according to the `HTML_SANITIZATION` setting.

## Checked

2026-11-08: read handlebars-chart.mdx in full. Removed claims not on the page: D3-style formatNumber, `group` listed as a just-handlebars helper, client-side rendering and secrets advice, style field advice.
Method: documentation only; no commands were run.
