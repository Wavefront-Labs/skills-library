---
id: computing-software.web-development.eleventy.layouts
name: layouts
category: computing-software
field: web-development
product: eleventy
tags: [layouts, layout-key, content-variable, layout-alias, double-escaping]
level: intro
status: docs-checked
description: "Wrap Eleventy content in layouts with the layout front matter key, output content unescaped, alias layout names and resolve file extensions."
sources:
  - https://raw.githubusercontent.com/11ty/11ty-website/main/src/docs/layouts.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Set `layout: mylayout.njk` in front matter. Eleventy looks in the includes folder (`_includes/mylayout.njk`) or the layouts directory if configured. Subdirectories work (`layouts/base.njk`). The layout language need not match the content's (an `ejs` template can use a `njk` layout).

The layout receives the child output as `content`. Avoid double-escaping:

| Language | Unescaped content |
| --- | --- |
| Nunjucks | `{{ content \| safe }}` |
| EJS | `<%- content %>` |
| Handlebars, Mustache | `{{{ content }}}` |
| Liquid | `{{ content }}` (unescaped by default) |
| HAML | `! #{ content }` |
| Pug | `!{content}` |

Layouts may have front matter. It merges with the content's data and the content wins on conflicts. The placement of layout front matter in the data cascade changed in 1.0; the page lists the current order in its Sources of Data section.

**Aliases** (0.2.8+): `eleventyConfig.addLayoutAlias("post", "layouts/post.njk")` lets old `layout: post` values keep working.

**Extensionless layouts** (`layout: mylayout`) make Eleventy search all supported formats `mylayout.*`. That is slower and ambiguous when `mylayout.njk` and `mylayout.liquid` both exist. Disable with `eleventyConfig.setLayoutResolution(false)` (2.0.0-canary.21+).

## Checked

2026-11-08. Confirmed against the Eleventy docs Layouts page (markdown source): the layout key and includes lookup, subdirectories, mixed languages, the content variable, the double-escaping table (the page also lists Handlebars/Mustache/HAML/Pug as shown), layout front matter merging with content winning, aliases, and extensionless resolution with setLayoutResolution. Removed the specific cascade position claim, because the page pulls that list from an include not visible in the source; it now only says the position changed in 1.0.

Method: documentation only; no commands were run.
