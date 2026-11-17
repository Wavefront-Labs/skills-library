---
id: computing-software.web-development.eleventy.liquid-templates
name: liquid-templates
category: computing-software
field: web-development
product: eleventy
tags: [liquid, liquidjs, dynamic-partials, jstruthy, shortcodes, parameter-parsing]
level: practitioner
status: docs-checked
description: "Use Liquid in Eleventy: options, jsTruthy, quoted include paths and dynamicPartials, filters, async shortcodes and builtin parameter parsing."
sources:
  - https://www.11ty.dev/docs/languages/liquid/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`.liquid` files use `liquidjs` (10.x for Eleventy 2 and 3). Default options differ from liquidjs; see `getLiquidOptions` in Eleventy's `Liquid.js`.

**Options:** `eleventyConfig.setLiquidOptions({ dynamicPartials: false, strictFilters: false })` (`strictFilters` was `strict_filters` before 1.0). `setLibrary("liquid", new Liquid(options))` overrides it.

**Truthiness:** in LiquidJS `""` and `0` are truthy. Set `jsTruthy: true` for JS rules.

**Includes:** `{% include 'user' %}` finds `_includes/user.liquid`. Unquoted `{% include user %}` needs `dynamicPartials: false` (default flipped to true in 1.0). Relative `./`/`../` since 0.9.0, but an `_includes` file of the same path wins. Pass data: `{% include 'user' with 'Ava' %}` or `{% include 'user', user1: 'Ava' %}`. No front matter processing.

**Filters:** `addLiquidFilter` or universal `addFilter`; async works natively. Call `{{ "first" | f: "second", "third" }}`.

**Shortcodes:** `addLiquidShortcode`, `addPairedLiquidShortcode`; async functions work. Commas between arguments are optional.

**Parameter parsing:** `setLiquidParameterParsing("builtin")` switches to Liquid-native parsing; current default is `"legacy"`.

Non-arrow functions can read `this.page` (0.11.0+).

## Checked

Method: 2026-11-08 compared against the 11ty website source markdown for the Liquid language page (languages/liquid). Options, truthiness, include rules, filters, shortcodes, parameter parsing and this.page match the page; no changes to the technical content.
