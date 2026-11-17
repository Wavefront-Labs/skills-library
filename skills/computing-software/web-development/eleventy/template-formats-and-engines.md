---
id: computing-software.web-development.eleventy.template-formats-and-engines
name: template-formats-and-engines
category: computing-software
field: web-development
product: eleventy
tags: [template-formats, markdown-template-engine, html-template-engine, formats-flag]
level: practitioner
status: docs-checked
description: "Choose which file types Eleventy processes with templateFormats and set the preprocessing engine for Markdown and HTML templates."
sources:
  - https://raw.githubusercontent.com/11ty/11ty-website/main/src/docs/config.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`templateFormats` lists the file extensions Eleventy transforms. Default: `html,liquid,ejs,md,hbs,mustache,haml,pug,njk,11ty.js`. Values are template engine short names.

```js
export default function (eleventyConfig) {
  // Reset to this value
  eleventyConfig.setTemplateFormats("html,liquid,njk");
  // Additive to existing
  eleventyConfig.addTemplateFormats("pug,haml");
  // Arrays work too
  eleventyConfig.setTemplateFormats(["html", "liquid", "njk"]);
};
```

CLI override: `npx @11ty/eleventy --formats=html,liquid,njk` (comma separated).

Files with an opted-in extension that has no template engine are passed through to the output directory (see passthrough copy).

File extensions are case insensitive.

Markdown and HTML files are first preprocessed by a template engine (default `liquid` for both). Valid values are a template engine short name or `false`:

- Object key: `markdownTemplateEngine`, API `setMarkdownTemplateEngine`
- Object key: `htmlTemplateEngine`, API `setHtmlTemplateEngine`

Set either to `false` to skip preprocessing so that template syntax in the file is left alone.

## Checked

2026-11-08. Confirmed against the Eleventy docs Configuration page (markdown source): the templateFormats default list, setTemplateFormats (0.2.14) and addTemplateFormats (0.11.0), the --formats flag, case-insensitive extensions, passthrough of extensions without an engine, and the markdown and HTML engine keys with liquid defaults. The page lists the setMarkdownTemplateEngine and setHtmlTemplateEngine API methods as added in 4.0.0-alpha.1, so they may not exist in older releases. Reworded the "skip preprocessing" line to the page's own description of false as a valid option.

Method: documentation only; no commands were run.
