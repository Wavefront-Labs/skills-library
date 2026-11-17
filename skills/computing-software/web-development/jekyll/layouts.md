---
id: computing-software.web-development.jekyll.layouts
name: layouts
category: computing-software
field: web-development
product: jekyll
tags: [layouts, default-layout, content-variable, layout-inheritance, layout-variables]
level: practitioner
status: docs-checked
description: "Write Jekyll layouts in _layouts: the content variable, choosing a layout in front matter, chaining layouts by inheritance and reading layout front matter."
sources:
  - https://raw.githubusercontent.com/jekyll/jekyll/master/docs/_docs/layouts.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Layouts wrap content so navigation and footers are written once. They live in `_layouts`, by convention with a base `default.html` that others inherit from. Jekyll looks for `_layouts` at the root of the site `source` or of the theme; `layouts_dir` can rename it but it must still sit at the source root.

`content` holds the rendered content of the wrapped page or post. Front matter of the origin is available, e.g. `page.title`:

```liquid
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>{{ page.title }}</title>
  </head>
  <body>
    <section>
      {{ content }}
    </section>
  </body>
</html>
```

Select it per file, or via front matter defaults:

```markdown
---
title: My First Page
layout: default
---
```

Inheritance: a layout names its parent in its own front matter. `_layouts/post.html`:

```liquid
---
layout: default
---
<p>{{ page.date }} - Written by {{ page.author }}</p>

{{ content }}
```

Layouts can carry their own front matter, but read it as `layout.<name>`, not `page.<name>`:

```liquid
---
city: San Francisco
---
<p>{{ layout.city }}</p>
```

## Checked

2026-11-04. Confirmed against the Jekyll layouts doc: `_layouts` location and `layouts_dir` note, `content` variable, `default.html` convention, choosing a layout in front matter or defaults, inheritance via `layout: default` in the layout, and `layout.<name>` for layout front matter. Nothing removed.

Method: documentation only; no commands were run.
