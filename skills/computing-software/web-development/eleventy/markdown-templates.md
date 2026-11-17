---
id: computing-software.web-development.eleventy.markdown-templates
name: markdown-templates
category: computing-software
field: web-development
product: eleventy
tags: [markdown, markdown-it, amend-library, indented-code-blocks, paired-shortcodes]
level: practitioner
status: docs-checked
description: "Configure Eleventy Markdown: markdown-it defaults, setLibrary, amendLibrary plugins, indented code blocks and the paired shortcode HTML block pitfall."
sources:
  - https://www.11ty.dev/docs/languages/markdown/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`.md` files use `markdown-it` (Eleventy 3.x uses markdown-it 14). Markdown files are pre-processed as Liquid by default; change globally in config or per template with `templateEngineOverride`.

Default option difference: `html: true`. Indented code blocks are disabled since 2.0.

**Own instance** (0.3.0+):

```js
import markdownIt from "markdown-it";
eleventyConfig.setLibrary("md", markdownIt({ html: true, breaks: true, linkify: true }));
```

**Amend** (2.0.0+), works on the default or your own instance, and is how you add plugins:

```js
eleventyConfig.amendLibrary("md", (mdLib) => mdLib.use(emoji));
eleventyConfig.amendLibrary("md", (mdLib) => mdLib.enable("code")); // re-enable indented code blocks
```

Highlighting: use fenced code blocks plus the Syntax Highlighting plugin.

**Indented code blocks:** if re-enabled, any content indented four or more spaces after a line break becomes code, including output of includes and shortcodes. Do not return indented template literals from shortcodes; strip indentation (e.g. the `outdent` package).

**Pitfall: paired shortcodes.** Returning `content` as is gets processed as Markdown. Wrapping it as `<div>${content}</div>` makes Markdown treat it as an HTML block, so nested Markdown is not transformed.

## Checked

Method: 2026-11-08 compared against the 11ty website source markdown for the Markdown language page (languages/markdown). Defaults, setLibrary, amendLibrary, indented code block notes and the paired shortcode pitfall match the page; no changes to the technical content.
