---
id: computing-software.web-development.eleventy.nunjucks-templates
name: nunjucks-templates
category: computing-software
field: web-development
product: eleventy
tags: [nunjucks, njk, async-shortcodes, setasync, named-arguments, globals]
level: practitioner
status: docs-checked
description: "Use Nunjucks in Eleventy: environment options, includes and extends paths, async filters and shortcodes, named arguments, setAsync and the macro pitfall."
sources:
  - https://www.11ty.dev/docs/languages/nunjucks/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`.njk` files use `nunjucks` 3.x with Nunjucks defaults.

**Options** (1.0.0+): `eleventyConfig.setNunjucksEnvironmentOptions({ throwOnUndefined: true })`. Or pass your own via `setLibrary("njk", new Nunjucks.Environment(new Nunjucks.FileSystemLoader("_includes")))`, which overrides the options method.

**Paths:** include, extends and import look in `_includes`; relative `./` and `../` (0.9.0+) resolve from the template. Included files get no front matter processing.

**Filters:** prefer universal `addFilter`. Nunjucks-only: `addNunjucksFilter`, and `addNunjucksAsyncFilter(name, function (value, callback) { callback(null, result) })`. Multi-arg call: `{{ "a" | f("b", "c") }}`.

**Shortcodes:** `addNunjucksShortcode`, `addPairedNunjucksShortcode`, and async `addNunjucksAsyncShortcode`, `addPairedNunjucksAsyncShortcode` (0.10.0+). Nunjucks-only named arguments pass one object, order free, any optional:

```njk
{% user name="Zach Leatherman", twitter="zachleat" %}
```

**Globals** (1.0.0+): `eleventyConfig.addNunjucksGlobal("fortytwo", () => 42)`, used as `{{ fortytwo() }}`. Not async-friendly.

**Pitfalls:** macros cannot do anything async. `{% set %}` cannot capture async shortcode output; use `{% setAsync "name" %}...{% endsetAsync %}` (1.0.0+), whose first argument is a string.

Filters and shortcodes can access `page`, `eleventy`, `ctx` and `env`; the Nunjucks page defers details to the Shortcodes and Filters docs.

## Checked

Method: 2026-11-08 compared against the 11ty website source markdown for the Nunjucks language page (languages/nunjucks). Options, paths, filters, shortcodes, named arguments, globals and pitfalls match the page. Removed the "via this, not arrow functions" detail, which this page does not state for Nunjucks.
