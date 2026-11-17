---
id: computing-software.web-development.eleventy.filters
name: filters
category: computing-software
field: web-development
product: eleventy
tags: [filters, addfilter, async-filter, getfilter, memoize]
level: practitioner
status: docs-checked
description: "Add universal and per-engine Eleventy filters, use async filters, scoped this.page data, getFilter to reuse filters and memoization."
sources:
  - https://www.11ty.dev/docs/filters/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A filter transforms data inside template syntax and can be chained. Add universal filters in config; they reach JavaScript, Markdown, Nunjucks, Liquid and WebC. Markdown uses its preprocessor's filters.

```js
export default function (eleventyConfig) {
  eleventyConfig.addFilter("makeUppercase", function (value) { /* ... */ });
  eleventyConfig.addAsyncFilter("makeUppercase", async function (value) { /* ... */ });
}
```

Use: `{{ name | makeUppercase }}`; in `.11ty.js` call `this.makeUppercase(name)`.

**Async** (2.0.0+): `addFilter` accepts async callbacks, as does `addAsyncFilter`; both reach Liquid, Nunjucks and JavaScript.

**Scoped data** on `this`: `page`, `eleventy` (2.0.0+), Nunjucks-only `env` and `ctx` (3.0.0+). Avoid arrow functions.

**Reuse:** `eleventyConfig.getFilter("url")` returns a filter's callback, for aliasing or using inside shortcodes:

```js
return `<img src="${eleventyConfig.getFilter("url")(url)}" alt="${alt}">`;
```

**Memoize** with a library such as `memoize` around the callback. Eleventy 3.0 already memoizes the built-in `slug`, `slugify` and `inputPathToUrl` filters.

**Per-engine:** `addLiquidFilter`, `addNunjucksFilter`, `addNunjucksAsyncFilter` (callback-based; read the Nunjucks page first), `addJavaScriptFunction`. `addFilter` is an alias for calling all of them.

## Checked

2026-11-04. Confirmed against the Eleventy Filters page: universal filters reaching JavaScript, Markdown, Nunjucks, Liquid and WebC, Markdown using its preprocessor's filters, addFilter and addAsyncFilter, async support (v2.0.0), scoped this.page and this.eleventy (v2.0.0) and Nunjucks env and ctx (v3.0.0), no arrow functions, getFilter reuse, memoize and the Eleventy 3.0 memoization of slug, slugify and inputPathToUrl, and the per-engine methods. Removed the unconfirmed 0.7.0+ and 0.11.0+ version gates and corrected the canary gate to 2.0.0.

Method: documentation only; no commands were run.
