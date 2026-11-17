---
id: computing-software.web-development.eleventy.layout-chaining
name: layout-chaining
category: computing-software
field: web-development
product: eleventy
tags: [layout-chaining, nested-layouts, template-inheritance, extends]
level: practitioner
status: docs-checked
description: "Chain Eleventy layouts by adding a layout key to a layout file, mix template languages, and know how it differs from engine-level extends."
sources:
  - https://raw.githubusercontent.com/11ty/11ty-website/main/src/docs/layout-chaining.md
  - https://raw.githubusercontent.com/11ty/11ty-website/main/src/docs/layouts.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A layout can itself have a `layout` in its front matter, and the chain continues. Layouts and content may use different template languages.

```md
---
layout: mainlayout.njk
title: My Rad Blog
---
# My Rad Markdown Blog Post
```

`_includes/mainlayout.njk` wraps the content in a main element and names its own layout:

```njk
---
layout: mylayout.njk
---
<main>{{ content | safe }}</main>
```

`_includes/mylayout.njk` is the outer HTML shell:

```njk
<!DOCTYPE html>
<html lang="en">
  <head><title>{{title}}</title></head>
  <body>{{ content | safe }}</body>
</html>
```

The output is the shell wrapping `<main>` wrapping the rendered post, written to the post's own output path.

Data merges along the chain: the closer to the content, the higher the priority.

Template-language reuse such as Nunjucks `{% extends %}` (Template Inheritance) still works. Eleventy layouts sit a layer above and add a multi-language mechanism configured in front matter that also shares data.

## Checked

2026-11-08. Confirmed against the Eleventy docs Layout Chaining page (markdown source): chaining via a layout key in the layout, mixed template languages, the mainlayout/mylayout example, and the addendum about Nunjucks Template Inheritance. Removed the claim that extends searches the includes directory and not the layouts directory, which the page does not state. The "closer to the content, higher priority" line comes from the Layouts page, not this one.

Method: documentation only; no commands were run.
