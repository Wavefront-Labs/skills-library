---
id: computing-software.web-development.eleventy.dynamic-permalinks
name: dynamic-permalinks
category: computing-software
field: web-development
product: eleventy
tags: [dynamic-permalinks, permalink-template-syntax, slugify-permalink, dynamicpermalink, yaml-quoting]
level: practitioner
status: docs-checked
description: "Build Eleventy permalinks from data with template syntax, slugify and dates, quote YAML correctly, set them per directory and disable templating."
sources:
  - https://www.11ty.dev/docs/permalinks/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A permalink may use data variables and template syntax, rendered with the current template's engine. Markdown and HTML templates follow the configured preprocessing engine. Pagination variables work too. Use the `slugify` filter for URL-safe strings.

```yaml
---
title: This is a New Path
permalink: "subdir/{{ title | slugify }}/index.html"
---
```

Liquid date example: `permalink: "/{{ page.date | date: '%Y/%m/%d' }}/index.html"`.

**Quote template syntax in YAML.** Unquoted `permalink: {{ page.filePathStem }}.html` is parsed as an object and errors ("can not read a block mapping entry").

**Per directory.** In `recipes/recipes.11tydata.js` a title is not yet in the cascade, but `permalink` is implied computed data:

```js
export default {
  permalink: function ({ title }) {
    return `/recipes/${this.slugify(title)}`;
  },
};
```

**Disable templating.** `dynamicPermalink: false` in front matter keeps the string literal for one template (a pitfall for Pug users). Project-wide: `eleventyConfig.setDynamicPermalinks(false)`.

Change defaults for the whole project with `addGlobalData("permalink", ...)` using `page.filePathStem`.

## Checked

2026-11-04. Confirmed against the Eleventy Permalinks page: template syntax rendered with the current template engine, the slugify filter, pagination variables, the Liquid date example, the YAML quoting pitfall and its error message, the per-directory permalink function with this.slugify and implied computed data, the dynamicPermalink front matter option, setDynamicPermalinks(false) and the global-data approach. Nothing removed.

Method: documentation only; no commands were run.
