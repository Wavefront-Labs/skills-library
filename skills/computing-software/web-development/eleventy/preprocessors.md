---
id: computing-software.web-development.eleventy.preprocessors
name: preprocessors
category: computing-software
field: web-development
product: eleventy
tags: [preprocessors, addpreprocessor, draft-posts, skip-templates]
level: advanced
status: docs-checked
description: "Intercept template content before rendering with addPreprocessor, skip files by returning false, and implement a build-only drafts workflow."
sources:
  - https://raw.githubusercontent.com/11ty/11ty-website/main/src/docs/config-preprocessors.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Preprocessors (3.0.0-alpha.17+) modify template content in memory before Eleventy processes it. They apply to templates, not layouts.

```js
eleventyConfig.addPreprocessor("drafts", "njk,md,liquid", (data, content) => {
  if (data.draft) {
    return false; // ignore this file
  }
  return `${content}<!-- Template file: {{ page.inputPath }} -->`;
});
```

- Argument 1: an arbitrary name, used in error messages.
- Argument 2: a comma-separated string or an Array of file extensions (the docs also use `"*"`).
- Return `false` to skip the template, like `.eleventyignore`.
- Return nothing or `undefined` for no change (unlike transforms, which must return content).
- Returning a string replaces the raw input; be careful.

**Drafts workflow:** with `draft: true` anywhere in the data cascade, build the file only under `--serve` or `--watch`:

```js
eleventyConfig.addPreprocessor("drafts", "*", (data, content) => {
  if (data.draft && process.env.ELEVENTY_RUN_MODE === "build") {
    return false;
  }
});
```

The page says the same approach can exclude content before a publish date set in front matter.

Preprocessors run before most computed data is resolved, so `eleventyComputed` values are not available in the `data` argument.

## Checked

2026-11-08. Confirmed against the Eleventy docs Preprocessors page (markdown source): the 3.0.0-alpha.17 version note, templates not layouts, the argument list, return false versus undefined, the drafts workflow and the publish-date remark. Added the page's note that eleventyComputed values are unavailable. Nothing removed.

Method: documentation only; no commands were run.
