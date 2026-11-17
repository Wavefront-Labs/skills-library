---
id: computing-software.web-development.eleventy.shortcodes
name: shortcodes
category: computing-software
field: web-development
product: eleventy
tags: [shortcodes, paired-shortcodes, addshortcode, async-shortcode, memoize]
level: practitioner
status: docs-checked
description: "Add Eleventy shortcodes and paired shortcodes, use async versions and scoped this.page data, add per-engine variants and memoize results."
sources:
  - https://raw.githubusercontent.com/11ty/11ty-website/main/src/docs/shortcodes.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Shortcodes (0.5.0+) return a string for reusable content. Supported in JavaScript, Liquid, Nunjucks, Markdown and Handlebars (sync only). Markdown is preprocessed as Liquid by default, so Liquid shortcodes work there.

```js
export default function (eleventyConfig) {
  eleventyConfig.addShortcode("user", function (firstName, lastName) { /* ... */ });
  // async works in addShortcode from 2.0.0-canary.24
  eleventyConfig.addAsyncShortcode("user", async function (myName) { /* ... */ });
}
```

**Paired shortcodes** have start and end tags; the first callback argument is the nested content.

```js
eleventyConfig.addPairedShortcode("user", function (content, firstName, lastName) {});
eleventyConfig.addPairedAsyncShortcode("user", async function (content, myName) {});
```

**Scoped data** on `this`: `page`, `eleventy`, and Nunjucks-only `env` and `ctx`. The page's example comments: make sure you are not using an arrow function.

**Per-engine:** `addLiquidShortcode`, `addPairedLiquidShortcode`, `addNunjucksShortcode`, `addNunjucksAsyncShortcode` (and paired forms), and `addJavaScriptFunction`. Plain `addShortcode` adds to every supported engine. Await async JavaScript functions in templates.

**Memoize** by wrapping the callback with a library such as `memoize` to cache repeated calls with identical input.

Shortcodes are sugar around template language custom tags.

## Checked

2026-11-08. Confirmed against the Eleventy docs Shortcodes page (markdown source): 0.5.0 version note, supported languages, async support from 2.0.0-canary.24, paired shortcodes, scoped this data, memoize, and per-engine registration functions. Removed the "prefer them" advice and the stated consequence of arrow functions, which the page does not give; the this.page and this.eleventy version notes (0.11.0, 2.0.0-canary.5) were not carried and are not asserted here.

Method: documentation only; no commands were run.
