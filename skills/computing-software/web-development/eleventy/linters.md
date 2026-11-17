---
id: computing-software.web-development.eleventy.linters
name: linters
category: computing-software
field: web-development
product: eleventy
tags: [linters, addlinter, data-filter-selectors, typescript-types]
level: practitioner
status: docs-checked
description: "Add Eleventy linters that inspect template output without changing it, include data cascade values in JSON output, and enable config type hints."
sources:
  - https://raw.githubusercontent.com/11ty/11ty-website/main/src/docs/config.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Linters analyse a template's output without modifying it (unlike transforms). Callback may be sync or async. `this` has `inputPath`, `outputPath` and (Eleventy 2.0+) the full `page` variable.

```js
export default function (eleventyConfig) {
  eleventyConfig.addLinter("linter-name", async function (content) {
    console.log(this.inputPath);
    console.log(this.outputPath);
    console.log(this.page.inputPath);
  });
};
```

Example from the docs: log a warning when a Markdown file contains a trigger word such as "simply" or "obviously" (packaged as eleventy-plugin-inclusive-language). Inside the callback, guard with `this.inputPath.endsWith(".md")`.

**Data filter selectors** (1.0.0+; `--to=json`, `--to=ndjson`): a `Set` of lodash selectors that choose data cascade values to add to the output as a `data` property.

```js
export default function (eleventyConfig) {
  eleventyConfig.dataFilterSelectors.add("page");
}
```

**Type hints.** For IDE autocomplete, annotate the config function:

```js
/** @param {import("@11ty/eleventy/UserConfig").default} eleventyConfig */
export default function (eleventyConfig) {}
```

## Checked

2026-11-08. Confirmed against the Eleventy docs Configuration page (markdown source), Linters, Data Filter Selectors and TypeScript Type Definitions sections: addLinter signature and this properties, the inclusive-language example and its plugin packaging, dataFilterSelectors as a Set of lodash selectors producing a data property, and the JSDoc type hint. Added the 1.0.0 version note. The page's example itself uses the older (content, inputPath, outputPath) arguments and notes that 1.0+ should use this.inputPath instead. Nothing else removed.

Method: documentation only; no commands were run.
