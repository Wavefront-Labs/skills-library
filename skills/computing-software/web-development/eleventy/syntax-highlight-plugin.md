---
id: computing-software.web-development.eleventy.syntax-highlight-plugin
name: syntax-highlight-plugin
category: computing-software
field: web-development
product: eleventy
tags: [syntax-highlighting, prismjs, diff-highlight, code-blocks, build-time]
level: intro
status: docs-checked
description: "Highlight code at build time with PrismJS via @11ty/eleventy-plugin-syntaxhighlight: install, options, theme CSS, highlighters for each language and diff- syntax."
sources:
  - https://www.11ty.dev/docs/plugins/syntaxhighlight/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Build-time PrismJS highlighting with no browser JavaScript. Docs apply to v3.2.0+.

```sh
npm install @11ty/eleventy-plugin-syntaxhighlight
```

```js
import syntaxHighlight from "@11ty/eleventy-plugin-syntaxhighlight";
export default function (eleventyConfig) {
  eleventyConfig.addPlugin(syntaxHighlight, { /* options */ });
}
```

**Options:** `lineSeparator`, `templateFormats` (default `["*"]`; `11ty.js` supported in v4.0.0), `init({ Prism })` to add custom languages, `preAttributes` and `codeAttributes` (3.1.1; callbacks from 4.1.0), `errorOnInvalidLanguage` (5.0.0).

**Theme CSS:** you must supply a PrismJS theme yourself, from a CDN link in the layout, a downloaded file or a style tag.

**Highlighters:** Markdown triple-backtick fences, Liquid `{% highlight %}` tag, Nunjucks paired shortcode `highlight`, JavaScript `this.highlight()` (v4.0.0), WebC `<syntax-highlight>` (v4.2.0). See PrismJS for supported languages.

**Diffs** (v3.2.2): prefix the language with `diff-` (for example `diff-js`) and start lines with `+` or `-`. Plain `diff` gives plaintext highlighting. You must add CSS for `.token.inserted` and `.token.deleted`. v3.2+ bundles Prism's `diff-highlight`; the old line-highlight feature is deprecated.

## Checked

Method: 2026-11-08 compared against the 11ty website source markdown for the Syntax Highlighting plugin page (plugins/syntaxhighlight). Install, options with version notes, theme CSS, highlighters and diff syntax match the page; no changes to the technical content.
