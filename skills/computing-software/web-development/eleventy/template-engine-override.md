---
id: computing-software.web-development.eleventy.template-engine-override
name: template-engine-override
category: computing-software
field: web-development
product: eleventy
tags: [templateengineoverride, template-language-override, markdown-pairing, preprocess-engine]
level: practitioner
status: docs-checked
description: "Change how Eleventy processes a single file with templateEngineOverride: swap engines, pair njk with md, or disable transformation with false."
sources:
  - https://raw.githubusercontent.com/11ty/11ty-website/main/src/docs/template-overrides.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Eleventy picks the engine by (1) file extension (which also finds the files), (2) config: `markdownTemplateEngine` and `htmlTemplateEngine` (use `false` to avoid preprocessing; for HTML that means the content is passed through untransformed), and (3) `templateEngineOverride` in front matter (0.2.14+).

The value is one engine, or Markdown paired with one other engine.

Replace the engine: in `example.liquid`, this parses the file as Nunjucks:

```md
---
templateEngineOverride: njk
---
```

Markdown files are normally preprocessed by the global Markdown engine, so when overriding list every engine you want. Only Markdown can be paired; any other combination throws an error.

```md
---
templateEngineOverride: md
---
```

Markdown only, no preprocessing.

```md
---
templateEngineOverride: njk,md
---
```

Nunjucks first, then Markdown.

```md
---
templateEngineOverride: false
---
```

Any falsy value copies the content without transformation.

## Checked

2026-11-08. Confirmed against the Eleventy docs Overriding the Template Language page (markdown source): the three ways to choose an engine, the 0.2.14 version note, the njk-in-liquid-file example, the md-pairing rule and error, and the falsy-value behaviour. Nothing removed.

Method: documentation only; no commands were run.
