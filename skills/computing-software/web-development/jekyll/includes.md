---
id: computing-software.web-development.jekyll.includes
name: includes
category: computing-software
field: web-development
product: jekyll
tags: [include-tag, include-relative, includes-dir, dynamic-include-name]
level: practitioner
status: docs-checked
description: "Insert partials with the include tag from _includes, use include_relative for paths next to the current file, and pick the file name from a variable."
sources:
  - https://raw.githubusercontent.com/jekyll/jekyll/master/docs/_docs/includes.md
  - https://raw.githubusercontent.com/jekyll/jekyll/master/docs/_docs/configuration/incremental-regeneration.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`include` inserts a file from the `_includes` directory at the source root:

```liquid
{% include footer.html %}
```

`include_relative` resolves relative to the file using the tag, so the content need not be in `_includes`:

```liquid
{% include_relative somedir/footer.html %}
```

If `_posts/2014-09-03-my-file.markdown` uses it, the included file must be in `_posts` or a subdirectory. `../` cannot reach a higher directory. All other `include` capabilities, such as variables, work with it.

The file name can come from a variable. With `my_variable: footer_company_a.html` in front matter:

```liquid
{% if page.my_variable %}
  {% include {{ page.my_variable }} %}
{% endif %}
```

This inserts `_includes/footer_company_a.html`.

Avoid too many includes: they slow the build, so do not use one for every image.

For incremental builds, the only dependency types tracked are includes and layouts.

## Checked

2026-11-04. Confirmed against the Jekyll includes doc and the incremental regeneration doc: `_includes` lookup, `include_relative` with the `_posts` example and no `../`, variable file names, the build-time warning, and the tracked dependency types. Fixed one point: the page says other `include` capabilities such as variables work with `include_relative`, not parameters.

Method: documentation only; no commands were run.
